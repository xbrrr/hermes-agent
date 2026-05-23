# Telegram bot-to-bot outbound logging for watchdog visibility

Context: Agentic Stack topic 642 uses public Hermes → Bud handoffs like `/task@iq5000_bot correlation_id=...` and passive watchdogs that scan `chat-events.jsonl` for missing Bud ACKs.

## Durable lesson

A passive watchdog cannot prove Hermes tasks were acknowledged unless Hermes-originated outbound task messages are logged into the same event log as inbound topic messages. If outbound sends are not logged, the watchdog reports `checked_tasks=0` / `no_hermes_task_events_seen`, which is a logging-visibility gap, not evidence that no tasks were sent.

## Safe minimal pattern

1. Send the public task normally and capture the returned Telegram `message_id`.
2. Append a synthetic outbound event to the topic-scoped `chat-events.jsonl` with:
   - `platform=telegram`
   - `chat_id`
   - `topic_id`
   - `message_id` from the successful send
   - `from_agent=hermes`
   - `from_username=@ceo5000_bot`
   - exact public task `text`
   - `ts`
   - `raw_summary.source=hermes.telegram.outbound_task_logger`
3. Re-run the passive watchdog. Expected change:
   - before logging: `checked_tasks=0`, warning like `no_hermes_task_events_seen`
   - after logging: `checked_tasks>=1`, `matched_acks` or `missing_acks` reflects reality

## Guardrails

- Keep the first implementation passive: no Telegram sends from the logger/watchdog, no routing/enforcement changes, no SQLite board.
- Make the logger idempotent: detect duplicate `(platform, chat_id, topic_id, message_id, correlation_id)` and skip unless explicitly forced.
- Use the exact public text that was sent; do not reconstruct a shortened version, because correlation IDs and acceptance criteria are part of the audit trail.
- Distinguish approval ACKs from completion ACKs before treating duplicate ACKs as errors. A workflow may legitimately produce both `approved=yes` and `status=completed` for one correlation ID.

## Verification commands used in the session

```bash
python3 /path/to/outbound_task_logger.py --self-test
python3 -m py_compile /path/to/outbound_task_logger.py
python3 /path/to/outbound_task_logger.py --message-id <telegram_message_id> --text-file <sent_task.txt>
python3 /path/to/bot_to_bot_watchdog.py --timeout-seconds 600 --dry-run
```

The acceptance signal is that the watchdog sees at least one checked task and no longer emits the outbound-visibility warning for the logged handoff.
