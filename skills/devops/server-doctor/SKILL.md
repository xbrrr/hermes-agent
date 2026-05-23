---
name: server-doctor
description: Audit and repair hosts, agents, Telegram bots, launchd/systemd/Docker services, remote access, incidents, health checks, safe restarts, rollback, and postmortems.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [ops, incident-response, remote-access, launchd, systemd, docker, health-checks]
    category: devops
---

# Server Doctor

Use this skill for ops-style host/service triage and repair: hosts, OpenClaw/Bud, Telegram bots, launchd/systemd/Docker services, remote access, health checks, safe restarts, baseline/rollback, and postmortems.

## Working protocol

0. **Proactive ops for Hermes↔Bud coordination**
   - When Hermes delegates a task to Bud via `@iq5000_bot /task correlation_id=...` in a topic with `requireMention: true`, expect ACK within 2–5 minutes.
   - If no ACK/response after 5 minutes: **do not wait for user ping**. Immediately start server-doctor triage: baseline → diagnose → safe action → report.
   - User expectation: "менеджер делегирует → исполнитель не принимается → менеджер чинит блокер → продолжает задачу" — not "менеджер ждёт ping от Mikhail".
   - Correct delegation format for `requireMention: true` topics: `@iq5000_bot /task correlation_id=...` (plain text mention first). Bot-command format `/task@iq5000_bot ...` will be stored by Telegram but classified as `no-mention` by OpenClaw and ignored.

1. **Baseline first**
   - What is broken from the user's point of view?
   - Which host/service/account is involved?
   - Current state: `down`, `degraded`, `partial`, `unstable`, or `unknown`.
   - Capture current time, hostname, OS, network, process/runtime, ports, logs, and launch/service state before changing anything.

2. **Map host/runtime/access**
   - Host identity, LAN/public/VPN IPs, logged-in user, privileges.
   - Runtime owner: launchd, systemd, Docker, tmux, cron, app bundle, or manual process.
   - Access paths: SSH, GUI remote desktop, mesh VPN, vendor remote app, console/provider panel.
   - Config paths and log paths.

3. **Diagnose with evidence**
   - Do not declare root cause from symptoms alone.
   - Check process state, listener ports, logs, recent exits, permissions, credentials/session state, network/DNS, and watchdog output.
   - For Telegram bot non-response, separate four classes before fixing: process down, Telegram transport/ingress degraded, routing/config mismatch, and model/tooling slowdowns. See `references/telegram-agent-nonresponse-triage.md`.
   - OpenClaw/Bud wake quirk: bot-origin `/task@iq5000_bot ...` can be stored as a Telegram message but classified as `no-mention`; for reliable bot-to-bot delegation use a plain textual mention such as `@iq5000_bot /task correlation_id=...` and verify runtime logs for `Inbound message ... -> @iq5000_bot` rather than only checking message storage.
   - For network/provider reachability, distinguish OS/device-level exit-node routing, macOS system proxy, and per-process `HTTP_PROXY`/`HTTPS_PROXY`. Verify both the current shell and the actual gateway/worker PID environment before saying a blocked provider will or will not route via VPS; see `references/agent-runtime-vps-proxy-vs-exit-node.md`.
   - Prefer small probes that are safe and reversible.

4. **Safe action**
4. **Safe action**
   - Before restart/repair, know the exact restart path and owner.
   - If an Agentic Stack request is really product/admin architecture (for example TODO-topic UX, task lifecycle, buttons, or prioritization rules), do not absorb it as an ops incident. Route concept/UX/rules to the product/admin lane and code changes to the coding lane; return to Server Doctor only for the final drain → restart/reload → smoke → rollback gate.
   - Before any gateway/OpenClaw/Telegram runtime restart, check active/current long-running tasks, runs, sessions, queues, and background processes. Defer restart until they drain unless the user explicitly approves interrupting them; one task needing a restart must not break unrelated long tasks.
   - For OpenClaw session token pressure/compaction, do not assume `safeguard` is a continuous background collector. Use `references/openclaw-session-compaction-guard.md`: classify token pressure, gate explicit compaction on idle/queue/run state, avoid interrupting active sessions, and verify before→after tokens/connectivity.
   - For paired Hermes/MM + Bud/OpenClaw runtime risks, close the problem class, not only the current symptom. If context/compaction, routing, restart/cutover, watchdog, delivery, or memory-hygiene risk is found in one runtime, check the peer runtime too. Safe default: alert/guard/runbook first; compact before reset; reset/restart/cutover only with audit trail, active-task check, and explicit reason.
   - Interpret `stop` precisely: if the user stops an unsafe restart, cancel only that unsafe action, not the whole underlying task. Once a safe/drained restart is approved and completed, continue the original task automatically through post-restart smoke/dry-run verification and report; do not wait for the user unless a new product/policy decision is required.
   - Prefer `launchctl kickstart`/`systemctl restart`/container restart over killing broad process groups. For macOS LaunchAgent plist environment changes, `kickstart -k` alone may restart without re-reading env; use `launchctl bootout` + `launchctl bootstrap` + `launchctl kickstart`, after drain/baseline and with a rollback backup.
   - Avoid destructive edits; back up config files before modifying.
   - Define a stop condition: when to stop trying and ask/escalate.
   - For any agent-initiated `restart`, `reset`, or `cutover`, write an attribution record before/with the action: actor, source/tool/client, reason, target PID/service, timestamp_msk, optional raw_source_timestamp, `correlation_id`, expected downtime, rollback/smoke path, and evidence/log path. Never leave handoff/source fields as `unknown` when the action came from Hermes/Bud/MM.

