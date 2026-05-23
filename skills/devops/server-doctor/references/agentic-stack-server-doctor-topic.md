# Agentic Stack Server-doctor Topic

Session-derived reference for Agentic Stack topic `1346`, created/confirmed during the 2026-05 topic inventory refresh.

## Scope

`Server-doctor / topic 1346` is the dedicated ops/runtime lane for:

- hosts and access paths;
- OpenClaw/Bud and Hermes gateway runtime;
- Telegram bots and routing incidents;
- Docker, launchd, systemd, watchdogs, health checks;
- incidents, safe restarts, rollback, and postmortems.

It is **separate from Web Admin**. Web Admin remains for UI/admin/settings/product web-admin tasks. Server-doctor owns runtime/host/ops work.

## Skill set

Use the `server-doctor` protocol first. Related skills that may be relevant by task:

- `systematic-debugging` for root-cause work;
- `healthcheck` for probes and verification;
- `migration-cutover-safety` for changes with rollback/cutover risk;
- `openclaw-update-safety` for OpenClaw updates;
- `telegram-bot-coding` when Telegram bot runtime/code is involved;
- `hermes-agent` before modifying Hermes config, gateway, sessions, tools, skills, or runtime.

## Required sequence

1. Baseline: what is broken, current time, affected host/service/topic, current status.
2. Host/runtime/access map: owner, process manager, config paths, log paths, remote access path.
3. Diagnostics with evidence: logs, process state, ports, recent exits, credentials/session state, routing/event logs when Telegram is involved.
4. Classification: `down`, `degraded`, `partial`, `unstable`, or `unknown`.
5. Safe action: minimal reversible action only after evidence.
6. Verification: status command, logs quiet, external/path-specific smoke check.
7. Rollback/stop condition: know when to stop and ask/escalate.
8. Short report: result, risk, next action.

## Pitfall from this session

Do not respond to stale/delayed messages with repeated restart/reset actions. Before restart/reset/cutover:

- check whether the symptom is fresh or a caught-up/old message;
- inspect logs and session/runtime state;
- choose the minimum action;
- do not repeat restart/reset without a new fact.

## Inventory note

When refreshing Agentic Stack topic inventory, map `1346` as Server-doctor and keep this lane distinct from `Web Admin / topic 92`.
