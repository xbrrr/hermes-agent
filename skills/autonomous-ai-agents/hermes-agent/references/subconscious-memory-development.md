# Hermes “Subconscious” / Agent Memory Development Notes

Use this reference when the user asks how Hermes' subconscious, memory, self-improvement, or long-term cognition should evolve.

## Current Hermes baseline

Hermes' built-in subconscious is a combination of:

- **Built-in curated memory**: `~/.hermes/memories/MEMORY.md` and `USER.md`, injected as a frozen system-prompt snapshot at session start.
- **Session search**: SQLite/FTS5 transcript recall on demand, separate from always-on memory.
- **Skills**: procedural memory / reusable workflows.
- **MemoryManager + plugins**: provider lifecycle hooks (`prefetch`, `queue_prefetch`, `sync_turn`, `on_session_end`, `on_pre_compress`, `on_memory_write`, `on_delegation`). Only one external provider is active at a time, alongside built-in memory.
- **Cron/delegation**: background reflection, audits, and long-running consolidation loops.

Baseline limitation: built-in memory is compact and manually curated; without an external provider or reflection job, Hermes mostly remembers key facts rather than actively learning from outcomes.

## Useful external patterns found in agent-memory repos

- **CHIP Memory Service** (`Cheffromspace/chip-memory-service`): hybrid Redis hot cache + PostgreSQL/pgvector long-term store + local embeddings. Memory types include stream events, user relationships, personality/lore, and episodic memories. Good model for agent personality and relationship continuity.
- **Hindsight** (`vectorize-io/hindsight`, ~13.7k stars as of May 2026): focuses on agents that learn, not just recall. Pattern: retain / recall / reflect; exposes wrapper/API/SDK and positions itself as benchmark-oriented memory for long-horizon agents.
- **TencentDB Agent Memory** (`Tencent/TencentDB-Agent-Memory`, ~3.2k stars as of May 2026): symbolic short-term memory for heavy tool logs plus layered long-term memory for personas/scenes/workflows. Key principle: do not hoard everything; use memory to reduce repeated human steering and improve reasoning. Reports large token reductions and pass-rate gains in long-horizon OpenClaw-style runs.
- **Mem0** (`mem0ai/mem0`, ~56k stars as of May 2026): mature universal memory layer with user/session/agent state, multi-signal retrieval, memory decay/recency ranking, and self-hosted/cloud options.
- **mcp-memory-service** (`doobidoo/mcp-memory-service`, ~1.8k stars as of May 2026): practical shared memory backend with REST + MCP + OAuth + dashboard, knowledge graph, typed edges, and autonomous consolidation.
- **LangMem** (`langchain-ai/langmem`, ~1.4k stars as of May 2026): functional primitives + LangGraph store integration; agent-managed memory tools plus background extraction/consolidation.
- **Redis Agent Memory Server** (`redis/agent-memory-server`): practical production pattern — working + long-term memory, extraction strategies, semantic/keyword/hybrid search, async workers, REST + MCP.
- **ALucek agentic-memory**: useful ontology — working, episodic, semantic, procedural memory.
- **Neo4j-style graph memory**: graph-native memory with short-term history, long-term knowledge graph, reasoning memory, and audit edges from reasoning steps to entities.
- **YourMemory**: forgetting-curve / decay model; important facts stick, stale facts fade or get replaced.

## Social/X signals from May 2026 rerun

Direct `x.com` scraping is Cloudflare-prone; prefer official `xurl` when authenticated, otherwise use search-index snippets as a fallback. In this environment `/Users/xbr/.local/bin/xurl` was actually the unrelated `xurls` URL extractor, so the official X CLI was installed locally at `/Users/xbr/.local/opt/xdev-xurl/node_modules/.bin/xurl`; `xurl auth status` showed no registered apps, so authenticated X search was unavailable until the user registers an app.

