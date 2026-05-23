# Local subconscious + Hindsight staging pattern

Use this reference when developing Hermes' "subconscious"/long-term cognition stack, especially in Agentic Stack topic `1347 / Subconscious`.

## Recommended architecture

- Keep Hermes' built-in memory as the compact control layer: durable user preferences, stable environment facts, and small hand-curated notes.
- Keep `session_search` for transcript recall, not durable semantic memory.
- Keep skills as procedural memory: reusable workflows, fixes, and quality gates.
- Use the local `subconscious` provider as the default/main memory backend when it is active and healthy.
- Treat Hindsight as a benchmark/staging candidate or secondary brain until it proves better than local `subconscious` on sanitized smoke tests.

## Local `subconscious` quality layer

Useful features to preserve and verify:

- Layered memory: `working`, `episodic`, `semantic`, `procedural`.
- Topic-aware recall: pass or preserve `chat_id`, `topic_id`, `platform`, `layer`, and tags so Agentic Stack topics do not bleed together.
- Hybrid/graph recall: combine direct text matches with graph neighbors/edges.
- Ranking: combine confidence, recency, topic scope, graph weight, and soft decay.
- Dedup: normalize text and hash by `layer/topic/chat/platform/text`.
- Forgetting: prefer soft decay/re-ranking over destructive deletion.
- Skill promotion: produce candidate lists for review; do not auto-create skills without human/agent review.
- Night reflection: cron can run deterministic local consolidation; morning reports should be short and action-oriented.

## Hygiene and cleanup rules

Nightly reflection and skill-candidate extraction should improve memory quality, not simply store more text:

- Do not promote raw tool outputs, JSON blobs, cron dumps, path lists, exception payloads, or copied `/task` messages as procedural memory or skill candidates.
- Prefer distilled facts: decision, owner, next action, invariant, reusable procedure, or explicit user preference.
- Mark noisy/low-confidence/malformed memories with lower confidence/soft decay before considering deletion.
- Use destructive cleanup only after review/approval; default to soft cleanup and re-ranking.
- Report cleanup in human terms: "почистили технический шум", "нашли устаревшее решение", "есть кандидат на skill" rather than database counts.
- A good subconscious review should answer: what is useful, what is stale/noisy, what should become a skill, and what improvement would make future answers better.

## Hindsight decision rule

Hindsight is **not automatically required** if local `subconscious` already provides topic-aware graph/hybrid recall. Use Hindsight only if staging shows clear value, e.g. better entity resolution, richer graph recall, or useful UI/inspection.

Avoid switching Hermes' main provider until all criteria pass:

1. Staging retain works.
2. Staging recall works.
3. Topic metadata survives export/import.
4. Recall quality is better than local `subconscious` on sanitized samples.
5. Rollback/stop commands are documented.
6. A controlled restart window is approved if provider switch is needed.

## Fully local/no-pay Hindsight path

The safest privacy posture is local Hindsight plus local LLM backend:

- Hindsight mode: `local_external` preferred for staging.
- Run it in an isolated environment outside the live Hermes venv, e.g. `~/.hermes/staging/hindsight-local/.venv`.
- Bind services to localhost only, e.g. Hindsight `127.0.0.1:8888`, Ollama `127.0.0.1:11434`.
- Do not use Hindsight Cloud or `HINDSIGHT_API_KEY` for local-only staging.
- Do not send raw Telegram history, secrets, or full logs; retain only sanitized summaries/samples.
- On a 16 GB Mac mini, a viable starter backend is Ollama + `qwen2.5:7b`; avoid larger models without explicit approval.

Example staging env variables:

```bash
export HINDSIGHT_MODE=local_external
export HINDSIGHT_API_URL=http://127.0.0.1:8888
export HINDSIGHT_BANK_ID=hermes-local-staging
export HINDSIGHT_RETAIN_TAGS=staging,sanitized,subconscious

export HINDSIGHT_API_LLM_PROVIDER=ollama
export HINDSIGHT_API_LLM_BASE_URL=http://127.0.0.1:11434/v1
export HINDSIGHT_API_LLM_MODEL=qwen2.5:7b
```

Approval-gated setup commands may include:

```bash
brew install ollama
ollama serve
ollama pull qwen2.5:7b
cd ~/.hermes/staging/hindsight-local
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip uv
uv pip install hindsight-api
hindsight-api --host 127.0.0.1 --port 8888
```

## Morning report / subconscious review pattern

