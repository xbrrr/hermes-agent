# Agentic Stack Topic Inventory Notes

Use this reference when refreshing Telegram topic / skill routing inventory for the Agentic Stack Hermes/Bud setup.

## Source of truth

- Prefer documented local sources before ad-hoc inference:
  - `/Users/xbr/.agentic-stack/chats.yaml`
  - `/Users/xbr/.openclaw/workspace/chats.md`
  - `/Users/xbr/.agentic-stack/agentic-stack-v2-topic-inventory.md`
- Treat memory/user profile as active routing policy, but update durable files only from verified/documented evidence.
- If Bud/OpenClaw has the freshest topic list, request a compact public ACK/delta in the relevant Telegram thread rather than relying on private/off-thread coordination.

## Coordination protocol

- Hermes is coordinator/default responder; Bud/OpenClaw is executor.
- In Agentic Stack thread 642, Hermes↔Bud coordination should be visible publicly by default.
- Use `/task@iq5000_bot correlation_id=<stable-id> max_hops=<n>` for formal Bud requests that need lifecycle visibility.
- Bud→Hermes ACKs may be plain text with `correlation_id=...`; do not assume `/ack` works because OpenClaw may intercept it as a local command.
- Explicit mentions override reply context: `@ceo5000_bot` targets Hermes, `@iq5000_bot` targets Bud.

## Inventory refresh workflow

1. Read current `chats.yaml` and existing inventory doc.
2. Ask Bud for a compact delta when topics changed today: topic_id → title/purpose, Bud skills, Hermes behavior, unknowns.
3. Reconcile conflicts by preferring verified Telegram links or current documented config over stale prior inventories.
4. Update inventory version with only documented/verified topic bindings; mark unresolved items as unknown rather than guessing.
5. Remove stale “unknown” TODOs once a link/config proves the answer; do not leave contradictory sections in the same inventory.
6. If the next cleanup step is obvious (e.g. align Bud after correcting a topic conflict), do it now: send the public alignment task with a correlation_id, update docs, and validate.
7. Validate YAML/config after edits when changed.
8. Reply with concise changed files, key deltas, verification result, and remaining unknowns only.

## Telegram topic URL parsing

For URLs like `https://t.me/c/3772186616/4/1547`:

- chat id for bot/API form: `-1003772186616`
- topic/thread id: `4`
- message id: `1547`

This pattern is useful for resolving stale topic-ID conflicts. Example lesson: if a current link proves `topic 4 = Analyst`, do not keep an older `topic 4 = CFO` binding as current; move the stale binding to unknown/history until re-verified.

## Known routing cautions

- Topic 1 should be ignored/disabled for both bots unless Mikhail explicitly reassigns it.
- Topics 723 and 1347: Mikhail talks to Hermes; Hermes coordinates/reviews; Bud/OpenClaw executes after Bud approval.
- In 1347/Subconscious, Hermes must not self-execute runtime/file changes unless explicitly reassigned.
- Server-doctor is separate from Web Admin: use server-doctor for hosts, bots, Docker/launchd/systemd, incidents, health checks, restarts, rollback, postmortems; use Web Admin for UI/admin/settings/product web-admin tasks.
