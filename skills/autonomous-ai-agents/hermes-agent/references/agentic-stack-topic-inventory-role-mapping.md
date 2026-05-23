# Agentic Stack Topic Inventory + Role Mapping

Session-derived reference for Telegram-centered multi-agent workspaces where Hermes/Master Mind coordinates Bud/OpenClaw and future domain agents.

## Trigger

Use this when Mikhail or another operator asks to design, audit, or extend Agentic Stack across Telegram forum topics, especially after topic-scoped Hermes↔Bud coordination is working and the next question is how to handle existing topics such as HR, Analyst, or Summarize.

## Core lesson

Do **not** start Agentic Stack v2 by adding many agents. Start by inventorying the real Telegram topics and mapping each topic to a lane policy. The real workspace may already have meaningful topical separation, and a good agent architecture should fit that structure rather than impose an abstract swarm design.

## Operating principles

- Treat each Telegram topic as a first-class lane with its own policy.
- Refer to topics by visible title plus ID when available, e.g. `MM / topic 642`, not numeric IDs alone.
- Current approved default across active Agentic Stack topics: Mikhail's messages go to Hermes/MM first; Bud answers Mikhail only when explicitly tagged or when Mikhail replies to Bud; Hermes may delegate Bud in the same topic; visible MM↔Bud discussion should stay human-level, not raw technical chatter.
- `MM / topic 642` is deprecated as the single global coordination lane; keep it only as a migration/control-room lane until queues, logs, watchdogs, and history references are safely moved.
- `MM Only / topic 723` is deprecated; replace with direct messages to `@ceo5000_bot` unless a public Hermes-only archive is explicitly needed.
- Unknown/unregistered topics use safe default: Hermes only if addressed/context requires; Bud silent unless directly requested; passive audit only.
- Bud/OpenClaw should generally remain executor, not default responder, in domain topics.
- Preserve the per-topic skill set that Bud/OpenClaw already used. Topic inventory is incomplete unless it records exact skill names (or closest class-level skills), why they matter, and whether Hermes should load the same skills before answering in that topic.
- Hermes should not be just a mailbox: in domain topics, answer directly when the task is conversational/managerial and the relevant skill set is known; triage/delegate to Bud when the task is execution-heavy, needs scripts/files/board lifecycle, or depends on Bud-specific context.
- Add runtime enforcement only after documented policy, smoke tasks, and passive/dry-run audit prove stable.

## Recommended current lane model

For the detailed 642/723 removal workflow, dependency-audit checklist, migration order, and smoke tests, see `references/agentic-stack-topic-deprecation-migration.md`.

### MM / topic 642

- Lane: deprecated migration/control-room.
- Status: remove as a separate work center after safe migration.
- Why: MM→Bud→MM coordination now belongs inside each domain topic so task context, delegation, discussion, and final answer stay together.
- Temporary uses: routing smoke tests, emergency coordination, architecture/rule migration, tasks with no domain topic.
- Guardrail: before deleting the Telegram topic, confirm no cron deliveries, queue/watchdog/logging paths, or saved links still depend on `642`.

### MM Only / topic 723

- Lane: deprecated Hermes-only public lane.
- Replacement: DM `@ceo5000_bot` for private/strategic Hermes-only communication.
- Keep only if Mikhail explicitly wants a public Hermes-only archive.
- Guardrail: before deleting the Telegram topic, preserve needed decisions/links and confirm no scheduled deliveries or routing rules still target `723`.

### HR

- Lane: HR / people operations.
- Hermes default initially; future HR Agent behind Hermes.
- Bud only for concrete delegated work such as drafts, templates, CV parsing, formatting.
- No autonomous external candidate outreach or hiring decisions without explicit approval.

### Analyst

- Lane: analytics / research.
- Hermes default initially; future Research/Analyst Agent behind Hermes.
- Bud for calculations, scripts, files, API pulls, report generation.
- Good first Agentic Stack v2 pilot: Research & Briefing.

### Summarize

- Lane: summaries / digests.
- Hermes or future Summarizer Agent default.
- Bud silent unless transcript/file/batch-processing automation is needed.
- Beware summarizing sensitive topic content into broader channels without permission.

## Inventory collaboration with Bud/OpenClaw

