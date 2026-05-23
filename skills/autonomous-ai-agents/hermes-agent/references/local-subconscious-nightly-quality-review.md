# Local subconscious nightly quality review

Use this when improving or auditing the local subconscious morning/daily report.

## Pattern that worked

For `subconscious-morning-report`, avoid a report that only says the database was cleaned. The useful shape is a product-style memory health review:

1. Soft hygiene only: down-rank obvious tool-output/raw-log/cron noise; do not delete records from an automated nightly pass.
2. Add recall quality probes over durable operating decisions, not generic counters.
3. Report probe pass/fail in human terms: what the memory remembers, which decision is weak, what to fix next.
4. Keep Hindsight separate: local subconscious remains the active provider; Hindsight is staging/benchmark unless explicitly switched.
5. Name the limitation: lexical probes prove evidence exists in memory, not that the agent will answer correctly in a live turn.

## Good probe classes

Use 5-7 probes over decisions that cause repeated user steering if forgotten:

- topic/routing boundaries: Server-doctor, Subconscious, Web Admin, Coding, Picasso;
- deleted/retired topics and DM fallback;
- critical-collaboration/no-sycophancy style;
- local subconscious vs Hindsight provider policy;
- explicit bot mention overriding reply-context;
- Subconscious topic scope: memory/recall/reflection/decision preflight only;
- live runtime restart/canary guardrails.

## Cron prompt guardrails

The cron agent should produce a concise Russian manager-readable report with:

- one-line outcome;
- what improved or was cleaned;
- quality-probe result and weak probes;
- where Mikhail will feel the benefit;
- what remains weak;
- max three recommendations.

Explicitly say this is not a Hindsight benchmark. Do not switch providers, restart services, expose raw Telegram/log data, or print secrets.

## Verification

Before reporting completion:

- run `python3 -m py_compile <script>`;
- run the script directly and inspect the first report output;
- verify the cron job still points to the script, schedule, and delivery target intended;
- check the prompt contains quality probes and Hindsight separation language.

Useful local commands in Agentic Stack:

```bash
cd /Users/xbr/.agentic-stack
python3 subconscious_memory.py quality-probes --topic-id 1347
python3 subconscious_memory.py recall-hard-negatives --topic-id 1347
python3 subconscious_memory.py weekly-consciousness-report --topic-id 1347
python3 /Users/xbr/.hermes/scripts/subconscious_weekly_consciousness_report.py
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

Weekly report cron is expected to use `subconscious_weekly_consciousness_report.py` as a `no_agent` script and deliver to `telegram:-1003772186616:1347`. The report must stay under 40 lines and include: background reflection, improvements, autonomy impact, next actions, quality probes, hard-negative probes, and precision@5.

## Live recall smoke upgrade pattern

When lexical probes pass but live answers still miss decisions, upgrade recall in a TDD loop rather than adding more generic memory:

1. Pick 8-12 real user-facing questions whose answers depend on durable decisions (`retired/deleted topics`, topic boundaries, provider policy, restart/canary guardrails, routing ownership).
2. Define expected evidence and top-k acceptance before changing code; include at least one critical-miss class where a wrong answer would cause repeated user steering.
3. Run the smoke against the same recall path used in live answers, not only a database grep.
4. If the durable decision log exists, include topic-scoped `decisions.jsonl` records in recall and rank concrete decisions above generic topic/reflection rows.
5. Keep the old memory-layer recall as fallback; do not break topic isolation or graph/hybrid recall while boosting decision evidence.
6. Verify with targeted tests, full relevant tests, `py_compile`/self-test where applicable, and a before/after smoke summary: pass count, critical misses, and proxy precision@k.
7. Ask Bud/OpenClaw for public review/execution in Agentic Stack topic `1347 / Subconscious` when this is runtime/file work in that lane; Hermes reports final green only after review/verification.

## Pitfalls

- A `7/7 probes passed` result is not production-grade semantic recall. Treat it as a baseline guard. The next level is a live recall smoke: ask a real question, compare the generated answer with an expected answer, and only then claim live-answer quality improved.
- A green smoke is still an incomplete management update if it lacks `что дальше`. Always include 1-3 concrete next steps or experiments, even when all probes pass.
- Weekly consciousness reports are not just cron heartbeats. They must say what was reflected in background checks, what improved, how autonomy/interaction efficiency changed, and what to improve next.
