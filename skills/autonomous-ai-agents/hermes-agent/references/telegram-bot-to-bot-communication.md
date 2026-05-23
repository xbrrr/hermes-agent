# Telegram Bot-to-Bot Communication for Multi-Agent Topics

Use this when diagnosing or implementing public two-way communication between Hermes and another Telegram bot/agent in a shared group topic.

## Key Telegram Bot API 10.0 Facts

Telegram historically blocked bots from seeing messages from other bots; older StackOverflow answers and older gateway assumptions may still say “bots can't see messages meant for other bots regardless of privacy mode.” That is outdated for Bot API 10.0+.

Telegram now documents **Bot-to-Bot Communication**:

- Bots generally still cannot see other bots by default.
- Bot-to-Bot Communication Mode must be enabled in `@BotFather` / BotFather MiniApp.
- In groups, reliable bot→bot addressing is:
  - a command mention: `/command@OtherBot ...`, or
  - replying directly to a message from the other bot.
- Plain text `@OtherBot` mention is not the documented reliable trigger for group bot-to-bot delivery.
- Private bot→bot `sendMessage` to `@username` requires Bot-to-Bot Communication Mode enabled for both sender and recipient.
- For broad passive visibility of all bot messages in groups, the receiving bot also needs admin rights or disabled Group Privacy Mode.
- Telegram explicitly requires loop prevention: dedupe, rate limits, max interaction depth/timeouts.

## Live Probe Pattern

Use Bot API `getMe` for both bot tokens and inspect:

- `can_read_all_group_messages` — privacy/admin visibility indicator.
- `supports_guest_queries` — Guest Mode indicator, not the same as bot-to-bot.

Then test direct bot→bot private send in both directions. If it fails with:

```text
Bad Request: USER_BOT_TO_BOT_DISABLED
```

then Bot-to-Bot Communication Mode is disabled for at least one side. Do not keep debugging allowlists or prompt wording as the primary cause.

## Correct Public Two-Way Protocol

For a public Hermes↔executor exchange in a topic:

1. Enable Bot-to-Bot Communication Mode for both bots in `@BotFather`.
2. Prefer command-addressed turns when both gateways pass them through:
   - Hermes → Bud: `/check@iq5000_bot correlation_id=...`
   - Bud → Hermes: `/ack@ceo5000_bot correlation_id=...`
3. If the executor gateway intercepts slash commands before sending (observed with OpenClaw treating `/ack` as a local command), use a plain-text protocol for that direction instead, e.g. `ACK correlation_id=... hops=1 max_hops=2`, or use reply-to-agent-message turns if both bots can receive replies.
4. Include a correlation ID and visible routing metadata in the message body.
5. Enforce max hops/depth, dedupe by Telegram message ID, and per-pair rate limits.
6. Add an emergency kill switch before enabling autonomous bot↔bot replies.

### Addressing Discipline: Do Not Summarize Instead of Tagging

If the user expects the executor bot to answer publicly, Hermes must perform an actual addressed bot-to-bot turn in the topic — for example `/task@iq5000_bot correlation_id=... hops=0 max_hops=2 ...` — and verify Telegram accepted the send. A normal Hermes reply that merely summarizes a plan, records a roadmap, or mentions Bud by display name is **not** a Bud-addressed turn and should not be described as agent-agent conversation.

When corrected that the executor did not answer because Hermes failed to tag/address it, immediately send a new command-addressed message with a fresh correlation ID, then report the Telegram `message_id` and expected ACK format. Do not claim consensus with the executor until the matching ACK/result arrives.

## Public Smoke-Test Identity Discipline

When validating a public bot-to-bot exchange, prove both **delivery** and **sender identity**. A common false-positive is sending the probe through the executor's own CLI/gateway helper (for example `openclaw message send`) and then interpreting the result as Hermes→executor traffic. That helper may post **as the executor bot**, producing a bot-self message rather than a cross-bot message.

Use the actual sender bot token/API for the direction under test:

- Hermes → Bud: send via Hermes / `@ceo5000_bot` Bot API token, not through Bud/OpenClaw's send helper.
- Bud → Hermes: send via Bud / `@iq5000_bot` token or executor gateway.

Record and verify these fields before declaring the smoke test complete:

- `ok: true` from Telegram `sendMessage`;
- `message_id`;
- `chat_id` and `message_thread_id` / topic id;
- `from.username` equals the intended sender bot;
- receiving gateway logs show the matching inbound message and correlation ID;
- executor session/trajectory shows `prompt.submitted` for the task and `message.send` `tool.result` for ACK/progress, with returned Telegram `messageId`;
- the lifecycle board/watchdog is queried with the exact `--chat-id` and `--topic-id` (do not rely on a default topic such as 642 for tasks posted elsewhere);
- the reciprocal ack is visible in the same topic and addressed back with `/ack@OtherBot` or the agreed plain-text `ACK correlation_id=...` fallback.

If the executor trajectory proves it sent ACK/progress but the coordinator does not see it, treat the problem as stale observer/board scope first. Do not resend the task or claim the executor ignored it until trajectory, public message id, and topic-scoped board have been reconciled.

## Bridge vs Native Bot-to-Bot

A local bridge can make messages visible by having Hermes invoke the other gateway, then the other bot sends a public message. This is useful as a fallback and for auditability, but it is not native two-way Telegram bot-to-bot delivery.

If the user explicitly asks for two-way bot communication, do not present bridge-only as sufficient. State the distinction and configure native Telegram bot-to-bot mode if possible.

## OpenClaw/Hermes Implementation Notes

OpenClaw issue `openclaw/openclaw#79077` captures the channel-handler work needed for Telegram Bot API 10.0 bot-to-bot:

- recognize `message.from.is_bot=true` as a separate sender type;
- add peer maps/trust levels for known bot IDs;
- add sender-type policies such as humans-only vs allowlisted bots;
- add loop guards and rate limits;
- add diagnostics for BotFather mode mismatch.

For Hermes Agent multi-agent Telegram topics, update the topic routing file to distinguish:

- `native_bot_to_bot`: public Telegram turns via Bot API 10.0 mode;
- `bridge_send`: gateway/API mirroring for fallback;
- `private_queue`: internal audit/task queue, not visible by default when the user wants public coordination.
