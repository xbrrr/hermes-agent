# Agentic Stack topic migration / deprecation playbook

Use this when retiring or deprecating Telegram topics, cron delivery targets, or Hermes/Bud coordination lanes.

## Durable pattern

1. Treat `/Users/xbr/.agentic-stack/chats.yaml` as the source of truth and `/Users/xbr/.openclaw/workspace/chats.md` as the human inventory.
2. Distinguish **active runtime defaults** from historical logs/sessions before editing. Do not bulk-replace topic IDs in history.
3. For a retiring topic:
   - mark the topic as inactive/retired in the registry;
   - add an explicit replacement policy;
   - reject the retired topic in routing/history/queue/logging helpers;
   - reroute cron delivery/origin to the replacement topic or DM;
   - keep Telegram archive/delete as a separate post-smoke approval.
4. For a deprecated-but-temporary coordination topic:
   - keep it active only as `deprecation_pending` / migration-control-room;
   - remove it as a hardcoded default from helpers;
   - route reports to subject topics, not to a catch-all.
5. Prefer a small shared registry module over scattered constants. Helpers should read active topic policy and fail closed on retired topics.
6. Smoke without live restart first:
   - compile/check scripts;
   - run helper self-tests;
   - verify accepted replacement topic;
   - verify retired topic rejection;
   - validate cron JSON/YAML/doc source-of-truth.
7. Report in the subject topic. For ops/runtime/topic migration, use Server-doctor topic `1346`; private Hermes-only TODO goes to Mikhail DM.

## Specific Agentic Stack lesson from 2026-05-20

- `642 / MM+Bud` and `723 / MM Only` were both Telegram-deleted/retired, not merely deprecated or pending archive.
- `723` routes to Mikhail DM for private Hermes-only/TODO; ops/runtime/migration reports route to `1346 / Server-doctor` or another explicit subject topic.
- Runtime helper defaults were migrated toward `1346 / Server-doctor` or explicit subject topic policy.
- After a user corrects topic lifecycle state (for example “deleted” vs “pending archive”), update both source-of-truth surfaces: `/Users/xbr/.agentic-stack/chats.yaml` and `/Users/xbr/.openclaw/workspace/chats.md`, then validate topic inventory and cron/job delivery/origin fields.
- Remove or neutralize stale cron `origin`/delivery pointers to deleted topics; they may not be visible as active delivery targets but can still preserve bad routing context.
- Remaining references to `642`/`723` after migration can be legitimate historical data or deprecation policy; do not treat every text match as a live dependency.
