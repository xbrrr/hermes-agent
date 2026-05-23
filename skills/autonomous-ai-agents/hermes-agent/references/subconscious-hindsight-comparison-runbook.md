# Subconscious vs local Hindsight 24h comparison runbook

Use this when Mikhail asks to compare Hermes' active local `subconscious` provider against local/no-pay Hindsight staging over a day.

## Baseline architecture

- Main provider remains `subconscious` throughout the experiment.
- Hindsight is secondary/staging only; do not switch provider or restart Hermes runtime.
- Local Hindsight staging path: `/Users/xbr/.hermes/staging/hindsight-local`.
- Typical local ports:
  - Ollama: `127.0.0.1:11434`
  - Hindsight API: `127.0.0.1:8888`
  - pg0/Postgres: `127.0.0.1:15432` when local `5432` is occupied.
- Starter model on 16 GB Mac mini: Ollama `qwen2.5:7b`.

## 24h comparison pattern

1. Capture a baseline snapshot into `comparison/baseline.json`:
   - timestamp;
   - ports 11434/8888/15432;
   - Ollama `/api/tags`;
   - Hindsight `/health` and `/version`;
   - `subconscious` layer counts/status.
2. Install a silent sampler cron every 6 hours for four runs:
   - no-agent script mode;
   - `deliver=local`;
   - append JSONL to `comparison/samples.jsonl`;
   - print nothing on success so no chat spam.
3. Install a one-shot 24h report cron delivered to the origin topic.
4. In the final report, compare:
   - uptime/health stability;
   - recall quality on 5–7 practical queries;
   - latency;
   - resource/process footprint;
   - privacy/safety posture;
   - operational complexity;
   - recommendation: keep Hindsight secondary, disable it, or consider later promotion.

## Good practical recall probes

Use sanitized queries, not raw Telegram history:

- local-first memory decision;
- Hindsight staging ports/processes;
- morning report / nightly reflection;
- Hermes/Bud role policy in topic `1347`;
- skill candidates / procedural memory;
- rollback/stop commands;
- privacy posture for Cloud vs local Hindsight.

## Report style

Mikhail prefers concise, essence-only output. Use:

- verdict first;
- 3–5 bullets where `subconscious` wins;
- 3–5 bullets where Hindsight wins;
- latency/resource notes;
- risks;
- one recommended next action.

Do not dump raw JSON or long logs unless asked.

## Stop / rollback commands

For the staging shape used in this session:

```bash
kill $(cat /Users/xbr/.hermes/staging/hindsight-local/logs/hindsight-api.pid)
brew services stop ollama
ollama rm qwen2.5:7b
```

Adjust if the process manager or model differs.
