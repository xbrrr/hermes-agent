---
name: harness-setup-audit
description: "Use when auditing or setting up AI-agent operating infrastructure: turning scattered prompts/rules into skills, mapping Hermes/Bud roles, AGENTS.md/CLAUDE.md, evals, vault/rules structure, safe MCP/tool boundaries, and monthly health checks. Do not use for ordinary one-off coding/chat tasks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [harness, skills, evals, agentic-stack, audit, safety]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# Harness Setup Audit

## Overview

A conservative, runtime-safe extraction from `AIM-harness-setup.md` for Agentic Stack / Hermes-Bud infrastructure work.

Purpose: provide an audit/playbook for AI-agent operating infrastructure without installing unverified scripts, external automation, or broad claims as runtime truth.

Core frame:

- **Operator**: human/coordinator deciding goals, boundaries, owners, evaluation.
- **Harness**: system prompts, routing, skills, permissions, lifecycle, telemetry.
- **Tools**: terminal, files, APIs, MCP, browser, messaging, cron, delegation.
- **Environment**: repos, vaults, servers, chats, processes, credentials.
- **Model**: replaceable capability behind the harness.

## When to Use

Use when the user asks to:

- organize scattered prompts, rules, notes, or procedures into reusable skills;
- audit Hermes/Bud/OpenClaw roles, routing, topic rules, or task boundaries;
- set up or refactor `AGENTS.md`, `CLAUDE.md`, vault/rules folders, evals, or health checks;
- decide which workflows should become skills;
- review AI-agent infrastructure after drift, incidents, or growth;
- prepare onboarding/playbook material for a team using agents.

Do **not** use for:

- one-off answers, coding tasks, or ordinary debugging;
- installing new MCP servers or tools without explicit user approval;
- claims/facts that need current verification unless independently checked;
- secret handling beyond safe review and redaction recommendations.

## Safety Defaults

1. **Do not install executable scripts from this skill.** Treat scripts from source documents as examples until reviewed.
2. **Do not copy secrets into skills, AGENTS.md, notes, eval cases, or logs.** Replace with placeholders like `<API_KEY>`.
3. **Do not grant broad write access to MCP/tools by default.** Prefer read-only, sandboxed, and allowlisted scopes.
4. **Do not treat external benchmark numbers as local truth.** Use them only as hypotheses to test locally.
5. **Do not enable this for every request.** It is for infrastructure/audit work only.
6. **Before live runtime changes**, make a reversible plan and verify with smoke tests.

## Procedure

### 1. Context discovery

Capture briefly:

- current goal;
- human owner / decision maker;
- active agents and roles;
- main recurring AI tasks;
- where rules/prompts currently live;
- known risks: secrets, live services, routing, credentials, cost.

### 2. Inventory before building

Map what already exists:

- chats/topics and routing rules;
- skills and their owners;
- memory/session-search/notes/vault files;
- repo-level `AGENTS.md` / `CLAUDE.md`;
- MCP/tools and permissions;
- cron/watchdogs/kanban/task queues;
- evals, smoke tests, telemetry;
- credential locations and redaction boundaries.

For Agentic Stack topic inventory refreshes, use `references/agentic-stack-topic-inventory.md`: start from `/Users/xbr/.agentic-stack/chats.yaml` and `/Users/xbr/.openclaw/workspace/chats.md`, reconcile with Bud's public compact delta, parse Telegram `/c/<chat>/<topic>/<message>` links for topic IDs, and mark unresolved conflicts as unknown/history instead of guessing. If a final cleanup/alignment is obvious, execute it immediately (update docs, send Bud alignment, validate) rather than ending with “I would do next…” suggestions.

Output as bullets, not a table if replying on Telegram. For Mikhail, keep the final answer ultra-concise: changed files, verified status, current mapping, remaining blockers only.

### 3. Choose only the first 3 skill candidates

Select candidates by:

- repeated at least weekly;
- takes >5 minutes to explain manually;
- has stable inputs and quality criteria;
- can be safely delegated or audited;
- benefits from persistent procedure.

