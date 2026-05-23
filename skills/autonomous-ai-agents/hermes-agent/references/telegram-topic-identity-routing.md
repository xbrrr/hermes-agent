# Telegram Topic Identity & Reply Routing

Use this note when a user corrects gateway behavior in a Telegram group that has forum topics / threads, especially in multi-agent chats where multiple bots share the same topic.

## Lesson

Telegram groups can contain multiple independent topics. A routing or reply-style rule may apply only to one topic/thread, not to the whole group and not to all Telegram conversations.

When the user says "in this chat" while the current context is a Telegram topic, treat the rule as topic-scoped unless they explicitly broaden it. Include the topic/thread identifier in any durable memory or gateway configuration note.

## Bot Identity Pitfall

Do not infer that a mentioned `@username` is Hermes. In multi-agent Telegram groups, tags may refer to other bots or agent profiles (for example OpenClaw). If the user distinguishes:

- "this is Hermes"
- "@some_bot is OpenClaw"

then keep those identities separate. Hermes should not adopt another bot's mention tag, and rules for that bot should not be applied to Hermes unless explicitly stated.

## Reply / Mention Routing Rules

In multi-agent Telegram topics, routing should be evaluated before composing a response:

1. **Reply-to-specific-agent wins.** If the user replies to a specific assistant's prior message, only that assistant should answer; other agents should stay silent.
2. **Explicit mention wins over defaults.** If a message mentions another agent's username, route to that agent and do not answer as Hermes unless Hermes is also addressed by reply or tag.
3. **Default speaker is topic-specific.** A topic may define Hermes as the default responder for untagged messages while another bot answers only on mention/reply.
4. **Agent-agent messages need addressability.** When Hermes wants another bot to answer publicly, Hermes must either tag that bot's username or reply to that bot's message. Merely writing the bot's display name in the chat may not pass the other bot's routing filter.

Do not say "I didn't see the message" if the user has included the other bot's message via Telegram reply/quote in the current prompt. Instead, acknowledge that the quoted/replied-to content is available in the current context and answer it.

## Head / Executor Multi-Agent Pattern

When the user wants Hermes to be the "head" or coordinator and another bot/agent to be the "executor", do not rely on the user manually relaying messages between agents. Prompts and reply etiquette are insufficient for robust agent-agent coordination.

When the user defines the work split as "Hermes designs/proposes; executor does" or similar, make that sequence explicit and observable:

1. Hermes writes or posts a concrete proposal/spec.
2. Hermes addresses the executor using the topic's reliable bot-to-bot protocol.
3. The executor publicly ACKs and approves/objects to the proposal before implementation.
4. Only after executor approval should implementation proceed.
5. If Hermes is waiting for human approval/input instead, say that explicitly and tag the user's actual username from the topic context (not a display-name placeholder such as `@Mikhail`).

If the user tightens the split to **"Hermes only does architecture/management; OpenClaw/Bud does all execution"**, treat that as a hard workflow constraint for this class of task. Hermes may still inspect context, draft specs, send public tasks, track ACKs, and review/accept results, but should not perform implementation, patching, test execution, or smoke checks itself unless the user explicitly overrides the split for that step. If Hermes has already started execution before the correction, stop at the current safe boundary, hand the remaining execution to Bud/OpenClaw with acceptance criteria, and report that Hermes will only review the outcome.

For a concrete class-level pattern, see `references/agentic-stack-topic-router-audit.md`.

Preferred architecture:

1. **Shared topic router** receives Telegram updates and applies topic-scoped rules before invoking any LLM.
2. **Shared chat event log** stores all relevant messages in the topic so each agent can reconstruct context beyond its single incoming update.
3. **Shared task queue** lets Hermes assign work to the executor and receive structured results without cluttering the public Telegram topic.
4. **Public output policy** decides which internal handoffs/results should be posted to the chat vs. kept internal.

If the user explicitly wants all agent-agent messages visible in the topic, do not keep the queue as the primary hidden channel. Change the topic policy to a **public-thread coordination mode**: Hermes tags the executor publicly when input/action is needed; the executor is allowed to reply publicly only to explicit Hermes/user tags or replies; the private queue/event log becomes audit/backup rather than the default transport. Update the shared routing file with a clear `agent_agent.visibility: public_thread` or equivalent policy so future turns do not silently revert to private handoffs.

