# Agentic Project Archivist MVP

Use this reference when turning a multi-agent project/chat/workflow into a local-first archived knowledge base.

## Trigger

- User asks for an "agent archivist", project memory, topic inventory, skill map, runbook index, or agent-maintained documentation.
- The project has multiple Telegram/Slack/Discord topics, agents, skills, runbooks, and evolving coordination rules.

## Recommended MVP

Create a dedicated project wiki, e.g.:

```text
<project>/.agentic-stack/wiki/
  SCHEMA.md
  index.md
  log.md
  raw/
    telegram/
    github/
    transcripts/
    decisions/
  entities/
  concepts/
  systems/
  topics/
  skills/
  runbooks/
  comparisons/
  queries/
```

Initial outputs:

1. `topics/<project>-topics.md` — topic/channel inventory and purpose.
2. `skills/topic-skill-map.md` — topic → skill/context bindings.
3. `runbooks/index.md` — runbook catalog and owners.
4. `systems/<agent-system>.md` — architecture map of agents, gateways, queues, bots.
5. `concepts/decisions-and-policies.md` — durable coordination rules and decisions.
6. `queries/` pages for substantial synthesis answers worth keeping.

## Safe source policy

Start with curated, local sources:

- topic inventories and `chats.yaml`-style source-of-truth files
- `AGENTS.md`, `CLAUDE.md`, `README.md`, docs folders
- `SKILL.md` files and runbooks
- curated chat summaries, not raw full chat logs by default

Do not ingest by default:

- `.env`, auth files, token files, private keys, browser profiles
- raw gateway/runtime logs likely to include tokens
- private chat exports without explicit approval and redaction
- cloud/NotebookLM/external MCP uploads unless explicitly approved

Before writing raw/private content, apply secret redaction for API keys, Bearer tokens, Telegram bot tokens, SSH/private keys, passwords, DB URLs, and webhook secrets. Maintain a source manifest with `source_path`, `source_type`, `sha256`, and `redaction_status`.

## Agent division of labor

- Coordinator agent: schema/taxonomy, synthesis, approval of broad scans, contradiction resolution.
- Executor agent: file scans, ingestion, wiki page updates, lint reports, graph/build artifacts.
- Human approval: broad repo scans, external uploads, publishing docs, or ingesting private chat logs.

## Useful related skills/tools

- `llm-wiki` for schema/index/log/raw/wiki mechanics.
- `obsidian` when the wiki should also be browsable as an Obsidian vault.
- `hermes-agent-skill-authoring` for skill inventories and skill updates.
- repo inspection/documentation tools only as optional batch inputs; keep the wiki as the canonical human-readable artifact.

## Verification checklist

- [ ] `SCHEMA.md`, `index.md`, and `log.md` exist.
- [ ] Every created page appears in `index.md`.
- [ ] `log.md` records source files and generated/updated pages.
- [ ] Raw/private source policy is documented in `SCHEMA.md`.
- [ ] Source manifest exists for private/local ingests.
- [ ] No obvious secrets are present in generated wiki pages.
- [ ] Topic inventory, skill map, runbook index, and system map are present.
