# Agentic Stack nightly runtime improvement loop

Use this reference for scheduled Server-doctor jobs whose goal is continuous small improvements to the Agentic Stack runtime/ops layer, not incident response only.

## Scope

Server-doctor owns:
- OpenClaw/Hermes gateway/runtime process health.
- LaunchAgent/systemd/Docker/cron jobs and safe operational refactors.
- Routing/topic-policy consistency where it affects runtime delivery.
- Board/task handoff tooling, passive parsers, smoke tests, log hygiene, architecture backlog.

Do not absorb Subconscious work: memory/recall/reflection/decision-quality checks belong to the Subconscious topic. Server-doctor may verify only runtime delivery/routing to that topic.

## Minimum loop

1. Baseline without restart:
   - time in MSK, hostname/OS if relevant;
   - gateway status/connectivity;
   - canonical topic files before routing changes: `/Users/xbr/.agentic-stack/chats.yaml` and `/Users/xbr/.openclaw/workspace/chats.md`;
   - board/task parser state if handoffs are involved;
   - recent high-signal logs, but avoid dumping logs in the report.
2. Look for measurable waste:
   - stale topic IDs in cron/job targets;
   - noisy repeated logs;
   - duplicated/manual loops;
   - missing smoke tests or docs;
   - brittle parser/wake formats;
   - runtime config drift such as LaunchAgent PATH/config mismatch.
3. Make only small safe changes:
   - docs/runbooks/backlog entries;
   - passive parser/test/doc fixes;
   - validators or smoke helpers;
   - no live gateway/Hermes/Telegram restart without separate approval, drain, attribution, rollback and smoke plan.
4. Verify with exact current commands, not remembered ones. If a smoke command is absent or CLI flags differ, inspect help and update the report/backlog to the actual command used.
5. Maintain `/Users/xbr/.agentic-stack/architecture-backlog.md` for durable runtime/ops backlog items: finding, next action, expected effect.

## Known good checks from the board/tooling path

- `python3 -m py_compile agent_board.py append_chat_event.py outbound_task_logger.py`
- `python3 agent_board.py --self-test`
- `python3 agent_board.py sync`
- `python3 agent_board.py list`
- `openclaw gateway status`

Current board parser expectations:
- Accept both `/task@iq5000_bot ...` and explicit-mention `@iq5000_bot /task ...` task wake formats.
- Accept Bud completion messages with `correlation_id=... status=completed` even without a literal `ACK` token.
- Treat `malformed_tasks=[]` and `malformed_acks=[]` as parser health signals; pending tasks can still be legitimate open work, not parser failure.

## Reporting style

Russian, concise, manager-readable:
- checked facts;
- inefficiencies found;
- changes made;
- verification result;
- remaining risks;
- next steps with expected effect.

Separate facts from hypotheses. Do not call reading/browsing “thinking”. Do not claim runtime acceptance if only docs/backlog changed.