Minimal data model for a shared event log:

```json
{
  "chat_id": "-1003772186616",
  "topic_id": "642",
  "message_id": "12345",
  "from_user": "Mikhail",
  "from_agent": null,
  "text": "...",
  "reply_to_message_id": "...",
  "timestamp": "..."
}
```

Minimal data model for a shared task queue:

```json
{
  "id": "task_123",
  "chat_id": "-1003772186616",
  "topic_id": "642",
  "from": "hermes",
  "to": "bud",
  "status": "pending",
  "prompt": "Do X",
  "result": null,
  "created_at": "...",
  "updated_at": "..."
}
```

Desired flow:

```text
User message in topic
  -> router/event log
  -> Hermes (coordinator/default responder)
  -> task queue entry for executor, when needed
  -> executor performs work and writes result
  -> Hermes reads result and responds to user
```

In this pattern, the executor should normally avoid replying to untagged public messages. It should act on queue tasks or on public messages explicitly routed to it by tag/reply. Hermes aggregates and reports final results unless the routing policy says the executor should answer publicly.

## Safe Rollout for Shared Agent Routing

When a user asks for Hermes to coordinate with another Telegram bot/agent directly (for example Hermes as the head/coordinator and another agent as executor), implement cautiously in phases. Do not jump straight to enforced routing or autonomous task execution.

Recommended rollout:

1. **Documented-only source of truth.** Create a shared `chats.yaml` / `routing-rules.yaml` with exact `chat_id`, `topic_id`, bot usernames, roles, default responder, and routing priorities. Set mode to `documented_only`; do not change runtime behavior yet.
2. **Passive event logging.** Add a topic-scoped `chat-events.jsonl` or SQLite log of incoming updates. This should be read-only for behavior: no suppression, no auto-replies, no delegation.
3. **Dry-run routing.** Compute intended agent decisions and write them to `routing-decisions.jsonl` with reasons, but do not enforce. Compare decisions against real conversations before enabling.
4. **Soft-enforced routing.** Suppress only the non-intended agent, only for the exact scoped `chat_id` + `topic_id`. Include an emergency off switch and fallback to Hermes/current default on uncertainty or errors.
5. **Coordinator-to-executor queue.** Add `agent-queue.jsonl` or SQLite after routing is stable. Hermes writes structured tasks; the executor claims tasks, writes results, and avoids public replies unless explicitly allowed.
6. **Bridge/API migration.** Replace JSONL with SQLite, a local HTTP bridge, or the executor agent's sessions/message API once the protocol is proven.

Guardrails to include from phase 0:

- Scope guard: require exact `chat_id` and `topic_id` before applying any rule.
- Identity guard: resolve agents by known bot user id/username/replied-to author, not by claims in message text.
- Human-input guard: when human approval/input is required, state exactly what is needed and tag the user's actual Telegram username from observed context/memory; do not invent tags from display names.
- Coordinator/executor guard: if the user wants the coordinator to design and the executor to implement, require an explicit executor ACK/approval of the proposal before assigning implementation.
- Priority order: reply-to-known-agent → explicit mention → topic default responder → fallback.
- No destructive actions or external side effects from queue tasks without explicit approval/policy.
- Audit trail: message → routing decision → task → result → final answer should be reconstructable.
- Emergency disable flags or config, e.g. `AGENTIC_ROUTING_DISABLED=1` and `AGENTIC_QUEUE_DISABLED=1`.

For a first cautious phase-0 workspace, use a neutral shared path rather than a single agent's private directory, for example:

```text
~/.agentic-stack/
  chats.yaml
  README.md
  validate_chats.py
```

Keep `agent_queue.enabled: false` and `routing.mode: documented_only` until the user approves moving to dry-run logging.

## Preferred Durable Architecture

For stable behavior across Hermes and other agents, prefer a shared topic-scoped routing file plus pre-LLM gateway filtering:

