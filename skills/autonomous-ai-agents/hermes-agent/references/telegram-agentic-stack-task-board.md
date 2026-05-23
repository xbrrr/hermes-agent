# Telegram Agentic Stack: public tasks, outbound logging, watchdog, and SQLite board

Use this reference when coordinating Hermes (`@ceo5000_bot`) as planner/reviewer and Bud/OpenClaw (`@iq5000_bot`) as executor in the Agentic Stack Telegram topic.

## Scope from the working setup

- Telegram group: `Agentic Stack`
- Chat ID: `-1003772186616`
- Topic/thread: `642`
- Hermes public task command format:
  - `/task@iq5000_bot correlation_id=<id> hops=0 max_hops=2 ...`
- Bud ACK/report format:
  - `ACK correlation_id=<id> hops=1 max_hops=2 approved=yes|no`
  - completion reports may use `status=completed`

## Public coordination sequence

1. Hermes writes or links a proposal with clear scope, acceptance criteria, allowed actions, and forbidden actions.
2. Hermes posts the public `/task@iq5000_bot ... correlation_id=...` handoff in topic 642.
3. Bud replies publicly with approval/objection before implementation.
4. Bud implements only after approval.
5. Bud reports changed files, commands run, verification output, risks/limitations, and board state if applicable.
6. Hermes verifies locally before accepting the report.

Do not treat a private queue/bridge as sufficient when the user asked for agent-agent coordination to be visible in the topic.

## Guaranteed outbound logging pattern

Problem: a passive bot-to-bot watchdog cannot see Hermes-originated `/task@iq5000_bot correlation_id=...` messages unless Hermes outbound sends are logged into the same event stream as inbound topic events.

Working fix:

- Hook after successful `send_message` when the returned `message_id` is available.
- Scope narrowly:
  - platform: `telegram`
  - chat_id: `-1003772186616`
  - topic_id/thread_id: `642`
  - text contains `/task@iq5000_bot`
  - text contains `correlation_id=`
- Append an idempotent synthetic outbound event to `chat-events.jsonl`.
- Preserve exact public task text and returned `message_id`.
- Do not send Telegram from the logger.
- Do not alter routing/enforcement.
- Ignore topic 723 and all non-scope messages.
- Use this raw summary source contract:
  - `raw_summary.source = "hermes.telegram.outbound_task_logger"`

Recommended smoke checks:

- `logged_once=true`
- duplicate same `message_id + correlation_id` is not appended again
- wrong topic ignored
- source contract equals `hermes.telegram.outbound_task_logger`
- watchdog dry-run reports no missing ACKs for visible completed tasks

If the gateway process may still have old code in memory, restart gateway and run a short live smoke after restart. Important nuance: a gateway restart may not reload the currently-running Hermes agent/tool process that is executing `send_message_tool`. If a smoke event still shows an old `raw_summary.source` value, do not accept the contract yet; finish the current turn or otherwise ensure a fresh agent/tool runtime, then send a follow-up smoke. Pass criterion: the new outbound event has `raw_summary.source = "hermes.telegram.outbound_task_logger"` and the watchdog still reports matched ACKs with `missing_acks=[]`.

## Topic-642 SQLite task board v1 pattern

A narrow stdlib-only board can live under `/Users/xbr/.agentic-stack/`:

- `task_board.py`
- `task-board.sqlite3`

Core lifecycle:

- `pending`
- `claimed`
- `running`
- `completed`
- `failed`
- plus `blocked` / `cancelled` if supported

Minimal CLI verbs:

- `init`
- `create`
- `list`
- `show`
- `claim`
- `heartbeat`
- `complete`
- `fail`
- `--self-test`

All command output should be JSON so Hermes/Bud can parse and quote it in reports.

Important transition rules:

- `create`: creates `pending` task and an event.
- `claim`: only from `pending` or `blocked`; sets `claimed`, increments attempts.
- `heartbeat`: updates heartbeat; from `claimed`, move to `running`.
- `complete`: only from `claimed` or `running`.
- `fail`: only from `claimed` or `running`.
- duplicate `task_id` or `correlation_id`: nonzero exit with JSON error.
- invalid transition: nonzero exit with JSON error.

Self-test should cover schema creation, lifecycle transitions, duplicate rejection, invalid transition rejection, fail path, and append-only events.

## Board lifecycle sync from chat-events

For an integration layer that turns public topic events into SQLite task lifecycle records, prefer a two-pass sync over a single chronological pass:

1. First pass: import all Hermes outbound `/task@iq5000_bot correlation_id=...` events as task records.
2. Second pass: apply Bud ACK/completion messages to existing records.

Reason: real `chat-events.jsonl` may not be strictly causal. Backfill or append timing can place a Bud ACK earlier in the file than the synthetic Hermes outbound task it replies to. A single-pass importer can miss or misclassify those ACKs. The board should be robust to physical log order and key state transitions by `correlation_id` / `reply_to_message_id`, not by assuming line order equals conversational order.

Keep this integration scoped to topic 642 unless the user explicitly approves broader routing. Do not touch topic 723, credentials, or gateway routing/enforcement as part of board sync.

## Hermes review checklist for Bud completion reports

When Bud reports completion, verify independently before accepting:

- Inspect the diff for the reported files.
- Run `py_compile` for changed Python files.
- Run the local self-test/smoke command if provided.
- Query the SQLite board record if board state is part of the task.
- Run watchdog `--dry-run` for bot-to-bot logging tasks.
- Confirm the report’s IDs match the public Telegram messages:
  - `source_message_id`
  - `result_message_id`
  - `correlation_id`

Report acceptance in practical terms: what passed, what remains risky, and the next separate proposal.