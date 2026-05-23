# Agentic Stack Subconscious Live Recall Smoke

Use this when Mikhail asks to check whether Subconscious actually remembers operating decisions, not just whether deterministic nightly probes passed.

## Trigger

- User asks to “do the live recall smoke”, “check recall”, “prove it remembers”, or similar for Subconscious / Agentic Stack memory.
- A nightly Subconscious report says quality probes passed but the user wants a more practical verification.

## Procedure

1. **Route correctly**
   - Subconscious memory/recollection work belongs in the `Subconscious` topic.
   - Runtime, cron delivery, topic governance, gateway restarts, and health incidents belong in `Server-doctor` unless the question is specifically memory behavior.
   - Verify topic mapping from the shared source of truth when routing is ambiguous.

2. **Ask 5–7 real operating questions**
   Use questions that matter in live work, for example:
   - Which deleted/retired topics must not be used?
   - What is the boundary of Subconscious?
   - Where do routing/runtime/cron governance tasks go?
   - What is the policy for Hindsight vs local Subconscious?
   - What approval/smoke/drain rule applies before live/canary/restart?
   - Which topic owns long coding work and creative/design/image work?
   - What style/format does Mikhail expect for short status reports?

3. **Ground answers**
   - Compare recall against `chats.yaml`, `chats.md`, Subconscious decision views/reports, and durable memory.
   - If using deterministic helper output, label it as deterministic/lexical, not a full semantic benchmark.
   - If using tool retrieval, judge whether top results contain the needed fact, not whether they merely mention a keyword.

4. **Report briefly**
   - One Telegram message.
   - Say: overall result, passed count, weak spots, next action.
   - Do not paste raw JSON, file paths, long logs, or every retrieved record unless asked.
   - Use natural Russian and avoid stock AI phrases.

## Example result format

```text
Live recall smoke готов.

Итог: зелёный, 7/7.

Проверил:
- retired/deleted topics не используются;
- Subconscious ограничен памятью/recall/reflection/preflight;
- runtime/routing/cron governance уходят в Server-doctor;
- Hindsight остаётся benchmark/staging;
- live/canary/restart требуют явного решения и smoke/drain;
- Coding/Picasso распознаются как отдельные направления;
- стиль ответа: коротко, естественно, без AI-штампов.

Слабое место: это ещё не полный semantic benchmark; следующий шаг — живой вопрос→ожидаемый ответ→оценка.
```

## Pitfalls

- Do not answer with a long forensic report when the user asked for a smoke check.
- Do not call deterministic keyword probes “semantic quality”. They are a guardrail, not a full evaluation.
- Do not keep discussing in DM if the user asked to move the topic; send the concise result to the correct topic and only confirm in DM.