Signals found through X-index search:
- Dair/DAIR.AI posts emphasize that long-horizon agents lose relationships between facts, not just facts; graph-augmented memory and periodic consolidation are recurring themes.
- Tencent AI posts promote four-layer progressive memory, persistent task context, preferences, and reduced token usage.
- Mem0 posts emphasize open-source long-term personalized memory and memory decay/recency ranking.
- Hindsight/Vectorize posts emphasize “learns over time,” Vercel AI SDK integration, retain/recall/reflect, and benchmark claims.
- Practitioner posts around Hermes/OpenClaw explicitly call long-term memory a prerequisite for “Jarvis”-style agents and value Hindsight/Mem0-like systems.
- Voice-agent posts recommend semantic retrieval for unstructured episodic memory, but not during the active turn; extract/consolidate after the turn.
- Hermes/OpenClaw community posts distinguish memory = durable facts, sessions = what happened, skills = procedural memory.

## Recommended Hermes subconscious roadmap

### Phase 1 — Activate learning substrate

1. Choose one external provider:
   - **Mem0** for fastest mature production memory.
   - **Hindsight** when the priority is learning from outcomes and reflection.
2. Add a daily/periodic `subconscious-reflection` cron job that reviews recent sessions and proposes:
   - durable memory updates;
   - skill patches;
   - stale/conflicting entries to replace;
   - unresolved blockers or recurring mistakes.
3. Keep built-in `MEMORY.md`/`USER.md` as the compact always-on control layer; use external memory for high-volume recall.

**Do not switch memory providers just because Hindsight/Mem0 plugin files exist.** First verify actual readiness:

- `hermes memory status` for active provider and plugin availability.
- Python/import readiness for provider deps (`hindsight`, `hindsight_client`, `mem0`, `mem0ai`, etc.).
- Hindsight cloud needs `HINDSIGHT_API_KEY` from `https://ui.hindsight.vectorize.io` or an explicit `HINDSIGHT_API_URL`.
- Hindsight local embedded needs `hindsight-all` plus an LLM backend/key (`HINDSIGHT_LLM_API_KEY` or OpenAI-compatible endpoint). It can be heavy; do not install into the live Hermes venv without explicit approval.
- Hindsight local external needs a running instance, commonly checked at `localhost:8888` or configured URL.

Safe default for this user's Hermes subconscious work: keep active `subconscious` as the main provider, run Hindsight in a separate staging env/instance, export/bridge topic-scoped memories into it, then compare retain/recall quality before any provider switch.

### Phase 2 — Layer memory by cognitive role

Represent memory explicitly as:

- **Working memory**: active thread state, current goal, pending decisions, blockers.
- **Episodic memory**: important events, task outcomes, failures/recoveries, agent-agent handoffs.
- **Semantic memory**: durable facts about users, projects, systems, architecture, roles.
- **Procedural memory**: skills, playbooks, protocols, debugging recipes.

### Phase 3 — Make recall topic-aware

For messaging/group-agent deployments, recall should be scoped by platform, chat, thread/topic, user, and profile. Before answering in a topic, fetch:

- topic-specific rules;
- active goal;
- last handoff / open tasks;
- relevant user/project facts;
- recent unresolved blockers.

For Agentic Stack topic `1347 / Subconscious`, respect the coordinator/executor split: Hermes coordinates, reviews, and proposes the direction; Bud/OpenClaw implements after approval/ACK. Do not silently take execution-heavy implementation work back from Bud. Handoffs should be public in-topic with a `correlation_id`, and Hermes should verify Bud's report with lightweight smoke checks before telling Mikhail the work is done.

### Phase 4 — Add forgetting and hygiene

Add metadata to non-built-in memory stores:

- confidence;
- source/session id;
- scope (global/user/project/topic);
- last verified time;
- TTL or decay policy;
- supersedes/conflicts-with links.

Avoid flat vector piles. Prefer layered summaries plus graph/entity links plus hybrid search.

## Reporting guidance

When explaining Hermes' subconscious to the user, start with a plain-language layer:

- what exists now;
- what is missing;
- what to enable first;
- the practical roadmap.

Keep implementation details second, unless the user explicitly asks for code-level detail.
