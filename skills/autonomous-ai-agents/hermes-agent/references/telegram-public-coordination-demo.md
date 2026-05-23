# Telegram public agent-agent coordination demo

Use this when the user asks to *show* Hermes coordinating with another bot/agent in a Telegram topic while keeping agent-agent messages visible.

## Context

In Agentic Stack topic 642, Hermes (`@ceo5000_bot`) is coordinator/default responder and Bud/OpenClaw (`@iq5000_bot`) is executor. The user wants Hermes↔Bud coordination to be visible in the topic by default; private bridge/queue-only coordination is not sufficient unless explicitly requested.

## Recommended pattern

1. Send a public Telegram handoff to the topic using a command-style mention that is more reliable than a plain mention:

   ```text
   /task@iq5000_bot correlation_id=<id> max_hops=2
   Bud, <task/request>...
   ```

2. Include loop guards in the visible message:
   - `correlation_id=<stable-id>`
   - `max_hops=<small-number>`
   - Direct addressee (`Bud`, `@iq5000_bot`, or command-qualified target)
   - Clear role boundary: Hermes coordinates, Bud executes/opines.

3. If a shared local workspace exists (for this setup: `/Users/xbr/.agentic-stack/`), also append a durable queue record as fallback/source of truth, but do **not** treat that private/local queue as satisfying the user's visibility requirement.

4. After sending, report concrete evidence back to the user:
   - Telegram target/topic
   - sent `message_id` if available
   - `correlation_id`
   - local queue/task id if created
   - short summary of the handoff content

## Architecture discussion defaults for Mac mini shared-agent setup

For Hermes + Bud/OpenClaw on the same Mac mini, recommend this order unless the user specifies otherwise:

1. **Router/event log first** — topic-scoped routing source of truth: reply-to, explicit mention, default responder, fallback, dedupe by `message_id`.
2. **Durable queue/board second** — SQLite/Kanban-style state machine: `pending → claimed → heartbeat → completed/failed`.
3. **Watchdog third** — monitor gateway/agent liveness, Telegram connectivity, stuck queue items, stale heartbeats.
4. **Profile/process isolation fourth** — separate profiles/configs/logs/sessions and supervised restarts via launchd/system service.

## Pitfalls

- A plain public `@other_bot` mention may not wake another Telegram bot reliably. Prefer `/command@OtherBot` plus local/API bridge fallback.
- Do not hide coordination in a private bridge when the user asked to demonstrate bot-to-bot communication publicly.
- Do not let autonomous bot↔bot replies recurse: always include correlation IDs, hop limits, sender checks, and dedupe.
- Scope rules to the exact chat/topic; do not generalize Agentic Stack topic 642 rules to other topics.