For local subconscious maintenance, a useful daily report prompt should be a **review**, not a technical heartbeat:

- Use the user's expected timezone for schedules and report language; for Mikhail/Agentic Stack use Moscow time (MSK), even if the host clock is another timezone.
- Write in Russian, manager-to-manager style: short, human, decision-oriented.
- Lead with the business summary: green/yellow/red, what changed, what it means, what decision/action is needed.
- Include recommendations: what to improve, what to clean up, what to turn into a skill/runbook, and what to watch next.
- Separate three concepts clearly:
  - `silent sampler` = local data collection / health snapshots; should usually not be shown to the user.
  - `subconscious report` = daily human review of memory quality, decisions, stale/noisy items, and next actions.
  - `Hindsight comparison` = separate benchmark/staging report; do not let it replace the local subconscious review.
- Check provider/cron/self-test status only as evidence, not as the main content.
- Summarize what changed overnight.
- List important new memories/decisions, unresolved blockers, and skill candidates.
- Recommend 1–3 next actions. Do not omit the "what next" section: Mikhail explicitly treats missing next steps as an incomplete report, even when the smoke result is green.
- For weekly "сознание / subconscious" reports, include manager-readable blocks: `что обдумано фоном`, `что улучшено`, `выводы`, `гипотезы`, `цели/задачи/прогресс`, `что это меняет для самостоятельности`, and `что сделать дальше`. The point is continuous improvement of interaction efficiency and agent autonomy — not just a status digest.
- Daily/weekly loops should include at least one concrete improvement candidate or experiment when probes justify it: recall precision, stale/noisy memory cleanup, skill-candidate promotion, decision preflight, background checks, or architecture/reflection tuning.
- A Subconscious report fails manager-readability if it only says that scripts/jobs ran. It must answer: what conclusion follows, what hypothesis we are testing, what improved since the previous run, which goal/task moved, what remains weak, and what exact next action reduces Mikhail's future manual steering.
- Do **not** mention Hindsight in every routine Subconscious report. Hindsight is not a Telegram topic; it is a local staging/comparison tool. Mention it only when a comparison actually ran, readiness changed, it blocked something, or Mikhail is deciding whether to adopt/drop it.
- Do not rely on the model remembering these criteria at generation time. Encode the guardrail in every layer that can shape the output: the cron prompt, the deterministic report script output, skill/reference docs, memory, and tests/checks for required sections. If a user catches a report that regressed into delivery/debug style, patch all of those surfaces, not just the immediate wording.
- Stay short and manager-readable; if nothing changed, say so and include one line of provider/cron status.
- Avoid long logs, JSON, PIDs, ports, paths, layer counts, raw tool outputs, and secrets in the main text.

- If technical details are needed, put them at the end under a short `Тех. детали:` line.

If the user asks for background work and a later report, do not make every job silent/local-only. Silent samplers are fine for data collection, but schedule at least one visible checkpoint/report in the Telegram topic so the user can see that the work happened. When reporting to Mikhail, lead with the business/manager summary and keep technical paths/IDs as backup details only.

## Agentic Stack coordination rule

For topic `1347 / Subconscious`, Hermes coordinates/reviews and Bud executes after agreement. When Mikhail says to proceed “in связке с Bud,” “делай дальше,” or asks for “магия,” treat it as approval to keep closing the loop, not as a request for another plan. Hermes should publicly task Bud, wait for Bud's execution/smoke report, verify the result where possible, then summarize. Do not silently change Hermes runtime/provider or restart services.

Operational close-the-loop pattern:

1. Run a compact local preflight/audit first (`subconscious_memory.py decision-preflight`, `doctor`, targeted tests) so the Bud task includes actual gaps, not vague goals.
2. Send the public `/task@iq5000_bot correlation_id=...` in the topic with a concrete DoD and no-restart constraint.
3. Immediately log the outbound task into the shared event/board path when available (e.g. `outbound_task_logger.py --message-id ... --topic-id 1347 --text-file ...`) so watchdogs and board sync can see coordinator-originated tasks.
4. Verify board visibility (`agent_board.py --topic-id 1347 sync/list/show`) before reporting that Bud is working.
5. If completion may happen later, install a silent short-lived watcher/cron that only emits on terminal status. The watcher should re-run tests, `decision-preflight`, `doctor`, and view generation before reporting green/red.
6. User-facing updates stay short and Russian/manager-style: audit result, correlation_id/message_id, board status, watcher status, next expected checkpoint.