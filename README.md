# TIA Automation Skills

**Free workflow automation skills for AI agents.** Add them to Claude, Claude Code, Codex, Cursor or any agent that reads `SKILL.md` files, then ask in plain words: *"build an n8n workflow that sends new form leads to HubSpot and Slack"*, *"why did my workflow run twice?"*, *"set up n8n on my VPS with HTTPS and backups"*.

One pack for **n8n, Activepieces, Node-RED, Windmill and Huginn**, not just one tool. No API keys. No accounts. No extra runtime. Two small helper scripts use only the Python standard library.

Made by [Tech Info AI](https://techinfoai.net) · Listed in the [Tech Info AI open-source directory](https://techinfoai.net/open-source/)

---

## The 9 skills

| Skill | What it does | Ask it like |
|---|---|---|
| `automation-planner` | Turns a task into a clear flow and picks the cheapest tool that can run it: n8n, Activepieces, Node-RED, Windmill, Huginn, GitHub Actions or plain cron. | "What's the best way to automate my lead follow-ups?" |
| `n8n-workflow-builder` | Builds importable n8n workflow JSON with correct expressions, Code nodes and error handling. Includes `n8n_lint.py`. | "Build an n8n workflow: Stripe webhook → Google Sheet → Slack" |
| `flow-builder-other-tools` | Builds flows the native way in Activepieces, Node-RED, Windmill and Huginn, and moves workflows from Zapier, Make or n8n. | "Make this a Node-RED flow I can import" |
| `api-and-webhooks` | Connects any API: auth, pagination, rate limits, retries, webhook signatures and duplicate protection. | "Call this API that has no n8n node" |
| `ai-agent-workflows` | Adds AI steps (classify, extract, summarize, agents, RAG) with structured output, cost estimates and human approval. | "Add an AI step that tags support tickets" |
| `scheduled-jobs` | Cron expressions, time zones, safe re-runs and monitoring jobs. Includes `cron_check.py`. | "Run this every weekday at 9 am Dhaka time" |
| `workflow-debugger` | Finds why a run failed, returned nothing, ran twice or stopped triggering, from the evidence in the run. | "My workflow says 401, fix it" |
| `self-host-setup` | Docker install, HTTPS reverse proxy, backups, updates and a security checklist for all five tools. | "Self-host n8n on a $5 VPS safely" |
| `automation-recipes` | Ready flows for sales, marketing, SEO and admin: lead capture, social posting, Search Console reports, review alerts, invoices. | "What can I automate for my agency?" |

## Install

### Claude Code (plugin)

```
/plugin marketplace add TechInfoAI/tia-automation-skills
/plugin install tia-automation@tia-automation-skills
```

Then just ask, or call a skill directly: `/tia-automation:n8n-workflow-builder`

### Claude.ai (web and desktop)

1. Download a skill's zip from the [`dist/`](dist/) folder, for example `n8n-workflow-builder.zip`.
2. In Claude, open **Settings → Capabilities → Skills** and upload the zip.
3. Start a new chat and ask for the task.

### Codex, Cursor and other agents

Copy the skill folders into your agent's skills folder:

```
git clone https://github.com/TechInfoAI/tia-automation-skills.git
cp -r tia-automation-skills/plugins/tia-automation/skills/* .claude/skills/   # or .agents/skills/
```

No skills support? Paste the contents of a `SKILL.md` into the chat as instructions.

## Helper scripts

Both use only the Python standard library.

```
python3 plugins/tia-automation/skills/n8n-workflow-builder/scripts/n8n_lint.py workflow.json
python3 plugins/tia-automation/skills/scheduled-jobs/scripts/cron_check.py "0 9 * * 1-5" --tz Asia/Dhaka --next 5
```

- `n8n_lint.py` (Python 3.8+): checks an exported n8n workflow for broken connections, duplicate node names, a missing trigger, disconnected nodes, webhooks with no authentication, hard-coded API keys or tokens, HTTP Request nodes without retries, no error workflow and workflows saved as active. Add `--json` for JSON. Exits with code 1 when it finds errors, so it works in CI.
- `cron_check.py` (Python 3.9+): explains a 5-field cron expression in plain English and lists the next run times in any time zone. Supports ranges, lists, steps, month and weekday names, and `@daily`-style shortcuts.

## Works with these tools

| Tool | What the skills cover |
|---|---|
| [n8n](https://github.com/n8n-io/n8n) | Workflow JSON, expressions, Code nodes, AI agents, error workflows, self-hosting |
| [Activepieces](https://github.com/activepieces/activepieces) | Flows, pieces, code steps, self-hosting |
| [Node-RED](https://github.com/node-red/node-red) | Importable flow JSON, function nodes, HTTP endpoints, editor security |
| [Windmill](https://github.com/windmill-labs/windmill) | Scripts, flows, schedules, resources |
| [Huginn](https://github.com/huginn/huginn) | Agents, events and scenarios for watching the web |

The skills give instructions to your AI agent. They don't install or run these tools for you, and they don't include any of their code.

## Why another automation skill pack?

Good n8n skill packs already exist. This pack fills the gaps we kept running into:

- **Tool-neutral**: helps you pick between five open-source tools instead of assuming n8n.
- **Light**: no MCP server, Node.js runtime or API key needed. If you already run an n8n MCP server, the n8n skill uses it.
- **Business-first**: ready recipes for sales, marketing, SEO and admin, with costs and human approval steps built in.
- **Safe by default**: workflows import inactive, secrets stay in credentials, webhooks get auth, backups get tested.

Want more depth on n8n? These projects inspired the scope of this pack (no code or text was copied):
[czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) (n8n skills built for the n8n-mcp server),
[czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp) (MCP server with n8n node docs and validation),
[tmolavi/n8n-agent-skills](https://github.com/tmolavi/n8n-agent-skills) (n8n skills for Claude Code, Codex and Cursor).

## Contributing

Issues and pull requests are welcome: new recipes, better prompts, more lint checks, fixes for wrong advice.

## License

MIT © Tech Info AI. The tools these skills work with have their own licenses; check each one before reselling or hosting it for clients.
