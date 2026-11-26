#!/usr/bin/env python3
"""Lint an exported n8n workflow JSON file.

Usage:
    python3 n8n_lint.py workflow.json [--json]

Checks for problems that commonly break imports or cause trouble in production:
broken connections, duplicate node names, missing trigger, disconnected nodes,
unprotected webhooks, hard-coded secrets, HTTP Request nodes without retries,
no error workflow and workflows saved as active.

Standard library only. Python 3.8+.
"""
import json
import re
import sys

TRIGGER_HINTS = ("trigger", "webhook", "cron", "schedule", "start", "formtrigger", "chattrigger", "mcptrigger")
SECRET_KEY_RE = re.compile(r"(api[_-]?key|apikey|secret|password|passwd|token|bearer|authorization)", re.I)
SECRET_VALUE_RE = re.compile(
    r"(sk-[A-Za-z0-9_\-]{16,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9\-]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_\-]{30,}|Bearer\s+[A-Za-z0-9\-_.=]{20,})"
)


def is_trigger(node):
    t = str(node.get("type", "")).lower()
    return any(h in t.split(".")[-1] for h in TRIGGER_HINTS)


def walk(obj, path=""):
    """Yield (path, key, value) for every scalar in a nested structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else str(k)
            if isinstance(v, (dict, list)):
                yield from walk(v, p)
            else:
                yield p, str(k), v
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")


def lint(wf):
    issues = []

    def add(level, msg, node=None):
        issues.append({"level": level, "node": node, "message": msg})

    if isinstance(wf, list):
        add("error", "File is a JSON array. n8n workflow exports are a single JSON object with 'nodes' and 'connections'.")
        return issues
    nodes = wf.get("nodes")
    conns = wf.get("connections", {})
    if not isinstance(nodes, list) or not nodes:
        add("error", "No 'nodes' list found. This does not look like an n8n workflow export.")
        return issues
    if not isinstance(conns, dict):
        add("error", "'connections' must be an object keyed by node name.")
        conns = {}

    names = [n.get("name") for n in nodes]
    seen = set()
    for name in names:
        if not name:
            add("error", "A node has no 'name'.")
        elif name in seen:
            add("error", f"Duplicate node name '{name}'. Connections refer to nodes by name, so names must be unique.", name)
        seen.add(name)
    name_set = set(n for n in names if n)

    for n in nodes:
        if not n.get("type"):
            add("error", "Node has no 'type'.", n.get("name"))
        if "typeVersion" not in n:
            add("warning", "Node has no 'typeVersion'; n8n may pick an unexpected version.", n.get("name"))
        if "position" not in n:
            add("info", "Node has no 'position'; it may stack on top of other nodes in the editor.", n.get("name"))

    incoming = {name: 0 for name in name_set}
    outgoing = {name: 0 for name in name_set}
    for src, outputs in conns.items():
        if src not in name_set:
            add("error", f"Connection starts from '{src}', but no node has that name.", src)
            continue
        if not isinstance(outputs, dict):
            continue
        for ctype, branches in outputs.items():
            for branch in branches or []:
                for link in branch or []:
                    tgt = link.get("node") if isinstance(link, dict) else None
                    if tgt not in name_set:
                        add("error", f"'{src}' connects to '{tgt}', but no node has that name.", src)
                        continue
                    outgoing[src] += 1
                    incoming[tgt] += 1

    triggers = [n for n in nodes if is_trigger(n)]
    if not triggers:
        add("warning", "No trigger node found (webhook, schedule, app trigger or manual trigger). The workflow cannot start on its own.")

    sticky = "n8n-nodes-base.stickyNote"
    for n in nodes:
        name = n.get("name")
        if not name or n.get("type") == sticky:
            continue
        if is_trigger(n):
            if outgoing.get(name, 0) == 0 and len(nodes) > 1:
                add("warning", "Trigger is not connected to any node.", name)
        elif incoming.get(name, 0) == 0 and outgoing.get(name, 0) == 0:
            # AI sub-nodes (models, memory, tools) connect through ai_* outputs and count as outgoing.
            add("warning", "Node is not connected to anything.", name)

    for n in nodes:
        t = str(n.get("type", ""))
        p = n.get("parameters", {}) or {}
        name = n.get("name")
        if t == "n8n-nodes-base.webhook":
            auth = p.get("authentication", "none")
            if auth in (None, "", "none"):
                add("warning", "Webhook has no authentication. Add header auth, basic auth or a signature check.", name)
        if t == "n8n-nodes-base.httpRequest" and not n.get("retryOnFail"):
            add("info", "HTTP Request has 'Retry On Fail' off. Turn it on for APIs that can time out or rate-limit.", name)
        if n.get("disabled"):
            add("info", "Node is disabled.", name)
        for path, key, value in walk(p):
            if not isinstance(value, str) or not value or value.startswith("="):
                continue
            if SECRET_VALUE_RE.search(value) or (SECRET_KEY_RE.search(key) and len(value) >= 12 and " " not in value):
                add("error", f"Possible hard-coded secret in parameter '{path}'. Move it into an n8n credential.", name)

    settings = wf.get("settings", {}) or {}
    if not settings.get("errorWorkflow"):
        add("info", "No error workflow set in workflow settings. Add one that starts with an Error Trigger and sends an alert.")
    if wf.get("active") is True:
        add("warning", "Workflow is saved as active. Import it inactive, test it, then switch it on.")

    return issues


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if len(argv) >= 2 else 2
    path = argv[1]
    as_json = "--json" in argv[2:]
    try:
        with open(path, encoding="utf-8") as f:
            wf = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Could not read JSON from {path}: {e}", file=sys.stderr)
        return 2

    issues = lint(wf)
    counts = {lvl: sum(1 for i in issues if i["level"] == lvl) for lvl in ("error", "warning", "info")}
    if as_json:
        print(json.dumps({"file": path, "workflow": wf.get("name") if isinstance(wf, dict) else None,
                          "counts": counts, "issues": issues}, indent=2))
    else:
        name = wf.get("name", "(unnamed)") if isinstance(wf, dict) else "(not a workflow)"
        n_nodes = len(wf.get("nodes", [])) if isinstance(wf, dict) else 0
        print(f"Workflow: {name}  |  nodes: {n_nodes}")
        print(f"Errors: {counts['error']}  Warnings: {counts['warning']}  Info: {counts['info']}")
        for i in issues:
            where = f" [{i['node']}]" if i["node"] else ""
            print(f"- {i['level'].upper()}{where}: {i['message']}")
        if not issues:
            print("No issues found.")
    return 1 if counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
