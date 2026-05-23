# Agentic Stack v2 Blueprint Research Notes

Session context: Mikhail asked to continue after completing the MM / topic 642 coordination lane DoD, then requested deep research via the local Perplexity helper for the next phase: Agentic Stack v2 / swarm architecture / roles / business automation.

## Durable recommendation

Start with a **centralized supervisor-worker architecture**, not a free-form swarm:

```text
Mikhail / Telegram topic
  -> Hermes / Master Mind (coordinator, planner, policy gate, final answer)
  -> task board + topic policy check
  -> Bud / Research / Reviewer / Policy / Memory / Watchdog roles
  -> Hermes synthesis
  -> Mikhail
```

Reasoning:
- easier to control and audit;
- safer for topic-scoped policies and human approvals;
- fewer runaway agent-agent loops;
- better fit for Telegram ChatOps and the existing MM / topic 642 lifecycle board;
- can later encapsulate domain swarms behind single domain agents.

## Initial 5-7 roles

1. **Hermes / Master Mind** — coordinator, planner, default manager-facing interface, final synthesis.
2. **Bud / OpenClaw** — executor/operator for files, commands, APIs, code, practical implementation.
3. **Research / Retrieval Agent** — web/social/local research, evidence gathering, citations, competitor/market scans.
4. **Reviewer / Critic Agent** — checks quality, consistency, hallucinations, completeness, and manager-readiness.
5. **Policy / Guardrail Agent** — checks allowed actions, approvals, prompt-injection/data-leakage risk, topic policy boundaries.
6. **Memory / Journal Agent** — maintains task summaries, decisions, context windows, knowledge base, topic history.
7. **Watchdog / Supervisor** — detects stuck tasks, missing ACKs, repeated failures, SLA violations, and escalates.

## First business workflow recommendation

Begin with **Research & Briefing**, not high-risk write actions.

Why:
- low side-effect risk;
- quick visible value;
- exercises Research, Reviewer, Memory, and Hermes synthesis;
- fits Telegram delivery well;
- avoids premature automation of money/production/security-sensitive systems.

Candidate workflows after that:
- Sales / Leads Research — closer to revenue, but needs data quality and outreach approval gates.
- Code / Product Ops — good fit for Bud executor, issues/PRs/tests, but can affect repos and should stay supervised initially.

## Governance principles

- Topic policies are first-class. A topic maps to allowed agents, tools, data sources, side effects, approval rules, and reporting style.
- Unknown topics use safe default: do not inherit MM / topic 642 behavior automatically.
- Keep Hermes as the single global coordinator/policy gate while the system is small.
- Agents should have distinct identities and least-privilege tools.
- Human approval is required for irreversible, external, financial, production, or security-sensitive actions.
- Board/watchdog/audit are passive-first unless explicitly promoted.
- Never rely on an LLM prompt alone for policy enforcement; deterministic gates should control tool access and side effects.

## Roadmap shape

### Phase 1 — Blueprint v0.1
- map Telegram topics by visible title + ID;
- define lane policies;
- define initial roles and trust graph;
- choose first workflow: Research & Briefing;
- define acceptance criteria and risks.

### Phase 2 — Low-risk workflow pilot
- implement daily/adhoc Research & Briefing through Hermes;
- add Reviewer check before final report;
- store concise Memory/Journal summaries;
- log lifecycle to board.

### Phase 3 — Supervised business automation
- add Sales/Leads or Code/Product Ops;
- all external sends/writes require approval;
- introduce Policy/Guardrail role.

### Phase 4 — Encapsulated swarms
- only after the baseline works;
- domain swarms appear to Hermes as one role/team;
- internal swarm details stay behind a narrow interface and still obey topic policy.

## Manager-facing reporting preference

For Mikhail, summarize this class of work as: value, result, risks/decisions, and next step. Avoid dumping raw research unless asked. Always reference Telegram topics by visible title plus ID (e.g. `MM / topic 642`, `MM Only / topic 723`) instead of numeric IDs alone.
