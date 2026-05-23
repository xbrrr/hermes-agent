# Subconscious finish-plan review pattern — 2026-05-21

Session-specific detail for Agentic Stack topic `1347 / Subconscious` after Mikhail corrected that the report lacked next steps and asked for a weekly "consciousness" report.

## Trigger

Use this when Mikhail asks to continue the Subconscious plan "до конца", asks for status across today's Subconscious thread, or complains that next steps / autonomy impact were not proposed.

## User-facing expectation

- Answer in Russian, manager-to-manager, 3–6 bullets where possible.
- Start with the conclusion: completed / blocked / pending external ACK.
- Always include an explicit `Следующий шаг` or `Что дальше`, not just what was done.
- For weekly consciousness reports include:
  - what was reflected/checked in background;
  - what improved;
  - autonomy / interaction-efficiency impact;
  - what to do next;
  - quality metrics.
- Distinguish Hermes-local completion from external Bud review/ACK. Do not call the whole branch fully closed if Bud review is still pending.

## Implementation pattern that worked

1. Keep scope to local Subconscious memory/recall/reporting in topic 1347.
2. Do not touch runtime/gateway/routing/restart/canary/provider switch from this lane.
3. Add hard-negative recall probes, not only positive recall smoke.
4. Add a weekly consciousness report command/script that stays concise (<40 lines) and includes required manager blocks.
5. Wire weekly cron as `no_agent` script delivery to topic 1347.
6. Verify with py_compile, unit tests, self-test/doctor, quality probes, hard-negative probes, and a direct weekly report smoke.
7. Ask Bud publicly for review with a correlation ID, but report pending ACK separately if it has not arrived.
8. If Bud does not answer, do not stop at “pending” or rely only on a watcher. Treat it as part of the goal: inspect `chat-events.jsonl` and `agent_board.py` for the task row, verify the wake format, and re-send with an explicit visible mention if needed.
9. Preferred wake format for this topic when a public Bud response is required: `@iq5000_bot /task correlation_id=... hops=0 max_hops=...`. The older `/task@iq5000_bot ...` may be logged/boarded but not reliably wake Bud in every path; explicit mention fixed the finish-plan review.
10. After Bud replies, mark both the explicit review correlation and the parent finish-plan correlation completed on the board, then verify no pending topic-1347 tasks remain.

## Known-good local commands from this session

```bash
cd /Users/xbr/.agentic-stack
python3 subconscious_memory.py quality-probes --topic-id 1347
python3 subconscious_memory.py recall-hard-negatives --topic-id 1347
python3 subconscious_memory.py weekly-consciousness-report --topic-id 1347
python3 /Users/xbr/.hermes/scripts/subconscious_weekly_consciousness_report.py
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

Observed green state in this session:

- unit tests: 12 passed;
- quality probes: 9/9;
- hard-negative probes: 4/4;
- weekly report: ok, 27 lines;
- cron `subconscious-weekly-consciousness-report`: enabled, `no_agent`, delivery to topic 1347.

## Bud non-response incident from this session

Root cause pattern:

- Hermes treated missing Bud ACK as an external pending tail instead of diagnosing it as a possible wake/routing failure.
- The original review request used `/task@iq5000_bot ...`; the task existed on the board as pending, but Bud had not replied.
- Re-sending visibly as `@iq5000_bot /task correlation_id=subconscious-finish-plan-review-explicit-20260521 ...` woke Bud immediately.
- Board parser originally only matched `/task@iq5000_bot`; patching the task regex to also match `@iq5000_bot /task` made the reliable wake format auditable:
  - from: `(^|\s)/task@iq5000_bot\b`
  - to: `(^|\s)(/task@iq5000_bot\b|@iq5000_bot\s+/task\b)`
- Add/keep a self-test fixture for the explicit mention format so this does not regress.
- Completion verification: `python3 agent_board.py --topic-id 1347 list --status pending` should return zero pending tasks after Bud review is marked complete.

User-facing correction:

- If Mikhail asks “why is Bud not answering / why didn't you investigate,” acknowledge the workflow mistake directly, then immediately diagnose and fix the wake path. Do not defend the watcher-only approach.
- Concise Russian final shape: cause → fixed action → Bud verdict → board status → remaining risk/next step.

## Pitfalls

- Do not answer "all tasks complete" without checking today's topic transcript/logs and current TODO state.
- If only Hermes implementation is done but Bud review is pending, say: "по моей стороне закрыто; внешний хвост — Bud ACK/review".
- Do not bury the next action under implementation details; Mikhail explicitly corrected this.
- Do not leave a public Bud handoff at “watcher active” when the user granted a full goal/DoD. A missing ACK is itself a diagnostic work item: check task event, board status, wake format, Bud visibility, and either fix/retry or name the exact Server-doctor blocker.
