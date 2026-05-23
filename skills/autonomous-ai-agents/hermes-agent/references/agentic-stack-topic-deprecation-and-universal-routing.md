# Agentic Stack: universal MM/Bud routing + safe topic deprecation

## Trigger

Use when Mikhail changes Agentic Stack Telegram topic architecture, deprecates coordination topics, or asks whether a topic can be deleted/archived.

## Current approved rule

Applies to all active Agentic Stack topics unless a topic explicitly overrides it:

- Mikhail's messages go to Hermes/MM first by default: direct tag, reply to Hermes, or ordinary topic message.
- Bud answers Mikhail only when explicitly tagged (`@iq5000_bot`) or when Mikhail replies to Bud's message.
- When Bud is directly addressed, Hermes stays silent unless Mikhail tags Hermes or asks for a comment.
- Hermes may delegate Bud inside the same topic. Bud replies to Hermes in that same topic.
- MM ↔ Bud discussion remains visible to Mikhail, but human-level only: essence, actions, conclusions, hypotheses, proposals. Avoid raw parameters and unnecessary technical chatter.
- Hermes normally owns the final user-facing answer.

## Topic status decisions

- `642 / MM + Bud`: `deprecation_pending`. It is no longer the single global coordination lane. The MM → Bud → MM protocol is rolled out per topic so task context stays with its domain.
- `723 / MM Only`: `deprecation_pending`. Replace with DM to `@ceo5000_bot` for private/strategic Hermes-only communication unless Mikhail explicitly wants a public Hermes-only archive.
- `259 / Perplex`, `584 / Summarize`, `21 / Music`, `488 / HR`: active and retained.
- `4 / Analyst`: includes CFO context; no separate CFO topic currently exists.

## Safe deprecation checklist before deleting a Telegram topic

Do **not** tell Mikhail to simply delete a topic until these are checked:

1. Update source of truth first:
   - `/Users/xbr/.agentic-stack/chats.yaml`
   - `/Users/xbr/.openclaw/workspace/chats.md`
   - relevant skill references / durable memory.
2. Search for hardcoded topic IDs in routing, board, watchdog, cron, reminders, docs, and scripts.
3. Move scheduled deliveries away from the deprecated topic.
4. Convert hardcoded single-topic scripts to multi-topic or retire them.
5. Preserve important links, decisions, correlation IDs, and history needed for audit.
6. Run smoke tests in 2–3 domain topics:
   - ordinary Mikhail message wakes Hermes;
   - direct Bud tag wakes Bud and Hermes stays silent;
   - Hermes delegates Bud in-topic;
   - Bud responds visibly but concisely;
   - Hermes gives final answer.
7. Only after smoke passes: archive/close/delete the Telegram topic.

## Known dependency pattern from the 642/723 migration

Typical blockers found before deleting `642`/`723`:

- cron jobs with `origin.thread_id` set to `642` or `723`;
- scripts such as topic-specific watchdogs, outbound loggers, boards, router audits;
- historical reports and one-shot cron outputs that mention old topic rules;
- subconscious/topic-policy snapshots that may need refresh after source-of-truth changes.

## Reporting style

For Mikhail, answer manager-style in Russian:

- decision first;
- why briefly;
- whether he can delete now: yes/no;
- blockers;
- safe sequence.

Avoid long implementation detail unless asked.