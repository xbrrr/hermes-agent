# OpenClaw Telegram topic routing triage

Use this when a Telegram task/mention to Bud/OpenClaw was sent successfully but Bud does not ACK or wake in the expected topic.

## Signal pattern

- Telegram send succeeds and returns a `message_id`.
- OpenClaw gateway may report `running` / health OK.
- Bud does not create/update the expected topic session and no ACK appears.
- Other topics may still work, so this is not necessarily a total gateway outage.

## Safe triage sequence

1. **Confirm outbound delivery**
   - Verify the sent `message_id`, `chat_id`, and `topic_id` from the sender side.
   - If a correlation id exists, search shared task/event logs for it.

2. **Check whether Telegram ingress is stuck**
   - Inspect OpenClaw Telegram offset state, e.g. `~/.openclaw/telegram/update-offset-*.json`.
   - Compare its mtime/last update with current time and recent messages.
   - If safe and credentials are locally configured, query Telegram `getUpdates` from `lastUpdateId + 1` without printing the token. Count pending updates and inspect only metadata/previews.

3. **Check ingress spool, not just logs**
   - Look under `~/.openclaw/telegram/ingress-spool-*/*.json` for the relevant `message_id` / `correlation_id`.
   - If the message is in spool, Telegram delivery and polling worked; the remaining problem is routing/session wakeup.

4. **Check session freshness per topic**
   - Inspect `~/.openclaw/agents/main/sessions/sessions.json`.
   - Compare `updatedAt` for the expected key, e.g. `agent:main:telegram:group:<chat_id>:topic:<topic_id>`, against the message time.
   - If another topic updates but the target topic does not, classify as topic-specific routing/config, not gateway-down.

5. **Check gateway runtime separately**
   - `openclaw status --deep` can show gateway reachable and Telegram OK while a specific topic still fails to wake.
   - `launchctl print gui/$UID/ai.openclaw.gateway` shows whether the LaunchAgent is running, but does not prove topic routing works.

6. **If polling is stale, do one safe restart**
   - `openclaw gateway restart`
   - Re-run status and verify offset/spool advances.
   - Do not treat restart success as final; still smoke the affected topic.

7. **If spool advances but target topic session does not wake**
   - Inspect OpenClaw Telegram group/topic config.
   - Look for an explicit topic entry for the affected topic and its `allowFrom`, `requireMention`, and `systemPrompt`/routing rules.
   - Do not assume wildcard topic config wakes bot-origin tasks/mentions correctly.

## Classification guide

- **Gateway/polling stuck:** offset mtime old, pending updates pile up, restart makes offset advance.
- **Topic routing broken:** message appears in ingress spool, gateway logs/other topics are active, but the expected topic session `updatedAt` remains stale.
- **Agent/model blocked:** topic session updates and a run starts, but no reply arrives; inspect session trajectory/logs next.

## Smoke after changes

After any config or restart:

1. Plain direct mention in the target topic: `@iq5000_bot ping`.
2. Formal task form if applicable: `/task@iq5000_bot correlation_id=<test-id> hops=0 max_hops=2`.
3. Verify:
   - ingress spool contains the message;
   - target topic session `updatedAt` changes;
   - public ACK appears in the topic;
   - watchdog/board state matches the public chat.

## Pitfalls

- Do not stop at “gateway is running.” A topic can be dead while gateway and another topic are healthy.
- Do not rely only on `openclaw status --deep`; it is a coarse health check.
- Do not print bot tokens or raw secrets when using Bot API diagnostics.
- Do not make runtime config changes silently; for live Telegram routing, summarize scope and verify with smoke tests after restart.
