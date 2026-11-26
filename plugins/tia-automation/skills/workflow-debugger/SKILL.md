---
name: workflow-debugger
description: Find and fix why an automation workflow failed, returned empty data, ran twice or stopped triggering, in n8n, Activepieces, Node-RED, Windmill, Huginn or GitHub Actions. Use when the user shares an error message, a failed execution, a workflow that "does nothing", or says their automation broke.
---

# Workflow Debugger

Fix the cause, not the symptom. Work from the evidence in the failed run, one step at a time.

## Step 1: Get the evidence

Ask for what is missing:
- The exact error message and which step failed.
- The input that step received and what it was expected to output.
- Whether it ever worked, and what changed since (app update, new credential, new data shape).
- For n8n, the workflow JSON; for Node-RED, the flow JSON; for other tools, a screenshot or export of the failing step.

Where to look:

| Tool | Where the evidence is |
|---|---|
| n8n | Executions list → open the failed run → click the red node to see input and output |
| Activepieces | Runs → the failed run → the failed step's input and output |
| Node-RED | Debug sidebar; add `debug` nodes before and after the suspect node |
| Windmill | Runs page → job logs and result |
| Huginn | The agent's Events and Logs, and its "last error" |
| GitHub Actions | Actions tab → failed job → the step's log |

## Step 2: Match the symptom

| Symptom | Usual causes |
|---|---|
| Never triggers | Workflow not active or published; webhook test URL used in production; schedule time zone wrong; calendar or app trigger lost its auth |
| Step errors 401 or 403 | Expired token, missing scope, credential attached to the wrong account |
| Empty output | Filter or IF too strict; field name changed; webhook data read from `$json.field` instead of `$json.body.field` (n8n) |
| Expression error | Referenced node renamed; field missing on some items; wrong item linking |
| Runs twice | Sender retried because the webhook answered slowly; two triggers on the same event; overlapping schedules |
| Works in test, fails live | Different data shape in production; test used pinned or sample data |
| Times out or crashes | Too many items in one run, huge files, an endless loop, low server memory |

## Step 3: Fix and prove it

1. Reproduce with the smallest input that fails.
2. Change one thing at a time, then re-run that step.
3. Add a guard so it cannot happen silently again: a default value, a check for empty data, an error alert.
4. Run one full real example end to end before calling it fixed.

## Deliver

A short report: the cause in one sentence, the evidence that shows it, the exact change (new expression, setting or node), and the guard added. If the evidence is not enough to be sure, say what else to collect instead of guessing.
