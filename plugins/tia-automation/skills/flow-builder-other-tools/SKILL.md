---
name: flow-builder-other-tools
description: Build automation flows in Activepieces, Node-RED, Windmill or Huginn. Use when the user asks for an Activepieces flow, a Node-RED flow or flow JSON, a Windmill script or flow, a Huginn agent or scenario, or wants to move a Zapier, Make or n8n workflow to one of these tools.
---

# Flow Builder: Activepieces, Node-RED, Windmill and Huginn

Each tool thinks about automation differently. Build in the tool's own way instead of forcing an n8n shape onto it.

## Activepieces

- A **flow** is one trigger plus a list of steps (pieces). Branches and loops are steps too.
- Build it as numbered steps the user can click through: trigger piece, then each action piece with its fields.
- Data from earlier steps is picked in the data selector; describe it as `step name → field`.
- For code, use a Code step that exports an async `code` function returning the value the next step needs.
- Remind the user to test each step with sample data before publishing the flow.

## Node-RED

- A flow is nodes wired together on a canvas. You can hand over importable flow JSON: an array of node objects with `id`, `type`, `z` (tab id), `wires` and node settings.
- Common nodes: `inject` (manual or timed start), `http in` + `http response` (webhook endpoint), `http request`, `function`, `switch`, `change`, `debug`.
- Data travels in `msg`; the main value is `msg.payload`. A `function` node must `return msg;` (or an array for several outputs).
- Every `http in` needs a matching `http response`, or the caller waits until timeout.
- Import with Menu → Import, paste the JSON, then click Deploy.
- Protect the editor: set `adminAuth` in `settings.js` before exposing Node-RED to the internet.

## Windmill

- Start with a **script** (Python, TypeScript, Go, Bash or SQL). Its main function's parameters become the input form.
- Chain scripts into a **flow**, or put a script on a **schedule** for cron-style jobs.
- Store API keys as Windmill resources or variables, never inside the script.
- Hand over: the script code, the input schema, and whether it should be a flow, an app or a schedule.

## Huginn

- Huginn uses **agents** that create and receive **events**. A scenario is a group of agents.
- Typical chain: Website Agent or RSS Agent (watch) → Trigger Agent or Event Formatting Agent (filter, reshape) → Email, Slack or Webhook agent (act).
- Hand over each agent's type, name, schedule and its options JSON, plus which agent it receives events from.
- Set realistic check intervals; checking a site every minute can get your server blocked.

## Moving from Zapier, Make or n8n

1. List the source workflow's trigger, steps and filters.
2. Map each one to the target tool's equivalent and mark anything with no direct match.
3. Rebuild, then run old and new side by side on the same test data before switching off the old one.

## Do not

- Invent a piece, node or agent type. If unsure it exists, say so and suggest an HTTP or code step instead.
- Paste real credentials into flows.
