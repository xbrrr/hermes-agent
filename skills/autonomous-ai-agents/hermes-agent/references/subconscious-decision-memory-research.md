# Subconscious Decision-Memory / Recall-Before-Answer Research Notes

Use this reference when the user asks how to implement the “magic” layer where Hermes closes the management loop: decisions, owners, next actions, stale/conflict detection, repeated-pattern detection, and automatic briefs before important replies.

## Executive pattern

Do **not** implement this as “just more vector memory.” The durable pattern is a **decision-state layer** on top of memory:

1. Extract structured decisions/cancellations/commitments from conversations and events.
2. Store them append-only with source evidence, owner, status, next action, scope, entities, and supersession/conflict links.
3. Maintain derived current-state views per platform/chat/topic/project/resource.
4. Before important replies, run a topic-scoped recall/brief step that returns active decisions, owners, pending actions, blockers, stale/conflicts, and repeated patterns.
5. Run background reflection jobs to consolidate repeated patterns into skills/runbooks and flag stale or contradictory decisions.

Key invariant: corrections and cancellations create new records and links; they do not destructively overwrite the old record. The live answer comes from derived views, not from mutating the audit log.

## Suggested decision record fields

Minimum useful schema:

- `id`, `created_at`, `source_session`, `platform`, `chat_id`, `topic_id`
- `kind`: `decision | cancellation | commitment | correction | blocker | open_question | policy | owner_assignment`
- `scope`: global/user/project/topic/resource
- `subject`, `summary`, `rationale`
- `owner`, `next_action`, `due_at`, `status`
- `entities`, `tags`, `confidence`
- `evidence`: message ids, file paths, report paths, URLs
- `links`: `supersedes`, `superseded_by`, `contradicts`, `depends_on`, `cancelled_by`
- `last_verified_at`, `stale_after`, `ttl_policy`

For Agentic Stack topics, include visible Telegram topic title + topic id where possible; users do not always map bare numeric ids to names.

## Retrieval / brief recipe

Use multi-signal recall, not semantic search alone:

- keyword/BM25 for exact names, issue ids, bot handles, commands;
- semantic embeddings for paraphrased intent;
- entity/topic filters for platform/chat/topic/project;
- temporal ranking and recency boosts;
- graph/supersession traversal to collapse old decisions into current state;
- status filters (`active`, `waiting`, `cancelled`, `superseded`, `stale`, `conflict`).

A good user-facing brief is compact and managerial:

- Current decision: …
- Owner: …
- Next action: …
- Waiting/blocker: …
- Risks/stale/conflicts: …
- Repeated pattern / skill candidate: …

## GitHub evidence to cite

Strong implementation/evidence sources from the May 2026 research pass:

- `vectorize-io/hindsight`: retain / recall / reflect; agents that learn from outcomes, not only retrieve facts.
- `mem0ai/mem0`: ADD-only extraction, entity linking, semantic + BM25 + entity retrieval, temporal reasoning, staleness/decay problems.
- `Tencent/TencentDB-Agent-Memory`: layered memory and “do not hoard everything” principle; memory should reduce repeated steering and improve long-horizon task success.
- `langchain-ai/langmem` + LangGraph patterns: hot-path memory plus background extraction/consolidation.
- `redis/agent-memory-server`: working + long-term memory, lifecycle, summary views, hybrid retrieval, MCP/REST interface.
- `doobidoo/mcp-memory-service`: shared multi-agent memory with graph edges and autonomous consolidation.
- `ALucek/agentic-memory`: working / episodic / semantic / procedural ontology.

## X/social research path

Do not use direct `x.com` scraping as the primary path; Cloudflare makes it unreliable and policy-wise brittle. Preferred path:

1. Use local Perplex/Sonar helper with `search_sources=["social","web"]` for open-ended social research.
2. Use official X tooling such as `xurl` only when authenticated/registered.
3. If concrete X URLs are unavailable, say so explicitly and label conclusions as social/web synthesis, not quoted tweet evidence.

Local Perplex helper quirk discovered during research: when API keys live in `/Users/xbr/.openclaw/workspace/.env`, source them with export enabled so child processes see them:

```bash
set -a
source /Users/xbr/.openclaw/workspace/.env
set +a
PERPLEXITY_SEARCH_SOURCES=social,web PERPLEXITY_TIMEOUT_SECONDS=220 perplex "<research query>"
```

Do not print or store secret values from `.env`; only report presence/absence or `[REDACTED]`.

## Recommended Agentic Stack posture

For the user’s Subconscious lane, keep local `subconscious` as primary and use Hindsight only as staging/benchmark until it beats local recall on sanitized probes. Practical MVP:

1. Append-only decision store (`jsonl` or sqlite).
2. CLI/script to add/list decision records and generate a topic brief.
3. Recall-before-answer hook for important Telegram replies.
4. Stale/conflict scanner.
5. Nightly reflection job that produces skill/runbook candidates.
6. Sanitized benchmark suite comparing local `subconscious` vs Hindsight.

Avoid runtime changes in topic `1347 / Subconscious` unless Mikhail explicitly reassigns execution to Hermes; otherwise Hermes coordinates/reviews and Bud/OpenClaw executes after approval.