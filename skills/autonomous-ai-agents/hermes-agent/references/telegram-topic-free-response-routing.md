# Telegram topic free-response routing for coordinator-only lanes

When a user says they communicate only with a specific bot in a Telegram forum topic (for example, "тут я общаюсь только с @ceo5000_bot"), treat it as a topic-scoped routing requirement, not a whole-group default.

## Lesson

Persistent memory can remember the preference, but it cannot wake Hermes if the gateway filters the message before an agent session starts. If `telegram.require_mention: true` (or `platforms.telegram.extra.require_mention: true`) is set, untagged topic messages will not reach Hermes unless the gateway/router has an explicit allow/free-response rule for that chat + topic.

## Recommended sequence

1. Confirm the exact Telegram `chat_id`, forum `topic_id` / thread id, and bot username.
2. Inspect current gateway mention settings and any topic router/free-response files.
3. Keep global `require_mention` enabled unless the user explicitly wants whole-group free response.
4. Add a topic-specific rule instead. Current Hermes Telegram adapter supports `free_response_topics` as either string entries (`"<chat_id>:<thread_id>"`) or dict entries. Put it where the adapter reads `PlatformConfig.extra` and, for env/config bridging compatibility, also mirror it under top-level `telegram` when editing `~/.hermes/config.yaml` directly:

```yaml
telegram:
  require_mention: true
  free_response_topics:
    - chat_id: "<telegram group id>"
      thread_id: "<forum topic id>"

platforms:
  telegram:
    extra:
      require_mention: true
      free_response_topics:
        - chat_id: "<telegram group id>"
          thread_id: "<forum topic id>"
```

Conceptual policy:

```yaml
chat_id: <telegram group id>
topic_id: <forum topic id>
default_responder: hermes
untagged_messages: route_to_hermes
other_bots: silent_unless_tagged_or_replied
```

5. Check that `gateway.config.load_gateway_config()` actually bridges top-level `telegram.free_response_topics` into `PlatformConfig.extra.free_response_topics` (and/or `TELEGRAM_FREE_RESPONSE_TOPICS`). If `config.yaml` is correct but runtime still only wakes an old/deleted topic, inspect `gateway/config.py`; older builds bridged `free_response_chats` but not `free_response_topics`.
6. Restart or reload the gateway after config/router changes.
7. Verify with an untagged message in that topic and confirm Hermes sees it without affecting other topics.

## Multi-agent coordination pattern

For coordinator/executor groups:

- Topic-specific user lane: user → coordinator bot only; executor stays silent unless tagged/replied/tasked.
- Public multi-agent lane: coordinator proposes; executor publicly ACKs/approves/objects; executor implements only after approval; coordinator verifies and explains to the user.
- Use `correlation_id` and `max_hops` for public bot-to-bot handoffs.

## Pitfalls

- Do not solve this by disabling `require_mention` for the whole Telegram group unless the user asks for that broader behavior.
- Do not rely on memory alone for pre-LLM routing. Memory affects the agent after launch; gateway routing determines whether the agent launches.
- Do not infer a bot identity from `@bot` casually in multi-bot topics. Keep Hermes/coordinator and executor bot usernames distinct.
