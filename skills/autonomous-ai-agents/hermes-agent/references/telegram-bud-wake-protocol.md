# Telegram Bud Wake Protocol — Agentic Stack MM/topic 642

Session learning from 2026-05-17: direct bot mentions must be kept distinct from reply context and from formal lifecycle tasks.

## Correct behavior

In `Agentic Stack` → `MM / topic 642`:

- `@iq5000_bot <question>`: quick direct question to Bud/OpenClaw; should wake Bud.
- `@ceo5000_bot <question>`: quick direct question to Hermes/Master Mind; should wake Hermes.
- Reply to a Bud message with no other explicit bot mention: continuation directed to Bud; should wake Bud.
- Reply to a Hermes message with no other explicit bot mention: continuation directed to Hermes; should wake Hermes.
- `/task@iq5000_bot correlation_id=<id> hops=0 max_hops=2 ...`: formal delegated task that should be logged into board/watchdog lifecycle.

Do **not** interpret "Bud is silent by default" as "Bud ignores direct mentions." The intended rule is:

- Bud stays silent on ambient/general chat noise.
- Bud answers when Mikhail directly tags `@iq5000_bot` or replies to Bud.
- Bud uses `/task` path for formal auditable tasks.

## Routing priority rule

Explicit bot mention must win over reply context:

- Reply to Bud + `@ceo5000_bot` → Hermes should answer.
- Reply to Hermes + `@iq5000_bot` → Bud should answer.
- Reply to Bud with no explicit bot mention → Bud should answer.
- Reply to Hermes with no explicit bot mention → Hermes should answer.

A good topic routing priority is:

```yaml
priority:
  - explicit_mention
  - reply_to_known_agent
  - default_responder

mentions:
  "@ceo5000_bot": "hermes"
  "@iq5000_bot": "bud"

direct_mention_policy:
  "@ceo5000_bot": "wake_hermes_even_when_replying_to_bud"
  "@iq5000_bot": "wake_bud_for_direct_question_or_task"
  note: "Explicit mention wins over reply context in MM/topic 642: @ceo5000_bot in a reply to Bud must wake Hermes; @iq5000_bot in a reply to Hermes must wake Bud. /task@iq5000_bot is required only for formal board/watchdog lifecycle tasks."

reply_to_agent_message: "same_agent_unless_explicit_mention_targets_another_agent"
```

## Pitfalls observed

1. A policy phrase intended for formal Hermes→Bud lifecycle tasks — "plain @mention is not sufficient" — was too broad. It made ordinary `@iq5000_bot` questions look unreliable or invalid, which felt to the user like Hermes had muted Bud.

Preferred wording:

> For formal lifecycle work use `/task@iq5000_bot correlation_id=...`; for quick direct questions, plain `@iq5000_bot` mention must still wake Bud in `MM / topic 642`.

2. `reply_to_known_agent` before `explicit_mention` can suppress the intended target. If Mikhail replies to Bud but tags Hermes, Hermes should wake. If Mikhail replies to Hermes but tags Bud, Bud should wake.

## Fix pattern

1. Check the topic policy (`chats.yaml` or equivalent) for mention mappings and routing priority.
2. Put `explicit_mention` before `reply_to_known_agent`.
3. Add explicit direct mention rules for both bots.
4. Keep `/task@iq5000_bot` scoped to formal board/watchdog lifecycle tasks.
5. Validate policy config.
6. If gateway/router caches rules, restart or reload it only after the policy is correct.
7. Live-test both directions:
   - reply to Hermes with `@iq5000_bot ...` should wake Bud;
   - reply to Bud with `@ceo5000_bot ...` should wake Hermes.

## User-facing explanation

If Mikhail asks why one bot is silent, answer plainly and avoid normalizing the failure:

- Direct `@iq5000_bot` should wake Bud in `MM / topic 642`; if it does not, treat it as a routing/wake regression.
- Direct `@ceo5000_bot` should wake Hermes even when the message is a reply to Bud; if it does not, treat it as a routing-priority bug.
- Use `@iq5000_bot` / `@ceo5000_bot` for quick questions.
- Use `/task@iq5000_bot correlation_id=...` only when the work should be tracked in board/watchdog.
- Hermes should not ask Bud via a wake path it knows is unreliable and then treat silence as meaningful. Use the path that matches the desired interaction.