5. **Verify**
   - Verify from the relevant path, not only locally: port open, status command healthy, connection handshake, logs quiet, watchdog exit code clean.
   - If a service must survive reboot/login, verify launchd/systemd unit syntax and loaded state.
   - For policy/config finalization, separate source-of-truth acceptance from loaded-runtime acceptance. If a rule was added to `chats.yaml`/`chats.md` but not to OpenClaw's live `systemPrompt` config, it is only policy-level ready. To make it runtime-ready, use `references/openclaw-runtime-prompt-policy-finalization.md`: backup `openclaw.json`, patch group/topic/wildcard prompts, validate coverage, safe-restart, then smoke PID/connectivity/Telegram/tasks.
   - For Telegram TODO/task-manager rollouts, use `references/agentic-stack-telegram-todo-rollout-smoke.md`: after tests and restart, verify PID old→new, Telegram connectivity, `/task` creation path, inline button callback such as `В работу`, reply-based `/done`, rollout watchdog/cron cleanup, and empty/known board state. Treat missing human live-button click as a residual external acceptance item, not a blocker, if local runtime callback smoke passed.

6. **Summarize concisely**
   - User prefers essence-first ops reports: result, access/commands, risks, next step.
   - For Mikhail, use terse manager-style Russian: answer the corrected point directly, avoid defensive explanations, and include only the evidence needed to support the conclusion.
   - Route reports to the topic that matches their subject. Ops/runtime/migration/health-check reports belong in Agentic Stack `Server-doctor` topic 1346; do not send them to retired/general MM/MM+Bud catch-all topics unless the user explicitly asks.
   - For Agentic Stack topic inventory/routing updates, verify against both source-of-truth files and runtime/session evidence before declaring the inventory complete. Existing domain topics can be missed if only the current registry is checked; see `references/agentic-stack-topic-inventory.md`.
   - For Telegram topic retirement/deletion, use `references/agentic-stack-topic-migration.md`: separate live defaults from historical references, fail closed on retired topics, update both registry/docs source-of-truth, and check cron/job delivery plus hidden `origin` context before declaring cleanup complete.
   - Avoid long forensic dumps unless asked.
  - When Mikhail asks to “duplicate today’s runs/progress/health checks” for Agentic Stack, do not paste cron logs. Reconstruct the day from scheduled job outputs, topic reports, board/session evidence, and current smoke checks, then answer human-first: what changed, why it matters, what is still weak, and what needs a decision. Do not use metrics unless they translate into a concrete management consequence. See `references/agentic-stack-daily-human-digest.md`.
  - For scheduled nightly Agentic Stack Server-doctor loops, do real small safe improvement work in addition to review: check canonical topic files, gateway/board health, log noise, stale references, missing smoke/docs, and maintain `/Users/xbr/.agentic-stack/architecture-backlog.md`. Verify with the current CLI/help before citing commands; no live restart without separate drain/approval. See `references/agentic-stack-nightly-runtime-improvement-loop.md`.
  - When Mikhail asks whether a routing/policy/config change is “внесено и работает” and whether restarts are needed, answer in three layers: source-of-truth policy/docs, static runtime config, and currently loaded live process. Be explicit if docs/policy are updated but the live gateway process predates the change or its `systemPrompt` lacks the rule; do not call that fully working. State whether an immediate restart is necessary for safety (often no) versus necessary for the runtime to ingest the new prompt/config (yes after drain/reload/smoke).
