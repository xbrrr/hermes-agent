# End-to-end verification of scheduled auto-ingest — 2026-05-20

Session pattern: Bud reported `completed` for Subconscious topic 1347. Initial command-level checks were green, but the claim “auto-ingest from chat-events exists” was not true because only the manual CLI path called ingest.

## Failure mode

- Manual command worked: `python3 subconscious_memory.py decision-ingest-events --topic-id 1347`.
- Scheduled entrypoint was LaunchAgent → `python3 subconscious_memory.py reflect`.
- `build_reflection()` read `chat-events.jsonl` and refreshed views, but did **not** call `decision_ingest_events()`.
- Therefore new chat events would not automatically enter decision-state/preflight/report.

## Correct acceptance test

Verify the real path, not just helper commands:

```text
chat-events.jsonl
  → scheduled/reflection entrypoint
  → decision-state rows
  → supersede/idempotency
  → views + manager report
  → preflight
```

A useful synthetic probe:

- write temporary `chat-events.jsonl` with:
  - `/task@iq5000_bot correlation_id=...` in target topic;
  - Bud `ACK correlation_id=... status=completed`;
  - optional event in another topic to prove scoping;
- run the scheduled-equivalent function/command;
- assert first run inserts expected rows;
- assert second run inserts 0;
- assert completion supersedes active next action;
- assert non-target topics are excluded;
- assert report path exists and preflight state reflects the rows.

## Review lesson

When an agent claims “automatic”, ask: automatic through which entrypoint? Then test that exact entrypoint. Green helper tests are insufficient if production/scheduled wiring bypasses the helper.
