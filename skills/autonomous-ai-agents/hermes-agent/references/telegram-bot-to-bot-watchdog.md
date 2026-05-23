# Telegram bot-to-bot handoff watchdog pattern

Use this when a Telegram topic has a visible coordinator/executor workflow (for example Hermes proposes work and Bud/OpenClaw executes) and the user wants public agent-agent coordination to be auditable.

## Durable pattern

1. Keep the watchdog passive: local log scan only. It must not send Telegram messages, trigger agents, change routing, or enforce suppression.
2. Scope by platform + chat id + topic/thread id. Telegram forum topics are separate coordination lanes.
3. Match handoffs by explicit `correlation_id=...`, not by fuzzy message text.
4. Require a visible executor ACK format, for example:
   - approval: `ACK correlation_id=<id> hops=1 max_hops=2 approved=yes|no`
   - completion: `ACK correlation_id=<id> hops=1 max_hops=2 status=completed|blocked`
5. Write machine-readable JSON/JSONL output: `checked_tasks`, `matched_acks`, `missing_acks`, `pending_young_tasks`, `duplicate_acks`, `malformed_tasks`, `warnings`, `scope`, `timeout_seconds`, `ts`.
6. Include a `--self-test` with fixtures for: matching ACK, old missing ACK, young pending task, wrong topic ignored, malformed missing correlation_id, duplicate ACKs, and file-read/report behavior.
7. Verify with both `python -m py_compile` and a dry-run against current logs.

## Key pitfall: outbound coordinator messages

A watchdog that only scans inbound gateway events cannot detect missing ACKs for coordinator-originated tasks unless the coordinator's outbound `/task@OtherBot correlation_id=...` messages are also logged. When Hermes sends a public task to another bot, add a synthetic/outbound event to the same event log with at least:

- `platform`
- `chat_id`
- `topic_id` / thread id
- `message_id` returned by the send call
- `from_agent=hermes`
- `from_username=@ceo5000_bot` (or the coordinator bot username)
- `text`
- `ts`

For Hermes `send_message` based handoffs, verify the delivery result exposes evidence that the outbound event was logged (for example an `agentic_stack_logged`/equivalent success flag, or a fresh matching JSONL line with the returned `message_id`). Do not assume a public send automatically reached the watchdog unless this logging evidence exists.

Do this before treating the watchdog as production-quality. Otherwise dry-runs may show `checked_tasks=0` and `warnings=["no_hermes_task_events_seen"]` even though public handoffs happened.

## Duplicate ACKs are not always errors

In proposal→approval→implementation workflows, two ACK-like messages for one correlation id may be legitimate: one approval ACK and one completion ACK. A v1 watchdog can report duplicates as a warning, but a better version should classify ACK type (`approved=...`, `status=...`) before treating duplicates as suspicious.

## Acceptance summary template

When reporting to the user, keep it practical:

- Changed files
- Self-test output
- Compile result
- Dry-run result
- Whether acceptance is complete or blocked by logging visibility
- Risks / next smallest fix
