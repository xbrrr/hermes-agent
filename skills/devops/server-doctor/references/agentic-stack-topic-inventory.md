# Agentic Stack topic inventory / routing governance

Use this reference when changing Agentic Stack Telegram topic routing, report delivery, or topic inventories.

## Source-of-truth order

1. `/Users/xbr/.agentic-stack/chats.yaml` — machine-readable registry and validation target.
2. `/Users/xbr/.openclaw/workspace/chats.md` — human-readable operating map for OpenClaw/Bud workspace.
3. Runtime/session evidence when inventory may be incomplete:
   - OpenClaw `openclaw.json` topic prompts/config.
   - OpenClaw sessions/trajectory metadata with `topic_id` / `topic_name`.
   - Telegram forum topic creation records in local session/message stores.

Do not claim the inventory is complete after checking only one source. Existing topics may be present in runtime/session history even when a current registry is stale.

## Current durable mapping after the 2026-05 correction

- `1346 / Server-doctor` — ops/runtime/topic settings, restarts, incidents, routing governance.
- `1347 / Subconscious` — memory/subconscious/decision preflight only.
- `92 / Web Admin` — web/admin/product settings and web-admin work.
- `76 / Coding` — long programming tasks: repos, features, refactors, tests, PRs, code review.
- `496 / Picasso` — creative/design/images/art, visual concepts, generation/editing workflows.
- `259 / Perplex` — research and social/X search routing.
- `584 / Summarize` — content summaries and extraction.
- `21 / Music` — music/DJ/discovery.
- `488 / HR` — HR/people/coaching.
- `4 / Analyst` — analytics and CFO context.
- `642 / MM+Bud` — deleted/retired historical safeguard; never target for new work.
- `723 / MM Only` — retired; use Mikhail DM for private Hermes-only/TODO.
- `1` — ignored/off.

## Update protocol

1. Baseline the requested change and identify whether it is ops/routing governance (`Server-doctor`), product/web-admin (`Web Admin`), memory (`Subconscious`), coding (`Coding`), or creative (`Picasso`).
2. Patch `chats.yaml` first, then `chats.md`, then any long-form inventory docs.
3. Update validators when a topic becomes required/active.
4. Run validation/smoke appropriate to the change (`validate_chats.py`, router self-tests, JSON validation for OpenClaw config when touched).
5. Report concise result and any runtime reload/restart caveat separately; do not imply file changes are loaded by a live runtime unless verified.

## Communication rule

Mikhail explicitly dislikes agentic flattery and ritual agreement. For routing/topic governance reports: give the correction, evidence, risk, and next boundary. Do not use phrases like “strong decision” or “you are thinking correctly” unless backed by concrete analysis, and even then prefer the evidence over praise.
