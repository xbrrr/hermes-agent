# Agentic Stack Telegram TODO MVP implementation notes

Implementation lessons for a Telegram-native TODO/control-panel topic.

## Durable data model

Store Telegram cards as UI, not the source of truth. The durable DB should include at least:

- `id`, `title`, `priority`, `status`, `stage`, `responsible`;
- `context`, `next_step`, `review_at`, `time_limit`, `result`;
- source scope: `source_platform`, `source_chat_id`, `source_thread_id`, `source_message_id`;
- UI linkage: `panel_message_id`, `reply_to_message_id`;
- events/audit table for created/started/blocked/closed/priority/assigned/history actions.

## Command behavior

- `/task <text>` creates a card from text.
- Reply + `/task` creates a card using the replied message as context.
- `/done <id>` closes by explicit id.
- Reply + `/done` must close the card linked to either the panel message or the original source message; store both `source_message_id` and `panel_message_id` to make this reliable.
- `/tasks`, `/mine`, `/stale` should be query-only and should not enter the LLM loop.

## Callback behavior

- Parse callback data narrowly, e.g. `tp:<action>:<task_id>`.
- Before applying any callback, verify task scope matches the current Telegram chat/topic; reject out-of-scope clicks rather than mutating the DB.
- Run SQLite operations from Telegram callback handlers through `asyncio.to_thread(...)` or equivalent so button clicks do not block the event loop.
- Update the Telegram card after mutation and remove/keep keyboard according to status.
- Treat inline buttons as **human UI**, not the agent control plane. Agents should be able to create, assign, reprioritize, start, block, close, and update tasks through backend/API/DB/command handlers and then refresh the Telegram card. Do not imply that Mikhail must click buttons for agent-owned work to advance.
- Do not try to simulate a Telegram user's button click through the Bot API; callbacks are produced by real Telegram clients. If true user-click automation is requested, treat MTProto/userbot as a separate sensitive personal-account integration and start read-only/draft-mode first.

## Rollout verification

- Code smoke: py_compile changed modules.
- Targeted tests: command registry, Telegram command routing, task-panel model, send-message/logging side effects if touched.
- Local post-restart smoke can use a temp DB: create task → parse/apply callback → close with `/done` by reply id.
- Live acceptance for inline buttons is only complete after a real Telegram button click (or a production-shaped callback update fixture), not just direct function calls.
- For live button acceptance without making the user manage the whole test, create one disposable Telegram card, record its `panel_message_id`, and attach a short-lived watcher over `task_events` that reports only when a non-creation callback event arrives. Phrase this as optional UI acceptance, not as a blocker for agent-side task management.
