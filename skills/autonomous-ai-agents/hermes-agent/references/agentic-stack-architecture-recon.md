# Agentic Stack Architecture Recon Pattern

Use this note when asked to perform read-only architecture reconnaissance of the Hermes/OpenClaw/Telegram coordination stack, especially for the Agentic Stack Telegram group with topic-scoped rules.

## Trigger

- User asks for an autonomous architecture recon/report of Agentic Stack.
- Scope mentions Hermes / OpenClaw / Telegram coordination / memory / skills / cron / background agents / task routing.
- User requires a compact Russian report and forbids deploys, deletes, production config changes, secrets changes, destructive commands, or sending messages manually.

## Safe workflow

1. **Respect delivery semantics.** In cron context, do not call `send_message`; final response is delivered by scheduler. If nothing new, use the exact `[SILENT]` convention only when requested.
2. **Load local context first.** Inspect current repo/cwd, Hermes memories, shared Agentic Stack workspace, cron jobs, gateway logs, and relevant past sessions before using web/docs.
3. **Keep topic scope explicit.** Do not inherit topic-642 rules into topic 723. Treat every rule as scoped by `chat_id` + `topic_id` unless Mikhail explicitly broadens it.
4. **Prefer existing shared source of truth.** For Agentic Stack this is typically `/Users/xbr/.agentic-stack/` with `chats.yaml`, `README.md`, `chat-events.jsonl`, `routing-decisions.jsonl`, `agent-queue.jsonl`, `router_audit.py`, and `agent_queue.py`.
5. **Verify rather than assume.** Run safe read-only checks such as `router_audit.py --self-test`, queue/event-log summaries, `hermes cron list`, `hermes status`, and `openclaw status`. Do not mutate production config.
6. **Look for drift.** Explicitly compare docs vs runtime state, e.g. README rollout phase vs `chats.yaml`, runtime gateway patches vs intended plugin/config design, audit schema vs runtime decision schema.
7. **Create report artifacts only in the approved reports path** when requested, e.g. `/Users/xbr/.hermes/reports/agentic-stack-recon/`, and list absolute paths in the final response.

## What to analyze

- Communication rules: Hermes identity, OpenClaw/Bud identity, Mikhail addressing preferences, reply/mention priority, public/private coordination policy.
- Memory/session recall: topic-scoped durable memories and whether they conflict.
- Shared task/routing source of truth: JSONL/SQLite readiness, schema completeness, dedupe/correlation/hops fields.
- Roles: coordinator, executor, reviewer, watchdog, researcher.
- Background systems: Hermes gateway, OpenClaw gateway/node service, cron jobs, queue processors, watchdog opportunities.
- Risks: silent failures, suppression without executor ACK, routing conflicts, context loss, duplicate replies, over-broad permissions, hardcoded production patches, doc/config drift.

## Recommended report shape

For Mikhail, keep the final in Russian, compact, and decision-oriented:

- Executive summary, 10–15 bullets.
- Current architecture.
- Top risks.
- Top 5 improvements.
- Architecture v2.
- Roadmap: 1 day / 1 week / 1 month.
- Backlog P0/P1/P2 with acceptance criteria.
- Permanent cron/watchdog proposals.
- Tasks suitable for OpenClaw/Bud delegation.
- Created files/artifacts with absolute paths.
- Decisions required from Mikhail.

## Durable lessons from 2026-05-16 recon

- Topic 723 had a separate memory rule: Mikhail communicates only with `@ceo5000_bot`; replies should not tag Mikhail.
- Topic 642 was the active shared-agent workspace and should not be silently treated as equivalent to topic 723.
- `chats.yaml` can drift from `README.md`; this is a first-class architecture risk.
- Runtime gateway patches can drift from class-level architecture; flag hardcoded `gateway/platforms/telegram.py` logic and recommend plugin/config extraction.
- Runtime `routing-decisions.jsonl` schema may be less complete than `router_audit.py` acceptance criteria; report missing fields such as `dedupe_key`, `suppressed_agents`, `correlation_id`, `hops`, and `max_hops`.
- If Hermes soft-suppresses itself for Bud, there must be a watchdog/timeout to avoid silent no-answer failures.
