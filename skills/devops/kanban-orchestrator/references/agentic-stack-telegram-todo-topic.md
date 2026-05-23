# Agentic Stack Telegram TODO topic pattern

Use this reference when designing or reviewing a Telegram-native task/TODO topic for Agentic Stack agents and Mikhail.

## Product shape

- Create a dedicated TODO/tasks topic so tasks do not disappear inside subject threads.
- Keep subject discussion in the relevant topic; the TODO topic is the control plane: intake card, status, priority, owner, review/close actions, and links back to source discussion.
- Prefer buttons for routine lifecycle changes (`ack/start/block/review/done/reopen/priority`) instead of long command messages.
- Support command fallback for text-only flows: `/task`, `/done`, `/block`, `/prio`, `/owner`, ideally working both by explicit task id and by reply to a task card or source message.
- Mikhail-facing reports should be short: conclusion first, 3–6 bullets, facts/tests/next action.

## Minimal durable data model

For each task record, keep both message anchors:

- `source_chat_id`, `source_topic_id`, `source_message_id` — where the task came from.
- `task_chat_id`, `task_topic_id`, `panel_message_id` — the TODO-topic task card/control panel.
- `correlation_id` and/or task id visible in both places.
- `status`, `priority`, `owner`, timestamps, and last actor.

Why: `/done` by reply only works reliably if the bot can map both the original source message and the TODO panel message back to the same task.

## Telegram safety rules

- Callback buttons must scope-check `chat_id` and `topic_id` before mutating a task; do not let a forwarded/copied card or wrong topic callback change state.
- Button handlers should be fast and non-blocking. If persistence is synchronous (SQLite/etc.), run writes off the event loop or through the app's existing DB executor.
- Store message ids after send/edit succeeds; handle failed edit/send as partial state, not as a completed card.
- Distinguish `code accepted`, `runtime loaded`, `button callback smoke`, `/done reply smoke`, and `live rollout accepted`.

## Ready-for-review validation package

Before calling a TODO-topic MVP ready:

1. Separate intended TODO/task-manager diffs from unrelated dirty work.
2. Run syntax/compile checks for changed modules.
3. Run targeted tests for routing, task creation, callback state transitions, and `/done` reply mapping.
4. Manually or with smoke tests verify:
   - `/task` creates a visible card in the TODO topic.
   - Buttons mutate only the intended task in the intended chat/topic.
   - `/done` works when replying to the TODO panel and when replying to the original source message.
   - Out-of-scope topics/chats cannot mutate tasks.
5. If production gateway restart is needed, hand off to `server-doctor`: drain current tasks, restart safely, then smoke `/task` + button + `/done` on the live runtime.

## Routing boundary

- Concept/UX/rules for the TODO topic: product/admin design lane.
- Bot code, DB schema, callback handlers, command parsing: coding lane.
- Gateway restart, smoke, task-drain, rollback: `server-doctor` lane only at rollout time.
