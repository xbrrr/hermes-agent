# Telegram private agent bridge pattern

Use this when a Telegram topic contains multiple bots/agents and the user wants one bot (Hermes) to be the public coordinator while another bot (e.g. Bud/OpenClaw) acts only as a private executor.

## Durable pattern

- Keep public Telegram routing topic-scoped: `chat_id` + `message_thread_id`/topic id are part of the rule key.
- Public behavior:
  - coordinator bot answers the user by default when appropriate;
  - executor bot stays silent unless directly tagged/replied to by the user, or unless the coordinator invokes it through a private channel;
  - agent-agent public chatter should be avoided unless explicitly requested.
- Private behavior:
  - coordinator writes an append-only queue/task record under a shared coordination directory;
  - coordinator invokes executor through a private/local session (OpenClaw local session, API, or equivalent), not via public Telegram mentions;
  - executor reads the queue item, writes a result artifact, and appends a status update such as `completed` with `result_path`;
  - coordinator verifies the queue status and result file, then reports the synthesized result publicly.

## Minimal queue record fields

- `task_id`
- `chat_id`
- `topic_id`
- `from` / `to`
- `status`: `pending`, `claimed`, `completed`, `failed`, or `cancelled`
- `visibility`: default `internal`
- `prompt`
- `result` and/or `result_path`
- timestamp

## Safety checks

- Scope queue helpers to the intended chat/topic; reject mismatched `chat_id` or `topic_id`.
- Keep the queue append-only for auditability.
- Do not store credentials, raw platform payloads, or unrelated private chat content in queue/result files.
- For smoke tests, use benign tasks like “write a short receipt file and mark completed.”
- Do not broaden to destructive or credential-bearing tasks until validation rejects malformed, oversized, token-like, or destructive payloads.
- Treat executor output as input for coordinator synthesis, not automatic user-facing truth.

## Verification recipe

1. Confirm topic config has coordinator/executor roles and queue enabled.
2. Create a benign queue item from coordinator to executor.
3. Invoke executor through the private/local session with the `task_id` and expected result path.
4. Read back the result artifact.
5. Show the queue history for that `task_id` and verify a `completed` event from executor.
6. Publicly report only the verified result; executor should not send a Telegram reply.
