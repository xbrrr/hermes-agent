# Agentic Stack local TODO reminder format

Use this when Mikhail asks to transform a raw TODO/reminder list into a clearer project/time-management format, especially for Agentic Stack cron reminders.

## Preferred shape

Keep the source file human-editable Markdown, but make each open task operational:

- `Status`: pending / in_progress / waiting / done
- `Priority`: `P1` blocks money/access/agents or a critical system; `P2` important after P1; `P3` backlog/later
- `Lane`: `Next`, `Waiting`, `Scheduled`, or `Later`
- `Owner`: who owns decision vs execution, e.g. `Mikhail decision; Hermes coordinates; Bud executes`
- `Review`: when it should resurface, in MSK for Mikhail-facing reminders
- `Timebox`: small enough to prevent an endless tail
- `Outcome`: bullets describing done-state
- `Next action`: exactly one concrete next step
- `Notes` / `Blocker`: only if useful; do not store secrets

## Reminder output

Daily reminder should be concise and manager-style:

1. Start with the schedule/time context: `Ежедневный TODO — 11:00 MSK`.
2. State the operating principle: max 3 focus items, one next action, timebox required.
3. Show `Фокус дня` with the top 3 tasks sorted by priority.
4. For each task include only: priority, title, status, lane/review/timebox/owner/next; include decision/blocker only if it changes the user's next step.
5. Put anything else into `Backlog / позже`, not into the main focus.
6. End with the escalation rule: if no movement after the timebox, record blocker and reduce the task to one decision/request.

## Workflow guardrails

- If the task requires purchase/payment/account credentials (for example buying Claude), do not perform external payment or store secrets. Track it as a human decision/purchase step, then route setup/smoke test after approval.
- For Claude access, distinguish account paths: Claude Code subscription/OAuth for coding executor work vs Anthropic API/OpenRouter Claude for Hermes provider/model usage. Subscriptions do not pay API/OpenRouter usage.
- If a cron job reads the TODO file, update both the Markdown source and the reminder script/output parser, then run a smoke test of the script before reporting done.
- Keep final Telegram reply terse: what changed, files touched, smoke result, and the user's next decision.