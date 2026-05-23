# Telegram agent task ACK triage

Use when a user says an agent task was posted but there is no visible progress.

## Principle

An outbound Telegram task message is only proof that the sender posted it. It is **not** proof that the executor accepted it, especially after stale sockets, transport timeouts, delayed polling, or bot-to-bot routing ambiguity.

## Fast triage

1. Identify the task message id, topic id, chat id, and correlation id.
2. Inspect recent Telegram ingress spool for the executor side:
   - chat id / topic id match;
   - original task message present;
   - executor ACK/progress messages after the task;
   - distinguish Telegram `message.date` from local `receivedAt` because delayed polling can ingest old messages later.
3. Check executor session/trajectory, not only the observer's chat transcript:
   - OpenClaw session key should match `agent:<agent>:telegram:group:<chat_id>:topic:<topic_id>`.
   - `prompt.submitted` proves the executor session was spawned for the Telegram message.
   - `tool.call`/`tool.result` for `message.send` proves whether a public ACK/progress was sent and gives the returned Telegram `messageId`.
   - A stale coordinator/observer view can miss valid executor sends; do not declare `no ACK` until trajectory/tool results are checked.
4. Check gateway logs around the posting window for:
   - `stale-socket`, `auto-restart`, `fetch-timeout`, transport unhealthy/backoff;
   - inbound lines to the executor bot;
   - `telegram-auto-reply` skip reasons such as `reason=no-mention`;
   - successful `message.action` sends.
5. For bot-to-bot handoffs, inspect the Telegram entity type. A message starting `/task@iq5000_bot ...` from another bot can be stored in Telegram history as `bot_command` yet still be classified by OpenClaw auto-reply as `no-mention`, so it will not wake Bud execution. A plain text mention such as `@iq5000_bot /task correlation_id=...` or `@iq5000_bot status-check correlation_id=...` is the reliable wake form until the parser is fixed.
6. Check lifecycle board/watchdog scope. Many Agentic Stack helpers default to topic `642`; for other topics, explicitly pass `--chat-id <chat_id> --topic-id <topic_id>` before concluding that a task was ignored. If a valid public ACK exists but the board missed it, sync/backfill from the public event with correlation id and source evidence rather than resending.
7. Check target artifacts only as supporting evidence; absence of files is not enough by itself if ACK is missing, and presence of files is not a substitute for public ACK when the user asked about progress.
8. If no ACK/progress is visible after spool + trajectory + board checks, send one concise public status-check in the same topic with the correlation id asking for one of:
   - `ACK + started + checkpoint ETA`
   - `BLOCKED + reason`
   - `NOT RECEIVED`
9. If still silent after a short window, escalate via the reliable fallback path or resend the full task. Do not restart live runtime services unless the user separately approved that action.

## Manager-facing wording

Keep it short:

- `Не вижу публичного ACK от Bud.`
- `Задача в ingress попала, но подтверждения старта нет.`
- `Проверяю не только чат, но и executor trajectory/message.send + topic-scoped board.`
- `Если trajectory показывает messageId ACK — проблема в stale watcher/board, не в Bud.`
- `Отправил status-check с тем же correlation id.`
- `Если ответа не будет через N минут — ресенд/эскалация как routing issue, без рестарта runtime.`

Avoid raw log dumps unless asked; include only message ids/timestamps and the operational conclusion.
