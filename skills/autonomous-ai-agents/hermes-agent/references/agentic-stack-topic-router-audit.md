# Agentic Stack Topic Router/Event-Log Audit Pattern

Use this when coordinating Hermes with an executor bot in a Telegram forum topic where the user wants public, auditable agent-agent coordination before enabling stronger automation.

## Trigger

- Multi-agent Telegram topic with a coordinator/default responder and executor bot.
- User wants all agent-agent messages visible in the topic.
- Before migrating to SQLite task board, enforcement changes, or autonomous executor work.
- User corrects that a prior summary was not a real bot-to-bot turn because the executor was not explicitly addressed.

## Public workflow

1. Hermes designs/proposes a concrete spec in the shared workspace.
2. Hermes addresses the executor publicly with the topic's reliable protocol, e.g. `/task@iq5000_bot correlation_id=<id> hops=0 max_hops=2`.
3. Executor must publicly ACK and approve/object before implementation, e.g. `ACK correlation_id=<id> hops=1 max_hops=2 approved=yes`.
4. If approved, executor implements and reports changed files + test output publicly.
5. Hermes verifies the artifact independently before reporting success.
6. If Hermes needs human input/approval, explicitly say so and tag the user's actual Telegram username from the topic context (for this setup: `@xbrrr`), not a display-name placeholder.

## Router audit requirements

A passive router-audit helper should be safe and deterministic:

- exact `chat_id` + `topic_id` scope guard;
- no Telegram sends;
- no agent starts;
- no enforcement/suppression changes;
- no SQLite/task-board migration in the same step;
- append-only `routing-decisions.jsonl` output unless `--dry-run` is used;
- stdlib-only is acceptable for a narrow fixed config, but use a proper config parser if rules expand.

Every routing decision should record:

- `intended_agent`;
- `reason`;
- `suppressed_agents`;
- `correlation_id`;
- `reply_to_message_id` and `reply_to_agent`;
- `hops` / `max_hops`;
- `dedupe_key`, preferably `telegram:<chat_id>:<topic_id>:<message_id>|correlation_id:<id-or-none>`;
- `enforced=false` during audit-only phases;
- `phase` for rollout tracking.

## Acceptance checks

A minimal `--self-test` should cover:

1. Untagged user message routes to Hermes/default.
2. Explicit executor mention routes to Bud/executor.
3. Reply to executor routes to executor.
4. Hermes `/task@executor correlation_id=x hops=0 max_hops=2` routes to executor and extracts metadata.
5. Executor `ACK correlation_id=x hops=1 max_hops=2` replying to Hermes routes to Hermes and extracts metadata.
6. Multiple known-agent mentions fall back safely with `ambiguity=multiple_known_agent_mentions`.
7. Wrong chat/topic is rejected.

## Pitfalls

- Do not treat an unaddressed roadmap/summary as a bot-to-bot turn; explicitly address the executor.
- Do not say you are waiting implicitly. State whether waiting on the human or the executor.
- Do not jump from audit directly to SQLite/enforcement until the audit has run long enough to reveal wrong-topic or wrong-agent decisions.
