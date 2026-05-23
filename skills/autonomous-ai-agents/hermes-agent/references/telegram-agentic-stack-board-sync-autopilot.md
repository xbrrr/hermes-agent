# Agentic Stack topic 642: board sync autopilot and review pitfalls

Context: Telegram group `Agentic Stack`, topic/thread `642`, Hermes/MM (`@ceo5000_bot`) as coordinator and Bud/OpenClaw (`@iq5000_bot`) as executor.

## Stack-level goal framing

Do not frame topic `642` and topic `723` as the whole Agentic Stack. They are the first explicitly registered lanes in a broader topic-scoped system:

- every Telegram topic/thread can have its own lane policy;
- `642` is the public Hermes↔Bud coordination lane;
- `723` is a Hermes-only lane where Bud stays silent unless work is explicitly delegated elsewhere;
- all other existing/future topics use a safe default until explicitly registered: no inherited `642` loop, no automatic Bud involvement, no global routing/enforcement change;
- board/watchdog are shared passive audit layers and must be topic-aware, not global policy engines.

When asking for approval on a broad agent-stack goal, make the implementation scope explicit: “first production scope is topic `642`; other topics are protected by safe default.” If Mikhail grants carte blanche for that goal, continue autonomously inside the stated guardrails instead of repeatedly asking for small-step approval.

## Workflow lesson

When Mikhail has already given carte blanche and the local rule says “if Bud approves, proceed without asking Mikhail again”, Hermes must not stop at a phrasing like “next logical step”. Treat that as an execution cue:

1. Send a scoped public `/task@iq5000_bot correlation_id=...` handoff.
2. Wait for/inspect Bud `ACK ... approved=yes|no`.
3. If approved, continue execution/review without another Mikhail approval.
4. Verify artifacts and report concise result to Mikhail.
5. After the agreed goal is reached, run the promised triple verification before declaring done: static/code check, self-test/smoke, and live/log/board consistency check.

If the user asks “are you waiting for my approval?” in this context, answer directly that Hermes should not have waited, then continue/verify the step. If the user asks “why didn’t you continue?”, acknowledge the miss, restate the active guardrails, and immediately resume via the logged public handoff path.

## Minimal board auto-sync pattern

For the topic-642 board lifecycle, the safe minimal auto-run step is not a daemon first. Use fail-open hooks in existing logging helpers:

- `outbound_task_logger.py` runs `agent_board.py sync` after a Hermes outbound `/task@iq5000_bot correlation_id=...` event is appended.
- `append_chat_event.py` runs `agent_board.py sync` after a scoped inbound chat event is appended, so Bud ACK/status messages update the board.
- The sync helper must never send Telegram messages and must not change routing/enforcement.
- Fail-open behavior: if SQLite sync fails, the chat event append still succeeds and the helper JSON reports the sync error.

Verification pattern:

```bash
python3 -m py_compile /Users/xbr/.agentic-stack/agent_board.py /Users/xbr/.agentic-stack/append_chat_event.py /Users/xbr/.agentic-stack/outbound_task_logger.py
python3 /Users/xbr/.agentic-stack/agent_board.py --self-test
python3 /Users/xbr/.agentic-stack/outbound_task_logger.py --self-test
python3 /Users/xbr/.agentic-stack/agent_board.py sync --events /Users/xbr/.agentic-stack/chat-events.jsonl
python3 /Users/xbr/.agentic-stack/agent_board.py show --correlation-id <cid>
```

## Review pitfall: combined approval + terminal status

Bud may answer in one line:

```text
ACK correlation_id=<cid> approved=yes status=completed
```

A board sync parser must treat terminal statuses (`completed`, `blocked`, `failed`, etc.) as higher priority than plain `approved=yes`; otherwise finished tasks can stay stuck in `approved`.

Recommended parse order in `apply_ack_event`-style logic:

1. terminal completion statuses (`status=completed`, `done`, `smoke_ack`);
2. blocked/failed/`approved=no`;
3. plain `approved=yes`;
4. record-only ACK.

Self-tests should include a combined `approved=yes status=completed` fixture, not only separate ACK and completion messages.
