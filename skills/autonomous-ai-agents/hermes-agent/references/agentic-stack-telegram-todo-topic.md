# Agentic Stack Telegram TODO topic / task-manager pattern

Use this reference when designing or implementing a dedicated Telegram TODO/Tasks topic for Agentic Stack.

## Product principle

The TODO topic should be an **index/control panel**, not the place where all work moves.

- Subject discussion/execution stays in the matching topic: Web Admin, Coding, Server-doctor, Subconscious, Picasso, etc.
- TODO/Tasks stores task cards, ownership, status, priority, stale/blocker state, and links back to source context.
- If TODO becomes the place where work is discussed, it turns into another catch-all and loses the benefit.

## Recommended MVP

Create a dedicated Telegram forum topic named `TODO`, `Tasks`, or similar.

A task can be created from any topic by command or by replying to a message. The task card is posted/updated in TODO and links back to the original chat/topic/message.

Minimal card shape, in Russian for user-facing reports:

```text
#A42 — Сделать task-manager для Agentic Stack

Приоритет: P1
Статус: Триаж
Этап: Концепция → MVP
Ответственный: Hermes / Bud / Mikhail
Контекст: Web Admin, исходное сообщение
Пересмотр: сегодня 18:00 MSK
Лимит времени: 1 день
Результат: концепция + MVP-план
Следующий шаг: выбрать реализацию — встроить в Hermes или отдельный bot/helper
```

Do not create cards without exactly one practical `Следующий шаг`; otherwise the task is not actionable.

## Minimal statuses

Keep the state machine small:

- `Триаж` — captured, not yet accepted.
- `Очередь` — accepted, waiting for slot/owner.
- `В работе` — someone is actively executing.
- `Блокер` — needs human/access/decision.
- `На проверке` — an agent reported completion; Hermes/human must verify.
- `Закрыто`
- `Отменено`

## Inline buttons

Telegram inline keyboards are a good fit for quick task operations. Use buttons for transitions, not long command prose.

Suggested card buttons:

- `▶️ В работу`
- `✅ Закрыть`
- `⛔ Блокер`
- `⏰ Пересмотр`
- `🔥 Приоритет`
- `👤 Назначить`
- `🧵 Контекст`
- `📝 История`

Technical note: Hermes Telegram adapter already has callback-query infrastructure for approvals, clarify prompts, and model picker. Reuse the same callback pattern rather than inventing a separate interaction loop.

## Minimal commands

- `/task <text>` — create a task from text.
- Reply to a source message + `/task` — create a task from that message.
- `/tasks` — list open tasks.
- `/mine` — list tasks assigned to the caller/agent.
- `/stale` — list stale tasks.
- Reply to a task card + `/done` — close with result.
- `/triage` — scan recent topic messages and propose candidate tasks for confirmation.

## Durable source of truth

Do not treat Telegram messages as the database. Use SQLite or Hermes Kanban as the durable source; Telegram cards are UI.

Suggested fields:

- `task_id`
- `title`
- `description`
- `status`
- `priority`
- `owner`
- `source_chat_id`
- `source_topic_id`
- `source_message_id`
- `todo_message_id`
- `created_by`
- `updated_at`
- `review_at`
- `external_link`
- append-only `events`

## Digest / watchdog behavior

A periodic digest should be short and management-oriented:

- show P0/P1 first;
- show blockers;
- show tasks without owner;
- show tasks stale for >N hours;
- cap focus items to 3 and put the rest in `Позже`.

Avoid noisy flat backlogs. The goal is to prevent lost open loops, not to produce another report stream.

## Research-backed patterns captured

- Slack triage-channel practice: dedicated triage channels, pinned rules, simple emoji/status conventions, and bot scans for outstanding items.
- GitHub Projects/Issues practice: small label/status vocabulary, assignees, durable issue IDs, audit trail.
- Telegram bot UX: inline keyboards for status/priority/assignee/reminder actions; update a task card in-place where possible; keep longer choice lists paginated or search-based.
- Chat-to-tracker practice: capture source message link/id, maintain mapping to durable issue/task id, and reflect external closure back into chat.

## Recommended rollout

1. **Phase 0 — no code:** create TODO topic, pin rules, use manual cards.
2. **Phase 1 — small helper:** SQLite registry + create/list/show/status/assign/priority/comment/close.
3. **Phase 2 — Telegram callbacks:** inline buttons update SQLite and edit cards.
4. **Phase 3 — watchdog/digest:** stale/blocker/unowned summaries.
5. **Phase 4 — integrations:** GitHub/Linear only for tasks that really need an external tracker.

Recommendation: do not start with GitHub/Linear. Start with Telegram TODO topic + SQLite registry + inline buttons + stale digest.