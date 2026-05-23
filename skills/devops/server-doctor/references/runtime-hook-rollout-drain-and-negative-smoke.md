# Runtime hook rollout: drain, stale code, and negative smoke

Session pattern captured from the `subconscious-preflight` OpenClaw plugin rollout.

## Durable lesson

For runtime hooks/plugins, a code-level smoke passing is not enough. The live gateway may still hold old plugin code or old registered hook closures until a safe restart/reload actually loads the new module.

Keep acceptance layered:

- **code accepted**: unit/smoke tests pass against files on disk.
- **loaded-runtime accepted**: live process has restarted/reloaded and is known to be running the changed code.
- **dry-run accepted**: positive and negative dry-run checks pass in the live runtime.
- **live-mode accepted**: only after scoped dry-run acceptance.

## Drain-check gotcha

Repeated Hermes↔Bud coordination messages and repeated polling can themselves create `message.queued`, `session.state=processing`, and `queueDepth=1`, preventing a clean drain. Do not create a self-sustaining restart blockade by chatting every few seconds.

Safe pattern:

1. Run one drain-check.
2. If not green, stop chatting/polling and allow a quiet interval.
3. Require a stable idle window (e.g. 30–60 seconds) with no new `message.queued` or `processing` events before restart.
4. If messages keep arriving, report `Go: no` once and wait for a real pause.

## Audit/attribution record rule

An old restart-audit entry is not permission to restart later. Before the actual restart, append a fresh attribution record with:

- actor/source/tool/client;
- reason;
- target service and current PID;
- timestamp;
- explicit `drain=green` evidence;
- expected downtime;
- rollback path;
- smoke path.

## Runtime hook smoke checklist

After safe restart/reload:

- Verify gateway is up and the expected PID changed or module reload is proven.
- Positive smoke: intended scope logs/receives dry-run context.
- Negative smoke: non-whitelisted scopes are silent — no log and no context.
- If negative smoke fails, do not enable live mode. Disable/rollback the plugin and debug config/module loading.

## Example failure mode

A plugin registered a hook while capturing config at registration time. `allowedScopes` was later hot-reloaded in config, but the live hook kept using the old config/code and continued logging dry-run events for non-whitelisted topics. The code fix was to resolve config on every hook invocation; runtime acceptance still required safe restart and live positive/negative smoke.
