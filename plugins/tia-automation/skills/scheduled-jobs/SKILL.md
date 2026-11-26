---
name: scheduled-jobs
description: Set up scheduled and recurring automations with cron expressions, time zones and safe re-runs, including site monitoring and daily or weekly reports. Use when the user wants something to run every day, hour or week, asks for a cron expression, wants to check what a cron schedule means, or has a scheduled job that runs at the wrong time or runs twice.
---

# Scheduled Jobs

A schedule looks simple until daylight saving time, a server in another time zone or a job that runs twice. Get the time right, then make the job safe to re-run.

## Step 1: Write the schedule

Standard cron has five fields:

```
minute  hour  day-of-month  month  day-of-week
0       9     *             *      1-5        → 09:00, Monday to Friday
```

Common patterns:

| Need | Cron |
|---|---|
| Every 15 minutes | `*/15 * * * *` |
| Every day at 07:30 | `30 7 * * *` |
| Every Monday at 09:00 | `0 9 * * 1` |
| First day of each month at 06:00 | `0 6 1 * *` |
| Weekdays, every hour from 09:00 to 17:00 | `0 9-17 * * 1-5` |

- Day-of-week: 0 or 7 is Sunday, 1 is Monday.
- If both day-of-month and day-of-week are set, standard cron runs when **either** matches.
- Some tools (n8n's Schedule Trigger, GitHub Actions, Windmill) have their own forms or a 6-field cron with seconds. Check which one the tool expects.

## Step 2: Check it

If you can run code, confirm the meaning and the next run times:
`python3 scripts/cron_check.py "0 9 * * 1-5" --tz Asia/Dhaka --next 5`

It prints a plain-English description and the next run times in the chosen time zone. Show these to the user before they save the schedule.

## Step 3: Get the time zone right

- Ask for the user's time zone and set it on the workflow or tool, not just the server.
- GitHub Actions schedules run in UTC; convert the time for the user.
- Avoid 01:00 to 03:00 local time where daylight saving applies; those runs can be skipped or doubled.
- Spread heavy jobs away from :00 when many jobs share a server.

## Step 4: Make re-runs safe

- Process "new since last run" by saving the last processed time or ID, not by "last 24 hours" guesses.
- Skip items already handled (check an ID in a sheet or database).
- Add an alert when the job fails or finds zero items for too long.

## Monitoring jobs

For "tell me when this page changes" or "alert me when my site is down", a dedicated tool is often simpler than a workflow: changedetection.io for page changes, Uptime Kuma for uptime, or a Huginn Website Agent. Use a workflow when the alert must trigger further steps.

## Deliver

The cron expression, its plain-English meaning, the next 3 to 5 run times in the user's time zone, where to set it in their tool, and how re-runs are kept safe.