- Keep Mikhail-facing status updates short enough for one Telegram message unless he asks for detail. Use natural Russian; avoid stock AI phrases and filler such as “без простыни”, ritual apologies, or meta-commentary about being concise.
   - For Subconscious/decision-memory quality checks, prefer a live recall smoke: ask 5–7 real operating questions, compare retrieved facts against source-of-truth/decision views, and report only pass/fail, weak spots, and next action. See `references/agentic-stack-subconscious-live-recall-smoke.md`.

## Restart/reset/cutover source checks

When asked whether an agent initiated a restart, verify attribution before answering:

1. Correlate the incident timestamp across the initiating agent session (`~/.hermes/sessions/`, `~/.hermes/logs/agent.log`), service logs, and any handoff/reliable-task artifact.
2. Look for the exact command/action (`openclaw gateway restart`, `launchctl kickstart`, `systemctl restart`, `kill`, `pkill`, etc.) and its tool output, not just downstream `SIGTERM` symptoms.
3. For OpenClaw gateway restarts, useful evidence paths include:
   - Hermes session JSON/JSONL for terminal tool calls.
   - `~/.hermes/logs/agent.log` for tool completion timing.
   - `~/.openclaw/logs/gateway.log` for `SIGTERM`, restart mode, and readiness.
   - `/tmp/openclaw/openclaw-YYYY-MM-DD.log` for CLI restart subsystem messages such as stale PID kills.
   - `~/.agentic-stack/reliable-mm/<correlation_id>/` for request metadata and prompt context.
4. Answer in the requested forensic shape: `yes/no/no evidence`, evidence paths checked, and whether the proposed logging rule is accepted.

## Remote access reliability pattern

Do not rely on a single vendor GUI tool as the only path. Build at least two independent channels:

- **Primary:** mesh VPN such as Tailscale + SSH for shell + VNC/Screen Sharing/RDP for GUI.
- **Fallback:** vendor remote desktop such as AnyDesk/RustDesk/Chrome Remote Desktop.
- **Emergency:** provider console, physical access, or another always-on management path where available.

For macOS specifically:

- Check Tailscale: `tailscale status --self`, `tailscale ip -4`, `tailscale debug prefs`.
- Check ports over the VPN IP: `22` for SSH, `5900` for Screen Sharing/VNC, vendor ports if applicable.
- Check launchd units with `launchctl print`, `launchctl list`, `plutil -lint` for plists, and script syntax with `zsh -n`/`bash -n`.
- For Screen Sharing, a successful RFB banner on `5900` is a useful low-level sanity check.
- For AnyDesk, `AnyDesk --get-status` and `AnyDesk --get-id` are useful baseline probes, but AnyDesk should usually be fallback, not primary.

## Watchdogs and health checks

Use lightweight, non-destructive watchdogs for brittle access paths:

- A reconnect job for mesh VPN if status fails.
- A health job that logs whether VPN, SSH, GUI remote desktop, and fallback remote app are reachable.
- A fallback-app repair job only when status is unhealthy.

Keep watchdog logs in a user-readable location such as `~/Library/Logs/` on macOS unless the job runs as root. Avoid writing user launch-agent logs to `/var/log` unless permissions are intentional.

## Pitfalls