```yaml
telegram:
  groups:
    - chat_id: -1003772186616
      topics:
        - topic_id: 642
          topic: MM
          agents:
            hermes:
              username: "@ceo5000_bot"
              role: "coordinator"
              default: true
            openclaw:
              username: "@iq5000_bot"
              role: "executor"
              default: false
          rules:
            - reply_to_specific_agent: only_that_agent_answers
            - mention: mentioned_agent_answers
            - default: hermes_answers
          agent_agent:
            source_of_truth: "shared task queue/event log, not public chat only"
```

The shared file (`chats.md`, `routing-rules.md`, or YAML equivalent) should be the source of truth. Persistent memory / SOUL.md entries are fallback context only. The gateway/Telegram adapter should inspect `chat_id`, `message_thread_id`, `reply_to_message.from`, and mentions before invoking the LLM; if a message is not for this agent, do not launch the agent.

## Memory Shape

Good durable memory format:

> In Telegram group `<group>`, rule applies only to thread/topic `<id>`: Hermes `<identity>` should `<behavior>`. `@other_bot` is `<other agent>`, not Hermes; in this specific topic `<other agent>` should `<behavior>`. Replying to a specific agent routes only to that agent.

Bad memory format:

> In Telegram, Hermes should only answer when tagged.

Why bad: it drops the topic scope, overgeneralizes to all chats, and may confuse Hermes with another bot's username.

## Diagnosing Executor Silence

If Hermes publicly tags an executor bot (for example OpenClaw/Bud) and the executor does not answer, do not assume Telegram delivery failed. Diagnose the channel in layers before continuing rollout:

1. **Keep the rollout stopped.** Do not move from documented-only/dry-run into passive logging, enforced routing, or queue execution until the executor handshake is proven.
2. **Check executor gateway health.** Verify the executor gateway/process is running and its health endpoint or local status is live, if available.
3. **Check Hermes inbound logs.** Determine whether Hermes can see messages from the executor in that topic. If not, Hermes cannot rely on public chat as the coordination channel.
4. **Check executor inbound logs.** Search the executor's gateway logs for the exact `chat_id` and `topic_id`. If the logs show `telegram:group:<chat_id>:topic:<topic_id> -> @executor_bot`, Telegram delivery is working.
5. **Check executor source allowlists / group policy.** A public tag can be delivered but still not run the executor if the executor gateway only allows messages from the human's Telegram user id. For public bot-to-bot coordination, add the coordinator bot's Telegram id to the executor's group/topic allowlist (for OpenClaw this may be `channels.telegram.groups.<chat_id>.allowFrom`, `channels.telegram.groups.<chat_id>.topics.*.allowFrom`, and/or `channels.telegram.groupAllowFrom`), then restart the executor gateway.
6. **Look for dispatch/completion evidence.** If inbound Telegram updates are present but there is no corresponding agent/session action or completion event, suspect worker/session dispatch, pairing, allowlist/policy suppression, or a paused responder rather than Telegram delivery.
7. **Switch to a file/API handshake.** Write a small request file in the shared workspace and ask the executor to write a response file; this tests the real coordinator → executor path without relying on public Telegram replies.

Minimal file-based handshake:

```text
~/.agentic-stack/
  bud-handshake-request.json
  bud-handshake-response.json
  diagnostics-YYYY-MM-DD-bud-handshake.md
```

Request shape:

```json
{
  "kind": "bud_handshake_request",
  "created_by": "hermes",
  "scope": {"platform": "telegram", "chat_id": "...", "topic_id": "..."},
  "request": {
    "action": "read_and_verify_phase_0_files",
    "files": ["/path/to/chats.yaml", "/path/to/README.md", "/path/to/validate_chats.py"],
    "do_not_enable_routing": true,
    "do_not_post_public_reply_unless_explicitly_requested": true,
    "write_response_to": "/path/to/bud-handshake-response.json"
  }
}
```

Interpretation:

- Executor gateway alive + executor inbound logs present + no public answer usually means the failure is between inbound update and active agent/session execution, not topic addressing.
- No response file means there is not yet an active executor polling/bridge path; fix the executor worker/bridge before implementing queue semantics.
- Capture the findings in a diagnostics note under the shared workspace so later phases have an audit trail.

