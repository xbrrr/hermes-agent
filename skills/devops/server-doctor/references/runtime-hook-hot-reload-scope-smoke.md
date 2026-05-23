# Runtime hook hot-reload and scope smoke

Session lesson: a runtime hook can pass code-level tests and still fail loaded-runtime scope isolation.

## Pattern

For OpenClaw/Hermes runtime hooks that add dry-run logs or prompt context:

1. Separate acceptance layers:
   - code/unit smoke;
   - loaded runtime has plugin/hook;
   - dry-run behavior;
   - live injection/mutation;
   - production-ready.
2. Treat `config hot reload applied` as only a reload event, not proof the hook's handler uses the new config.
3. Verify with live logs after the reload/restart:
   - positive scope: expected dry-run log or context appears;
   - negative scope: no dry-run log and no appended context.
4. If negative scopes still log after whitelist config:
   - suspect stale closure/`registeredConfig` captured at registration time;
   - inspect whether `event.context.pluginConfig` is present and fresh;
   - if code fix is needed, do it before restart;
   - if restart is needed, run drain-check first.
5. Drain-check is a stop/go gate:
   - green: queue depth 0, no processing session, no long-running active tasks, no pending replies that would be lost;
   - red: `queueDepth>0`, `session.state=processing`, active long task, or unclear rollback.

## Minimal evidence to report

- Config file snippet/path showing intended whitelist/dryRun.
- Runtime start/reload log line.
- Positive scope log line.
- Negative scope log absence, or exact failing line if present.
- Gateway stability/drain status before any restart.

## Failure wording

Use precise layer wording:

- `code accepted, runtime rejected`
- `positive dry-run passed, negative smoke failed`
- `live-mode not enabled`
- `restart blocked by drain-check`

Do not call this `done` until loaded-runtime negative smoke passes.