- **Wait-for-user-ping anti-pattern.** When Hermes delegates to Bud and Bud doesn't respond within 2–5 minutes, do not wait for Mikhail to notice and ping you. Start server-doctor triage immediately: the user expects "manager fixes blocker → task continues", not "manager waits for user to notice blocker". This applies to any cross-agent coordination where the executor goes silent.
- **Solve blockers before asking.** When Mikhail says "у тебя есть коннект к github можно делать комит и пуш туда без секретов" or similar unblocking info, act immediately — create forks, add remotes, push branches, open PRs. Don't ask "what should I do about X?" when the solution is known and executable. User expects: blocker identified → workaround/fix applied → task continues → result reported. Not: blocker identified → question to user → wait for permission.
- Do not call anything "guaranteed" without naming the physical/network limits: power off, no internet, expired auth/session, revoked permissions, broken OS boot.
- Do not restart broad services before mapping runtime and rollback.
- Do not treat dry-run success as production/live acceptance. For runtime hooks, separate: code accepted/rejected, loaded-runtime accepted/rejected, dry-run accepted/rejected, and live-mode accepted/rejected.
- Do not treat code-level smoke as runtime acceptance. A live gateway may keep old plugin code or a registered hook closure until a safe restart/reload actually loads the changed module.
- For Telegram-originated gateway rollouts, avoid restarting synchronously before the current final response can be delivered. Use a short tracked rollout runner (`terminal(background=true)`, not `nohup ... &`) that waits briefly, restarts, verifies PID/status/smoke, and reports GREEN/RED back to the topic; see `references/gateway-rollout-runner.md`.
- Drain-checks can be disturbed by agent chatter. Repeated Hermes↔Bud coordination messages and repeated polling may themselves create `message.queued`, `processing`, or `queueDepth=1`. If a restart is waiting on drain, stop the ping-pong and require a quiet stable idle window (30–60s) before Go.
- A restart-audit record is time-sensitive. An old attribution row is not authorization for a later restart; append a fresh record immediately before restart with current PID/time and `drain=green` evidence.
- Before switching a dry-run hook to live injection/mutation, verify scope policy explicitly. A provider-level gate such as `allowedProviders: ["telegram"]` may be safe for logging but too broad for live behavior; require topic/chat whitelist or another narrow guard when the intended rollout is a canary.
- For scoped dry-run hooks, negative smoke means **silence**, not just “0 records”: out-of-scope topics must produce no hook log and no prompt context/injection. If out-of-scope logs continue after a whitelist change, runtime acceptance is failed even when code-level smoke passes.
- Before switching a dry-run hook to live injection/mutation, verify scope policy explicitly. A provider-level gate such as `allowedProviders: ["telegram"]` may be safe for logging but too broad for live behavior; require topic/chat whitelist or another narrow guard when the intended rollout is a canary.
- Treat restart drain-check as a stop/go gate: the latest gateway stability state must be idle with queueDepth/queued=0. A prior idle event is not enough if a later `message.queued`/`processing` event exists.
- Restart attribution/audit records must be fresh for the actual restart window. An old planned restart record is not permission to restart after the drain state or target PID/time changes.
- Do not respond to stale/delayed incident messages with repeated restart/reset actions. First verify the symptom is fresh, inspect logs/session state, and require a new fact before a second restart/reset/cutover.
- Before switching a dry-run hook to live injection/mutation, verify scope policy explicitly. A provider-level gate such as `allowedProviders: ["telegram"]` may be safe for logging but too broad for live behavior; require topic/chat whitelist or another narrow guard when the intended rollout is a canary.
- For gateway/OpenClaw restarts, drain-check is a stop/go gate, not a checkbox. Treat `queueDepth>0`, `session.state=processing`, active long-running tasks, or pending replies as red; defer restart and report blocker + next check instead of forcing a reload.
- Do not respond to stale/delayed incident messages with repeated restart/reset actions. First verify the symptom is fresh, inspect logs/session state, and require a new fact before a second restart/reset/cutover.
- **Telegram bot-to-bot delegation format.** For topics with `requireMention: true`, use `@iq5000_bot /task correlation_id=...` (plain text mention at the start). The format `/task@iq5000_bot ...` is stored by Telegram as a `bot_command` entity but classified by OpenClaw auto-reply logic as `no-mention`, so the bot ignores it. Always verify with gateway logs (`Inbound message ... -> @iq5000_bot`) rather than only checking Telegram message storage. See `references/telegram-agent-task-ack-triage.md`.
- If wake-format changes require passive board/parser changes (for example accepting both `/task@iq5000_bot` and `@iq5000_bot /task` in `agent_board.py`), treat that as Server-doctor ops/tooling, not the originating subject topic. Smoke must prove: old format still works, new format works, `py_compile` and board self-test pass, enabled-topic syncs are OK, and `malformed_tasks=[]` / `malformed_acks=[]` across checked topics. Do not restart gateway/runtime for parser-only smoke unless a separate rollout decision requires it.
- OpenClaw gateway CLI pitfall: `openclaw gateway restart --safe` cannot be combined with `--wait`; safe restart uses gateway deferral. Use `--safe` alone, then poll `openclaw gateway status` until `Connectivity probe: ok`.
- Do not treat a localhost-only check as proof of remote reachability; verify through the intended remote path/IP.
- Do not declare an Agentic Stack topic inventory complete from one registry view only. Cross-check `/Users/xbr/.agentic-stack/chats.yaml`, `/Users/xbr/.openclaw/workspace/chats.md`, and runtime/session evidence for forum topic IDs/names. Missing existing domain topics is a routing bug, not a harmless omission.
- launchd plists must contain only valid plist XML. Do not leave shell commands appended after `</plist>`.
- If a user-facing remote app is unreliable, demote it to fallback and make the VPN + SSH/VNC path primary.
- **Frozen error logs:** If a service error log shows repeated old errors but no new writes (check mtime), rotate it safely: `mv old.log old.log.backup-$(date +%Y%m%d) && touch old.log`. This clears noise without losing history and makes fresh errors immediately visible.

