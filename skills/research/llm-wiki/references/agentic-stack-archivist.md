# Agentic Stack Archivist Pattern

Use this reference when designing or operating an Agentic Stack / Hermes↔Bud project archivist.

## Trigger

The user wants a project/topic/archive memory agent, topic inventory, skill map, runbook index, or research-backed documentation system for Agentic Stack.

## Correct workflow

1. First verify the required research/tooling path instead of falling back silently.
   - For open-ended X/Twitter/social research, use Perplex/Sonar with `search_sources=["social","web"]`.
   - On this setup, the helper is normally `/Users/xbr/.local/bin/perplex`; if the key is missing from the current shell, load `/Users/xbr/.openclaw/workspace/.env` without printing secrets.
   - For exact X URLs, use the configured X/Bird path; if `xurl` has a PATH collision, resolve to the official X CLI binary instead of declaring X unavailable.
2. If the first research/source step is blocked, fix or ask Bud to verify the path, then rerun. Do not produce a large fallback report that will need to be redone.
3. Keep Telegram replies compact: conclusion + deltas + file path. Put longer evidence in a markdown artifact.
4. Preserve provenance: record which sources were GitHub, Perplex social/web, X/search-index fallback, or Bud verification.

## Recommended Archivist MVP

Create a local-first markdown wiki under:

```text
/Users/xbr/.agentic-stack/wiki/
  SCHEMA.md
  index.md
  log.md
  sources/manifest.jsonl
  topics/
  skills/
  runbooks/
  systems/
  decisions/
```

Initial ingest should be curated/local only:

- `/Users/xbr/.agentic-stack/chats.yaml`
- `/Users/xbr/.agentic-stack/agentic-stack-v2-topic-inventory.md`
- selected local `SKILL.md` files
- curated summaries, not raw private logs

Hard rules:

- no external uploads by default;
- denylist `.env`, tokens, private keys, auth files, raw gateway logs;
- source manifest includes path, type, sha256, timestamp, redaction status;
- important claims need provenance;
- run lint/check before publishing or syncing summaries.

## Research signals to cite briefly

GitHub:

- `SamurAIGPT/llm-wiki-agent` — persistent interlinked markdown wiki maintained by coding agents.
- `swarmclawai/swarmvault` — local-first LLM Wiki + graph/RAG/agent memory.
- `coleam00/claude-memory-compiler` — compiles agent-session decisions/lessons into knowledge articles.
- `agentskills/agentskills`, `tech-leads-club/agent-skills`, `iflytek/skillhub` — skill registry/spec/governance references.
- `GoPlusSecurity/agentguard` — skill/security scanning reference.

X/social:

- Social discussion confirms the trend: Karpathy LLM Wiki, Obsidian/native memory for coding agents, and skill registries/security.
- When Perplex social/web does not return exact X post URLs, use a clearly labeled search-index fallback such as `site:x.com` snippets; do not claim live X verification.

## Output style for Mikhail

Prefer this shape:

```text
Done: <artifact path>
Key delta:
- <3-6 bullets>
Recommendation: <one sentence>
```

Avoid dumping long research in Telegram. Save it to `references/`, `/Users/xbr/.agentic-stack/research/`, or the wiki and link the path.