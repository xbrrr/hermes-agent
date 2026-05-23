# Agentic Stack Topic Deprecation + Multi-Topic MM/Bud Migration

Use this reference when Mikhail wants to remove/deprecate Telegram forum topics such as `MM+Bud / topic 642` or `MM Only / topic 723`, or when moving Hermes↔Bud coordination from one central topic into every domain topic.

## Current approved direction

- Keep domain topics active: `259 Perplex`, `584 Summarize`, `21 Music`, `488 HR`.
- No separate CFO topic currently exists; CFO context belongs inside `Analyst / topic 4`.
- Universal flow for active Agentic Stack topics:
  - Mikhail's ordinary messages go to Hermes/MM first.
  - Bud answers Mikhail only on explicit `@iq5000_bot` tag, direct Bud DM, or replies to Bud's own messages.
  - Hermes may delegate Bud in the same domain topic.
  - MM↔Bud communication stays visible to Mikhail in the topic where the task lives, but human-level: essence, actions, conclusions, hypotheses, proposals; avoid raw parameters unless needed.
  - Hermes/MM normally owns the final user-facing answer unless Mikhail explicitly addresses Bud.
- DM routing rule:
  - Mikhail may use DM with Hermes or Bud for private/preliminary/task-intake messages.
  - If Mikhail asks in DM to bring a task out for discussion, Hermes or Bud should choose the most appropriate subject topic by meaning and move the discussion there. Do not ask for topic choice unless genuinely ambiguous or sensitive; rules can be corrected iteratively.
  - Private TODO / Hermes-only remains in Mikhail↔Hermes DM; Bud-specific private intake can happen in Bud DM, but work that needs shared discussion moves to a subject topic.
- Topic lifecycle:
  - `723 MM Only` is confirmed for removal: no new reports, cron delivery, delegation, or routine work should target it; archive/delete after live delivery/queue dependencies are verified clear.
  - `642 MM+Bud` is only temporary migration/control-room until final smoke; not a routine report or new work catch-all.

## Why 642/723 are deprecated

- `642 MM+Bud` should no longer be the only execution/coordination center. Delegation belongs in the same topic as the task so context, discussion, and final answer remain together.
- `723 MM Only` is replaceable by direct messages to `@ceo5000_bot` for private/strategic Hermes-only communication.
- Both may remain as migration anchors/control-room lanes until dependencies are removed.

## Do not delete topics immediately

Before telling the user to delete/archive Telegram topics, run or request a read-only dependency audit. Deleting too early can break cron delivery, board/watchdog/queue logic, outbound logging, router audits, and historical correlation IDs.

Known dependency classes to audit:

- Cron jobs / delivery mappings with `thread_id=642` or `thread_id=723`.
- Scripts/helpers with hardcoded topic scope:
  - `agent_board.py`
  - `outbound_task_logger.py`
  - `append_chat_event.py`
  - `bot_to_bot_watchdog.py`
  - `agent_queue.py`
  - `router_audit.py`
  - validators/DoD scripts such as `validate_chats.py` and `stack_goal_dod.py`
- Event/history stores:
  - `chat-events.jsonl`
  - `agent-queue.jsonl`
  - watchdog reports
  - routing decisions
  - board/decision stores
- OpenClaw/Bud topic config: ensure every active topic needing explicit policy has one, not just wildcard routing.
- Docs/skills/memory references that still call 642 the only coordination scope or 723 the active Hermes-only lane.

## Typical blocker examples

- `642`: active daily TODO reminder still delivered to `thread_id=642`.
- `723`: weekly harness health check still delivered to `thread_id=723`.
- `642`: board/watchdog/queue/outbound logger/router audit default or hardcoded scope.
- Historical data: old correlation IDs remain readable only through 642-scoped event stores.

## Safe migration plan

1. Confirm target destinations with Mikhail:
   - daily TODO reminder: default recommendation is DM Mikhail, unless a public management/TODO topic is desired.
   - weekly harness health check: default recommendation is `Server-doctor / topic 1346` for ops/runtime audits, or DM if reports should stay private.
2. Prepare a mapping: old 642/723 job/script/reference → new target or multi-topic behavior.
3. Prepare patch set but do not apply until approved.
4. Migrate cron delivery first.
5. Convert hardcoded `642` scripts to explicit topic ID / active-topic allowlist / per-topic queue behavior.
6. Update docs/status from `deprecation_pending` to `archived` only after runtime is migrated.
7. Preserve old 642/723 correlation/history as history-only, not active workflow state.
8. Only after green smoke should the user archive/delete Telegram topics.

## Smoke checklist

Run smoke in 2–3 domain topics, typically `584 Summarize`, `488 HR`, and `1346 Server-doctor`:

- Mikhail writes without tags → Hermes/MM answers.
- Hermes delegates Bud in the same topic → Bud replies in that topic → Hermes gives final.
- Mikhail replies to Bud → Bud answers, Hermes stays silent.
- Mikhail tags Hermes in a Bud thread → Hermes may enter/comment.
- Board/task history records the correct `topic_id`.
- Watchdog does not wait for ACK in 642 for tasks from other topics.
- Cron delivery goes to the new target, not 642/723.
- Old 642 correlation IDs remain readable as history-only.

## Visibility/context pitfall

A public Bud reply may exist in Telegram and in event logs but not be present in Hermes' immediate conversation context. Before calling it an execution failure, inspect event logs or ask for a status ACK. If logs show Bud replied, classify it as a visibility/context gap, not a Hermes→Bud routing failure.

## Reporting style

For Mikhail, report in short Russian manager style. If the message is addressed to him, prioritize:

- essence only;
- humanitarian/non-technical wording first;
- management framing: decision, impact, risk removed, remaining decision/action;
- no ritual validation, no technical prose dump unless he explicitly asks.

For topic deprecation/status questions, use:

- verdict first (`can delete now` / `cannot delete yet`);
- what is already fixed/recorded;
- blockers or remaining verification;
- exact approval/action needed from Mikhail.

Avoid long code/file lists in the user-facing answer. Keep technical detail in internal notes, references, or only provide it on request.
