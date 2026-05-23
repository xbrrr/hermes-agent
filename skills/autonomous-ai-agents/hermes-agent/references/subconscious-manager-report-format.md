# Subconscious manager-report format

Use this when generating daily/weekly Subconscious reports or summarizing Subconscious progress for Mikhail.

## Trigger

- Mikhail asks for today's Subconscious report, progress, review, or what improved.
- A cron/Subconscious report contains mostly technical status, paths, probes, or green checks.
- The report is meant for a non-technical manager/humanitarian reader.

## Required shape

Start with the decision-level conclusion, not logs.

1. **Итог** — one sentence: what actually changed and whether it matters.
2. **Конкретные улучшения** — each item must say:
   - what changed;
   - what it gives the user/agents;
   - whether it is already active or only a foundation.
3. **Что слабое / риск** — name the architectural or product gap, not just failed tests.
4. **Что дорабатывать дальше** — concrete next architecture/product work.
5. **Approval boundary** — mention only if a user decision is needed.

## Avoid

- Raw cron output, file paths, report paths, job IDs, and script names unless explicitly requested.
- Metrics that do not mean anything to the user. If a metric is included, translate it into a user-facing consequence.
- “Everything is green” as a conclusion.
- Saying “we did something” without explaining what capability improved.
- Repeating unproven architecture tracks such as Hindsight in routine reports unless there is a new benchmark/result/decision.

## Good phrasing pattern

- `Decision State Layer: decisions are separated from chat noise. This gives agents a preflight source before answering, so Mikhail should need fewer repeated corrections. Still MVP: live dialogue usage is not yet proven.`
- `Weak spot: probes prove that facts exist, not that the agent uses them well in real turns.`
- `Next architecture work: separate ingest, decision store, retrieval/preflight, reporting, and evaluation into explicit contracts.`

## Bad phrasing pattern

- `Quality probes 10/10, recall precision@5 1.00, conflicts=0.`
- `Cron ran successfully and wrote reports to ...`
- `We improved hygiene.`

Translate every technical fact into: **what changed, why it matters, what remains weak, what we do next**.