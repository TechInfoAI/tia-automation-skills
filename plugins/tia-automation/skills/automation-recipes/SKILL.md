---
name: automation-recipes
description: Ready-made automation recipes for marketing, sales, SEO and small-business work, such as lead capture to CRM, new post to social media, weekly Search Console reports, review alerts, invoice follow-ups and uptime alerts. Use when the user asks for automation ideas, wants a template for a common business task, or asks "what can I automate".
---

# Automation Recipes

Start from a proven pattern, then adapt it. Each recipe lists the trigger, the steps and the trap to avoid. Build it with `n8n-workflow-builder` or `flow-builder-other-tools`.

## Sales and leads

| Recipe | Flow | Watch out for |
|---|---|---|
| Lead capture | Form webhook → clean and validate email → create or update CRM contact → Slack or email alert to sales | Duplicates: search the CRM by email before creating |
| Lead scoring | New lead → AI classifier (fit and intent) → tag in CRM → hot leads to a sales channel | Keep a "needs review" label for low-confidence scores |
| Missed follow-up | Daily schedule → CRM deals with no activity for 7 days → reminder to the owner | Respect time zones of the team |

## Marketing and content

| Recipe | Flow | Watch out for |
|---|---|---|
| New post to social | RSS or WordPress new post → AI drafts one caption per network → approval → post | Always keep a human approval step |
| Content calendar | Sheet row marked "ready" → create draft in WordPress → notify editor | Use the row ID to avoid double drafts |
| Newsletter signup | Form → email tool list → welcome email → tag by interest | Double opt-in where the law requires it |

## SEO and websites

| Recipe | Flow | Watch out for |
|---|---|---|
| Weekly Search Console report | Weekly schedule → Search Console API (clicks, impressions, top queries) → sheet → summary email | Data lags by about 2 to 3 days; report on the week before |
| Rank or page change alert | Schedule → check the page or rank tracker API → compare with last value → alert on a real change | Save the previous value so you only alert on change |
| Uptime and SSL alerts | Uptime Kuma or Gatus → webhook → workflow → Slack, Telegram or SMS | Alert after 2 failed checks to avoid noise |
| Broken link check | Weekly schedule → fetch sitemap → check status codes → sheet of 4xx and 5xx | Throttle requests to your own server |

## Operations and admin

| Recipe | Flow | Watch out for |
|---|---|---|
| Invoice follow-up | Daily schedule → unpaid invoices past due date → polite reminder email → log | Stop reminders the moment payment arrives |
| Review alerts | New Google or marketplace review → AI drafts a reply → owner approves → post or save | Never auto-post replies to negative reviews |
| File backup | Schedule → export sheets or database → compress → cloud storage → keep last 30 | Test a restore once |
| Inbox triage | New email → AI classifier → label and route; urgent to Slack | Do not let AI send replies without approval |

## How to adapt a recipe

1. Swap in the user's real apps (their CRM, email tool, chat).
2. Confirm each app has a node or an API (see `api-and-webhooks`).
3. Add the error path and the human approval step where money, customers or public posts are involved.
4. Estimate monthly runs and any paid API or AI costs.

## Deliver

The recipe adapted to the user's apps as a one-line flow, the build steps, the credentials needed and a test plan with one sample input.
