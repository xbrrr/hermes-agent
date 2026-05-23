# Subconscious live recall smoke baseline (2026-05-21)

Context: Agentic Stack / Subconscious topic. Mikhail wanted ongoing improvement of the subconscious layer for autonomy. Bud accepted a read-only p.1 scope: dataset → recall run → expected evidence → pass/fail → short report; no canary/live preflight, no runtime/restart, no cron/routing changes.

## Read-only smoke shape

Use 8–12 real decision cases. For each case capture:

- `query`
- expected evidence/ref (prefer stable decision id or source path)
- actual top-5 recall output
- pass/fail
- fail reason

Metrics:

- case pass rate
- `precision@5` over the actual top-5 slots
- `critical_miss_count`

Report should end with concrete recall/store fixes, not a narrative about the system.

## Baseline result from this session

Engine under test:

```bash
python /Users/xbr/.agentic-stack/subconscious_memory.py recall --topic-id 1347 --query '<query>' --limit 5
```

Baseline:

- cases: 10
- case pass: 0/10
- precision@5: 15/50 = 0.30
- critical miss count: 9
- no writes/runtime/cron/routing changes were made

Main failure:

- `recall()` searched only `working`, `episodic`, `semantic`, and `procedural` layers.
- Key Subconscious decisions lived in `subconscious/decisions.jsonl`.
- Top-5 often returned broad `semantic/topic_policy` or reflection rows instead of the expected decision evidence.

## Cases used

Expected evidence ids:

- `ds_20260519T190823Z_e577554d94ad` — Subconscious provider policy: local primary, Hindsight staging/benchmark.
- `ds_20260519T190823Z_0831ae8b618a` — runtime safety: no live Telegram/Hermes restart without approval.
- `ds_20260519T193412Z_fee0a9bb423c` — Decision State Layer MVP completed.
- `ds_20260520T134324Z_f31624090210` — live preflight verified without service restart.
- `ds_20260520T182812Z_36ecf29aea72` — dryRun whitelist 1347; live stays disabled.
- `ds_20260520T183858Z_416f3ddc106f` — Subconscious remains active; live/canary needs separate decision.
- `ds_20260520T190430Z_8cc978ba72d1` — MM+Bud/topic 642 deleted/retired; no new handoffs.
- `ds_20260521T172527Z_6df5c4ebbcd1` — weekly consciousness report format and metrics.
- `ds_20260521T172527Z_97794ce6781e` — Bud critique gate for major Subconscious changes.
- `ds_20260521T081148Z_ea3e2ee7a5e4` — deterministic quality review loop and Hindsight boundary.

## Fix direction for next iteration

Do not start a large benchmark before fixing the baseline miss. Start with:

1. Include `decisions.jsonl` in recall surface.
2. Add query-aware scoring over `subject`, `statement`, `owner`, `next_action`, and `evidence_refs`, strictly scoped by `topic_id`.
3. Rank concrete decision evidence above broad topic-policy/reflection rows.
4. Convert these 10 cases into a deterministic smoke once the recall implementation is patched.

Guardrail: this is an eval/store improvement path, not permission to enable canary/live preflight or restart runtime.