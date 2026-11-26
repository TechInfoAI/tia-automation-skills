---
name: automation-planner
description: Plan a business automation and pick the right tool (n8n, Activepieces, Node-RED, Windmill, Huginn, GitHub Actions or a plain cron job). Use when the user wants to automate a task, asks which automation tool to use, wants to replace Zapier, Make or IFTTT, or describes a repetitive job they want a workflow for.
---

# Automation Planner

Turn a vague "I want to automate this" into a clear flow and the cheapest tool that can run it. Plan first, build second.

## Step 1: Pin down the job

Ask only for what is missing:

- **Trigger:** what starts it? A form, a new row, an email, a webhook, a schedule, a page change.
- **Steps:** what happens to the data, in order.
- **Output:** where the result goes (CRM, sheet, Slack, email, database, file).
- **Volume:** runs per day and items per run.
- **Constraints:** budget, hosting (cloud or own server), coding skill, data that must stay private.

Write the flow back as one line before going further:
`Trigger → step → step → output (+ error path)`.

## Step 2: Pick the tool

| Pick | When it fits best | License note |
|---|---|---|
| **n8n** | Most business workflows, many app integrations, AI agent steps, visual editor | Fair-code (Sustainable Use License): free to self-host for your own business; reselling it as a service needs a deal |
| **Activepieces** | Non-technical teams who want a Zapier-like builder with AI steps | MIT, except the enterprise (ee) folders, which have their own license |
| **Node-RED** | Webhooks, IoT, MQTT, devices, lightweight API glue on small servers | Apache-2.0 |
| **Windmill** | Developers who write Python, TypeScript or SQL scripts and want them as flows, apps and cron jobs | Mostly AGPLv3 (some parts Apache-2.0); enterprise features under a commercial license |
| **Huginn** | Agents that watch websites, feeds and APIs and react to changes | MIT |
| **GitHub Actions** | Jobs tied to a code repository, or a free scheduled script | Free minutes vary by plan |
| **Plain cron + script** | One small job on a server you already have | Free |

Rules of thumb:
- Choose the simplest tool that covers the trigger and every app. Do not add a platform for one cron job.
- If the user already runs one of these tools, use it unless it clearly cannot do the job.
- If data must stay private, prefer a self-hosted option and say so.
- Always tell the user to check the current license on GitHub before reselling or hosting for clients.

## Step 3: Deliver the plan

1. The one-line flow.
2. The chosen tool and one sentence on why, plus the runner-up.
3. A numbered build list: each node or step, what it does, and the app credential it needs.
4. Error handling: what happens when a step fails (retry, alert, dead-letter sheet).
5. Rough running cost: server size or free tier, and any paid API calls such as AI models.
6. What to test before switching it on.

Then hand off to the matching builder skill: `n8n-workflow-builder` for n8n, `flow-builder-other-tools` for the others.

## Do not

- Promise an integration exists without checking the tool's docs or node list.
- Hide paid parts. AI model calls, SMS and some APIs cost money even when the tool is free.
- Build before the user agrees with the flow.
