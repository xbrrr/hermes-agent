# Cron report inventory and delivery audit

Use when Mikhail asks which scheduled reports are planned, already completed, or where they will be delivered.

## Procedure

1. Use `cronjob(action="list")` as the authoritative live scheduler inventory.
2. Check `~/.hermes/cron/jobs.json` only for fields that the compressed cron list may omit, especially `origin.chat_name`, `origin.thread_id`, `deliver`, `last_run_at`, `next_run_at`, and `last_delivery_error`.
3. Check `~/.hermes/cron/output/<job_id>/` for actual outputs created today. Read the newest output file for each relevant job to summarize what was produced.
4. Confirm delivery from `~/.hermes/logs/agent.log` when the user asks whether a report actually arrived. Look for `Job '<id>': delivered to telegram:<chat_id> via live adapter` and include the destination topic if known from `origin`.
5. Convert scheduler-local timestamps to MSK for Mikhail-facing reports. Do not leave raw PDT/UTC-only times unless comparing incident windows.
6. Separate:
   - already completed today;
   - still scheduled today;
   - future/not-today;
   - local-only jobs (`deliver: local`) versus Telegram-delivered jobs.

## Output style for Mikhail

- Russian, terse manager-to-manager.
- Start with current MSK date/time.
- For each report: time MSK, status, one-line purpose, and destination.
- Use Telegram topic names where known: e.g. `Agentic Stack → 1347 / Subconscious`, `642 / MM`, `723 / MM Only`.
- If a job is local-only, say `никуда в Telegram, только локально`.
- Avoid raw cron JSON, file dumps, and long prompts; include paths only when useful for verification.

## Pitfalls

- `deliver: origin` is not enough by itself; inspect `origin` in `jobs.json` to know the chat/topic.
- The scheduler may store local time in PDT on this Mac while the user expects MSK.
- A cron output file proves generation, not delivery. Delivery requires log confirmation or `last_delivery_error == null` plus scheduler status.
- If Mikhail says he “did not see” a standard report, treat that as a delivery/visibility problem, not as a request to re-explain cron internals. Check whether the job was `local`, `[SILENT]`, topic-only, or DM-delivered. For user-facing standard reports that matter operationally, prefer dual delivery (`telegram:<topic>,telegram:Mikhail`) after verifying this matches the report class; leave raw internal collector jobs (`deliver: local`) local.
- Distinguish “ran successfully” from “was visible to Mikhail”: a topic-only delivery can be technically OK but still fail the user expectation when he expects personal visibility. Report both facts directly and, when safe, fix the delivery target immediately.
