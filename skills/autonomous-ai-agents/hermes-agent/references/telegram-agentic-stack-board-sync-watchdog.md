# Telegram Agentic Stack: board sync + watchdog lessons

Scope learned from Agentic Stack topic 642 (`chat_id=-1003772186616`, `topic_id=642`) while coordinating Hermes/MM (`@ceo5000_bot`) and Bud/OpenClaw (`@iq5000_bot`).

## Workflow correction: do not pause for Mikhail approval after Bud approves

For this topic, Mikhail granted carte blanche: Hermes coordinates, Bud reviews/approves, and if Bud replies `approved=yes`, the next scoped step should proceed without asking Mikhail again. If Hermes stops at “next logical step” instead of executing, that is a workflow failure. Continue with a small reversible task and report back.

## Public task handoffs must go through a logged outbound path

If Hermes writes a public `/task@iq5000_bot correlation_id=...` as ordinary final response text, it may be visible in Telegram but not pass through the `send_message` tool outbound logger, so `chat-events.jsonl` may only contain Bud ACK rows. That creates watchdog warnings such as `ack_without_logged_chat_task`.

Preferred pattern for auditable Hermes → Bud tasks:

1. Send the public task via `send_message(target='telegram:-1003772186616:642', message='...')` or another explicitly logged outbound path.
2. Verify the send result includes a Telegram `message_id`.
3. Verify `chat-events.jsonl` contains a synthetic Hermes outbound row:
   - `from_agent=hermes`
   - `from_username=@ceo5000_bot`
   - `raw_summary.source=hermes.telegram.outbound_task_logger`
   - exact `/task@iq5000_bot ... correlation_id=...` text
4. Run `agent_board.py sync --events chat-events.jsonl`.
5. Confirm `agent-board.sqlite3` has the task row and then Bud ACK/status updates it.

## Minimal safe board sync pattern

A reversible/minimal step is to attach board sync to existing logging helpers rather than daemonizing immediately:

- `outbound_task_logger.py` runs `agent_board.py sync` after a Hermes outbound `/task@iq5000_bot` event is appended.
- `append_chat_event.py` runs `agent_board.py sync` after scoped inbound events are appended.
- Sync should be fail-open: event append still succeeds if board sync fails, and the sync error is surfaced in helper JSON output.
- Helpers must not send Telegram, change routing/enforcement, touch topic 723, or store secrets.

## Watchdog consistency checks

A passive watchdog can compare `chat-events.jsonl` and `agent-board.sqlite3`:

- `missing_board_tasks`: Hermes task in chat log but no board task.
- `board_without_chat_tasks`: board task exists without matching chat task; warning, not fatal.
- `ack_without_logged_chat_task`: Bud ACK exists but Hermes task row is absent in chat log; often means the task was sent via final-response path instead of logged `send_message` path.
- `completed_ack_board_not_completed`: Bud completion ACK exists but board status is not `completed`; error.

Keep this report-only. Do not auto-fix board rows or send Telegram from watchdog.

## Status parsing pitfall

Bud may combine fields in one line, e.g.:

```text
ACK correlation_id=... approved=yes status=completed
```

When syncing board status, terminal statuses (`status=completed`, `status=blocked`, `approved=no`) must be evaluated before plain `approved=yes`; otherwise completed tasks can get stuck in `approved`.

## Verification checklist

- `python3 -m py_compile` for changed Python files.
- `agent_board.py --self-test`.
- `bot_to_bot_watchdog.py --self-test`.
- `agent_board.py sync --events /Users/xbr/.agentic-stack/chat-events.jsonl` twice; counts should be stable/idempotent.
- `bot_to_bot_watchdog.py --timeout-seconds 600 --dry-run` should show no `missing_acks`; investigate new `ack_without_logged_chat_task` warnings for recent tasks.