When the user asks to inventory topics jointly with Bud, or to refresh inventory because topics changed:

1. Re-discover current reality before editing policy: list current messaging targets, inspect `chats.yaml`, and compare against the existing master inventory. Treat mismatches as deltas, not as proof that older Bud-domain topics never existed.
2. Send a visible public handoff in `MM / topic 642`, not only a final-response promise. Use `/task@iq5000_bot correlation_id=<stable-id> max_hops=<n>` when the inventory should have board/watchdog/lifecycle tracking; use direct `@iq5000_bot` only for quick clarifications that do not need a durable task record.
3. Ask Bud to ACK publicly with the same `correlation_id` and then return inventory in chunks if needed. For refreshes, explicitly ask for only the compact delta: `topic_id -> title/purpose`, Bud skill set, Hermes behavior, missing/unknowns.
4. Request these fields for each topic Bud has worked in:
   - topic title + ID;
   - domain/theme/purpose;
   - exact skill names or skill sets used, plus why they matter;
   - conventions/rules for that topic;
   - important decisions, artifacts, repos, commands, boards, watchdogs, integrations;
   - recommended Hermes behavior: answer directly after loading topic skills vs receive/triage/delegate to Bud;
   - when to use direct `@iq5000_bot` vs `/task@iq5000_bot`;
   - concise history summary focused on durable context/procedures, not stale progress;
   - missing context Hermes should fetch from chat history, repo files, skills, boards, or memory.
5. Merge Bud's chunks with Hermes session search, repo references, and existing topic policy docs into a master inventory.
6. If a topic is currently visible to Hermes but not mapped, add it as `documented_only`/safe-default until Bud or the user confirms purpose and skill set.
7. If a previously inventoried topic is not currently visible in Hermes messaging targets, retain it as historical/Bud inventory and mark it "needs confirmation" rather than deleting it.
8. If Bud's ACK arrives but the inventory has not yet arrived, report only that ACK was received and that the master inventory will be produced after the chunks land; do not invent the missing topic history.

### 2026-05 refresh example

- Current Hermes-visible targets were `92`, `723`, `1`, `642`, `1347`, `1346`.
- `1347` mapped to `Subconscious`: Hermes-owned local memory/subconscious development; preserve built-in memory/session_search/skills; use `hermes-agent` for Hermes changes and debugging/TDD/spike skills as appropriate.
- `1346` mapped to `Server-doctor`: ops/runtime diagnostics, incidents, hosts, OpenClaw, Telegram bots, Docker/launchd/systemd, health checks, safe restarts, rollback/postmortems; use the `server-doctor` protocol and do not conflate it with Web Admin.
- Older Bud-domain topics `259`, `584`, `21`, `4`, `488`, and Analyst were retained as historical inventory entries even when not visible in current Hermes targets.

## Minimum policy fields per topic

- `topic_id`
- `topic_name`
- `lane_type`
- `purpose`
- `default_responder`
- `silent_agents`
- `allowed_task_types`
- `forbidden_actions`
- `approval_rules`
- `delegation_rules`
- `audit_level`
- `board_policy`
- `watchdog_policy`
- `escalation_path`
- `data_sensitivity`
- `external_side_effects_policy`
- `human_readable_description`

## Safe topic onboarding checklist

1. Confirm topic title and ID.
2. Add a `documented_only` policy entry.
3. Define purpose, lane type, default responder, silent agents.
4. Define allowed/forbidden actions and approval rules.
5. Run 1-2 manual smoke tasks.
6. Enable passive audit if useful.
7. Enable board tracking for delegated tasks.
8. Only after stability, consider dry-run routing or soft enforcement.

Never automatically apply topic 642 rules to new topics, give Bud default responder status by default, or enable enforcement before behavior is validated.

## Manager-level reporting preference

For Mikhail, summarize value and results first, then risks/decisions and next steps. Keep technical details available but not front-loaded unless asked.

## Deliverable pattern

A good first artifact is a documented-only markdown proposal such as:

`/Users/xbr/.agentic-stack/agentic-stack-v2-topic-inventory.md`

It should include:

- Current Topic Inventory
- Proposed Lane Policy per Topic
- Agent Role Map
- Safe Defaults
- New Topic Onboarding Checklist
- Risks
- First workflow recommendation