## References

- `references/openclaw-telegram-topic-routing-triage.md` — triage OpenClaw Telegram topic wake failures: distinguish gateway/polling stuck, ingress spool present but topic session stale, and missing explicit topic routing.
- `references/runtime-hook-rollout.md` — layered acceptance for runtime hooks/plugins: code vs loaded-runtime vs dry-run vs live-mode, restart drain-check, and scope whitelist before live injection.
- `references/runtime-hook-rollout-drain-and-negative-smoke.md` — session-derived playbook for runtime hook rollout: stale loaded code, dynamic hook config, quiet drain windows, fresh restart attribution, and positive/negative smoke.
- `references/openclaw-runtime-prompt-policy-finalization.md` — finalize source-of-truth policy into OpenClaw runtime prompts: backup config, patch group/topic/wildcard prompts, validate JSON and coverage, safe restart, PID/connectivity/Telegram/task smoke, and concise human-first reporting.
- `references/gateway-rollout-runner.md` — delayed tracked runner pattern for Telegram-originated gateway restarts: baseline, fresh audit row, sleep-to-let-current-response-send, restart, PID/status wait, post-restart smoke, and concise GREEN/RED report.
- `references/agentic-stack-telegram-todo-rollout-smoke.md` — final ops acceptance for Telegram TODO/task-manager rollouts: safe drain, restart, loaded-runtime `/task` + button callback + `/done` smoke, watchdog/board cleanup, and residual human-click note.

- `references/mac-mini-remote-access.md` — concrete macOS/Tailscale/AnyDesk pattern from the Mac mini repair session; includes distinguishing Tailscale exit-node routing from macOS system proxy and per-process `HTTP_PROXY`/`HTTPS_PROXY`, plus safe full-device exit-node enable/rollback checks.
- `references/macos-per-app-browser-vps-proxy.md` — create and verify a dedicated Chrome launcher/profile that routes only browser HTTP/HTTPS traffic through a VPS proxy without changing the Mac's full-device route.
- `references/agent-runtime-vps-proxy-vs-exit-node.md` — diagnose provider reachability through per-process proxy env vs macOS system proxy vs Tailscale full-device exit node; includes process-env, Cloudflare trace, and launchd persistence checks.
- `references/agentic-stack-server-doctor-topic.md` — Agentic Stack `Server-doctor / topic 1346` scope, skill bindings, and the no-stale-message/no-repeat-restart pitfall.
- `references/agentic-stack-topic-inventory.md` — Agentic Stack topic inventory/routing governance: source-of-truth order, durable topic mapping, validator/smoke workflow, and anti-sycophancy reporting rule.
- `references/telegram-agent-task-ack-triage.md` — how to verify whether a bot-to-bot Telegram task was actually received/accepted before escalating.
- `references/agentic-stack-subconscious-live-recall-smoke.md` — run a concise live recall smoke for Subconscious memory decisions and report pass/fail without raw logs.
- `references/agentic-stack-backup-archive.md` — Agentic Stack backup/archive pattern: encrypted archives may include secrets, safe manifests must not, Windows LAN target/key blockers, restore-smoke acceptance, and closure checks.
- `references/telegram-agent-nonresponse-triage.md` — Hermes/MM + OpenClaw/Bud Telegram non-response triage: distinguish process, transport, routing, and model/tooling slowdowns before restart.
- `references/openclaw-session-compaction-guard.md` — safe guard for oversized OpenClaw sessions: token-pressure thresholds, idle/queue/run gates, explicit compaction vs defer, and before→after verification.
- `references/macos-launchd-path-wrapper-vs-default.md` — macOS LaunchAgent PATH issue: `.env` wrapper sets PATH correctly but `launchctl print` shows only default environment; non-interactive hooks/scripts may miss Homebrew binaries. Fix: add `EnvironmentVariables` to plist or `openclaw doctor --repair`.
