# Subconscious manager-readable report criteria — 2026-05-22

Session signal: Mikhail objected that the Subconscious report looked like a technical delivery/status log: “мы просто что-то сделали”. The correction is class-level for Agentic Stack/Subconscious reports.

## Required standard

A Subconscious report is not successful because cron ran or delivery worked. It is successful when a non-technical manager can understand whether the agent memory system became more useful.

Use this 30-second reader test:

- What became better?
- What became worse or remains weak?
- What is the agent's hypothesis?
- What does the agent propose next?
- How does this reduce Mikhail's manual steering?
- What changed compared with yesterday/last week?

If those questions are not answered, the output is a technical delivery report, not a Subconscious report.

## Required content blocks

For weekly consciousness reports:

- выводы: what was learned or understood;
- гипотезы: why this happened / what may improve the system;
- предложения: 2–3 concrete improvements;
- цели: e.g. better recall, less repeated steering, higher autonomy;
- задачи: what will be done next;
- прогресс: what changed since the last report;
- слабые места: what remains primitive, risky, or unresolved;
- следующий шаг: one concrete next action.

For daily morning reports: keep 3–6 bullets, but still include insight and next action. Do not let “short” collapse into “technical status only”.

## Metrics that matter

Prefer usefulness metrics over job mechanics:

- recall precision@5 / top-5 relevance;
- quality probes;
- hard-negative cases for confusing similar decisions;
- stale/conflict/blockers;
- learning yield — what became a rule, skill, check, or runbook;
- reduction in repeated corrections/manual steering from Mikhail.

## Anti-patterns

- Main text dominated by cron/job/delivery/path/log details.
- “Что реально сделано” without “what it means”.
- A report whose only honest conclusion is `мы просто что-то сделали`.
- Reporting that a script ran, without hypothesis, impact, or next task.
- Treating delivery troubleshooting as a Subconscious progress report.

## Rewrite rule

If the first draft is technical, do not ship it. Rewrite it as:

1. conclusion/verdict;
2. hypothesis about the system/user benefit;
3. evidence/progress in human terms;
4. weak spot or blocker;
5. proposed improvement;
6. next concrete task/owner/trigger.

Keep technical evidence in a short appendix or internal artifact unless the user asks for logs.