Avoid mass-generating skills. Draft, test in real use, then curate.

### 3a. Skill inventory and topic-scoped adoption

When Mikhail asks whether a skill should be enabled "everywhere" or asks for skill-library inventory:

- inventory first: installed skills by category, actual `skill_view`/cron-load usage, curator sidecar usage, and unused/niche groups;
- treat low usage as a triage signal, not proof a skill is useless;
- prefer topic/lane bindings over global auto-loads;
- keep the global always-on skill set small to avoid context bloat and process overhead;
- for heavy coding workflow imports such as `shaw`, recommend a Coding/Web Admin pilot before any default binding;
- do not execute or install imported scripts until reviewed and adapted for the active runtime.

For the concrete 2026-05-21 Shaw/coding-workflow audit and adoption rule, see `references/skill-inventory-and-shaw-adoption-20260521.md`.

### 4. Create or update minimal artifacts

Prefer small, composable files:

- short `SKILL.md` with trigger-focused description;
- references in `references/`;
- templates in `templates/`;
- reviewed scripts only in `scripts/`;
- local project rules in `AGENTS.md` / `CLAUDE.md`;
- eval cases only after workflow is stable.

### 5. Health check loop

Run monthly or after major changes:

- skill descriptions still match triggers;
- stale/duplicate skills identified;
- links and references checked if used;
- tool/MCP permissions still minimal;
- routing rules still match topic expectations;
- eval/smoke tests still green;
- token/cost or runtime regressions noticed;
- secrets absent from generated artifacts.

### 6. Agent memory / recall evals

When auditing a memory or recall layer (for example Agentic Stack Subconscious), do not treat a broad quality probe as proof of useful recall. Build a small read-only live recall smoke first:

- 8–12 real decision cases;
- query + expected evidence/ref + actual top-5;
- pass/fail + fail reason;
- `precision@5` and `critical_miss_count`;
- concrete store/scoring fixes as output.

For the Subconscious baseline and failure pattern (`recall()` missed `decisions.jsonl` and over-ranked broad topic-policy/reflection rows), see `references/2026-05-21-subconscious-live-recall-smoke.md`.

When working with the Agentic Stack local TODO system (`~/.agentic-stack/local-todo.md` and daily reminder script), follow the user-validated format requirements in `references/agentic-stack-local-todo-format.md` — especially stable unique IDs for every task, unified numbering (no split lists), and work-focused task titles that avoid infrastructure component name collisions.

## Output Format

For user-facing replies, keep it concise:

- **What we have**: current state.
- **Gap**: what is missing or risky.
- **Top 3 actions**: highest leverage next steps.
- **Safety notes**: secrets/permissions/runtime risks.
- **Verification**: how we know it worked.

## Quality Checks

- [ ] No secrets copied into artifacts or logs.
- [ ] No unreviewed script/tool/MCP installed.
- [ ] Description of any new skill is trigger-focused and ≤1024 chars.
- [ ] Claims are marked as verified locally, external claim, or hypothesis.
- [ ] Live runtime changes have smoke verification.
- [ ] Output is actionable and short enough for Telegram.
- [ ] If the change should affect Bud/OpenClaw, confirm whether the skill/config was also synced to `/Users/xbr/.openclaw/workspace/skills/` or explicitly state that only Hermes was updated.
- [ ] If a recurring health check is requested, schedule it as read-only by default: no restarts, installs, edits, or secrets in output unless Mikhail separately approves.

## Common Mistakes

- Treating a long article as a runtime skill.
- Building new infrastructure before inventorying existing rules/skills.
- Installing automation from a reference document without review.
- Making skills too broad, too many, or too generic.
- Confusing coordinator methodology with executor instructions.
- Letting secrets leak into examples, eval cases, or debug logs.

## Provenance

Derived conservatively from user-provided `AIM-harness-setup.md` on 2026-05-18.

Excluded on purpose:

- embedded refresh automation;
- unverifiable/fresh external references;
- hard benchmark claims as runtime rules;
- broad MCP install recommendations;
- AIM-private operational details beyond the general method.
