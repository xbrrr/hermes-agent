# Runtime hook rollout notes

Use for OpenClaw/Hermes/Gateway plugin or hook changes that affect prompt construction, routing, injection, or live runtime behavior.

## Layered acceptance

Keep verdicts separate:

1. **Code accepted/rejected** — source diff looks correct and unit tests/smoke pass.
2. **Loaded-runtime accepted/rejected** — the running process has restarted or otherwise loaded the changed file. Compare process start time to file mtime when needed.
3. **Dry-run accepted/rejected** — live runtime emits the expected no-op/dry-run evidence from the real hook path.
4. **Live-mode accepted/rejected** — mutation/injection is enabled only after explicit scope policy and canary plan.
5. **Production-ready accepted/rejected** — after live canary, logs/behavior are clean and rollback is known.

## Restart gate

Before restart:

- baseline: actor, approval source, target service/PID, reason, expected downtime, rollback, smoke path;
- drain-check: active long tasks, runs, sessions, queues, background processes;
- if active long tasks exist, defer unless user explicitly approves interruption.

If the user says `stop`, treat it narrowly: stop the unsafe restart/action, not the whole task. After a safe/drained restart, continue automatically through smoke/dry-run verification and verdict.

## Scope gate for live hooks

Dry-run at broad scope can be acceptable because it only logs. Live-mode is different:

- provider-level gates like `allowedProviders: ["telegram"]` may affect every Telegram topic;
- before live injection/mutation, require an explicit chat/topic whitelist or equivalent narrow guard;
- verify positive and negative scope: intended topic fires, unrelated topics do not;
- negative-scope smoke must assert full silence, not just empty/zero-result data: no dry-run log, no `appendContext`, and no fallback context for non-whitelisted chat/topics/DMs;
- keep `dryRun: true` until Hermes/MM accepts canary live.

## Evidence examples

- process loaded new code: gateway process start time is later than plugin file mtime;
- dry-run evidence: log line from the real gateway log, not only local smoke;
- negative scope evidence: no log/injection for non-whitelisted topics after test turns.
