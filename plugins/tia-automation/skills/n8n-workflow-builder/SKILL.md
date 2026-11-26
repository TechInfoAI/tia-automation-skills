---
name: n8n-workflow-builder
description: Build, edit or fix an n8n workflow and hand back importable workflow JSON. Use when the user asks for an n8n workflow, n8n nodes, n8n expressions, an n8n Code node, or wants to check or improve an exported n8n workflow JSON file.
---

# n8n Workflow Builder

Build n8n workflows that import cleanly and survive real data. If an n8n MCP server is connected (for example n8n-mcp), use it to look up nodes and validate. Otherwise build the JSON by hand and run the linter below.

## Step 1: Confirm the flow

Get the one-line flow (`Trigger → steps → output`) and the apps involved. If it is unclear, use the `automation-planner` skill first.

## Step 2: Build the JSON

An n8n workflow export has this shape:

```json
{
  "name": "Lead to CRM",
  "nodes": [
    {"id": "uuid", "name": "Webhook", "type": "n8n-nodes-base.webhook", "typeVersion": 2, "position": [0, 0], "parameters": {}}
  ],
  "connections": {
    "Webhook": {"main": [[{"node": "Next Node", "type": "main", "index": 0}]]}
  },
  "settings": {},
  "active": false
}
```

Rules:
- Every node needs a unique `name`; `connections` refer to nodes by that name.
- Use the real node `type`, for example `n8n-nodes-base.webhook`, `n8n-nodes-base.scheduleTrigger`, `n8n-nodes-base.httpRequest`, `n8n-nodes-base.if`, `n8n-nodes-base.set`, `n8n-nodes-base.code`. Check the node list or MCP server if unsure, and say which `typeVersion` you assumed.
- Never put API keys or passwords in parameters. Reference a credential and leave a placeholder such as `REPLACE_WITH_CREDENTIAL`.
- Keep `"active": false`. The user turns it on after testing.
- Lay nodes out left to right, about 200 px apart, so the canvas is readable.

## Step 3: Expressions and Code nodes

- Expressions sit in `{{ }}` and a parameter that holds one starts with `=`: `"={{ $json.email }}"`.
- Data from a Webhook node arrives under `body`: use `$json.body.email`, not `$json.email`.
- Read another node's output with `$('Node Name').item.json.field`.
- A Code node in JavaScript must return an array of items, each shaped like `{ json: { ... } }`.
- Python Code nodes cannot use `$('Node')`; prefer JavaScript when you need other nodes' data.

## Step 4: Errors and safety

- Add an error path: set an error workflow in workflow settings that starts with an Error Trigger node and sends an alert.
- Turn on retries for HTTP Request nodes that call flaky APIs.
- Protect Webhook nodes with header auth, basic auth or a signature check. A public webhook URL is an open door.
- Batch large lists (Loop Over Items) and respect API rate limits.

## Step 5: Lint and hand over

If you can run code, save the JSON and run:
`python3 scripts/n8n_lint.py workflow.json` (add `--json` for machine output).
It flags broken connections, duplicate names, missing triggers, unprotected webhooks, hard-coded secrets, HTTP nodes without retries, no error workflow and workflows set to active.

Hand back:
1. The full JSON in one code block.
2. Import steps: in n8n, open a new workflow, paste the JSON on the canvas (or use Import from File).
3. The credentials to create, by app.
4. A test plan: one sample input and the expected output.