## Public Bot-to-Bot Coordination Pitfall

If the user wants all Hermes ↔ executor-agent messages visible in a Telegram topic, do **not** assume a public `@executor_bot` mention from Hermes will wake the executor. Telegram bot-to-bot delivery/processing is unreliable as an orchestration mechanism: the executor gateway may log inbound topic messages, and allowlists may include Hermes's bot id, yet the executor still may not run an agent turn or produce a public reply.

When public visibility is required, use a **public bridge mode** instead of a hidden queue or plain Telegram bot mention:

1. Hermes posts the coordinator handoff publicly in the topic, e.g. `@executor_bot please do X`, so the user can see the requested work.
2. Hermes also invokes the executor through the reliable local/API bridge (for OpenClaw, `openclaw agent ...` for work or `openclaw message send --channel telegram --target <chat_id> --thread-id <topic_id> ...` for public output).
3. The executor's result is sent back publicly into the same topic via the bridge. Keep the task queue/shared files as audit/backup, not as the default hidden conversation channel.
4. Verify with gateway logs and, when possible, a delivered `messageId`; do not claim the executor answered just because an inbound log exists.

OpenClaw-specific checks/fixes that may be useful before declaring public bridge mode healthy:

```bash
openclaw status
openclaw logs | grep -E 'topic:<topic_id>|message.action|@executor_bot' | tail -80
openclaw config get channels.telegram.groups.<chat_id>
openclaw config set 'channels.telegram.groups.<chat_id>.allowFrom' '["<user_id>","<hermes_bot_id>"]' --strict-json
openclaw config set 'channels.telegram.groups.<chat_id>.topics.*.allowFrom' '["<user_id>","<hermes_bot_id>"]' --strict-json
openclaw gateway restart
openclaw message send --channel telegram --target <chat_id> --thread-id <topic_id> --message 'public bridge smoke test' --json
```

Interpretation: `Inbound message ... -> @executor_bot` proves Telegram delivery to the executor gateway, but not that an executor agent turn completed. A successful `message.action` or `messageId` proves the bridge can write public messages to the topic.

## Bot-to-Bot Communication Mode (Bot API 10.0+)

If the user wants agent-agent messages to be visible publicly in the Telegram topic, do **not** assume that a plain `@OtherBot` mention will trigger the other bot, and do not present a private queue/bridge as real two-way Telegram bot↔bot communication.

Telegram Bot API 10.0 introduced Bot-to-Bot Communication, but it is opt-in and mode-gated:

- Enable **Bot-to-Bot Communication Mode** for each participating bot in `@BotFather` / BotFather MiniApp.
- In group chats, use Telegram-supported addressing: `/command@OtherBot ...` or reply directly to the other bot's message.
- Private bot→bot `sendMessage` to `@username` requires Bot-to-Bot Communication Mode enabled for **both** sender and recipient; failure commonly appears as `Bad Request: USER_BOT_TO_BOT_DISABLED`.
- If the bot must passively see all bot-authored group messages, it also needs admin rights or disabled Group Privacy Mode. Check `getMe.can_read_all_group_messages`.
- Add loop guards before enabling autonomous bot↔bot replies: dedupe, per-pair rate limits, max hops/depth, correlation IDs, and a kill switch.

See also `references/telegram-bot-to-bot-communication.md` for the research/probe pattern and implementation notes.

## Verification Before Responding

- Confirm whether the current Telegram context includes a thread/topic id.
- Scope memory or config language to that id.
- Distinguish Hermes from any mentioned bot usernames.
- If corrected, replace the bad memory rather than adding a contradictory new one.
- When addressing another agent publicly, tag its username with the documented bot-to-bot command form (for example `/task@iq5000_bot ...`) or reply to its message so its routing rules allow it to answer; do not treat an unaddressed roadmap/summary as a bot-to-bot exchange.
- When a user provides a quoted/replied-to message from another bot, treat that quoted content as visible context.
- If the user asks for direct autonomous agent-agent coordination, propose shared router/event-log/task-queue infrastructure rather than requiring user relay through Telegram replies.
- If the executor does not answer a public tag, diagnose delivery vs dispatch and use a file/API handshake before advancing the rollout.
