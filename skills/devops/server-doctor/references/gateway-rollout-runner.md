# Gateway rollout runner pattern

Use when a Telegram-originated Hermes task needs a gateway restart/reload to activate code/config changes, but the current response still has to be delivered safely.

## Pattern

1. Baseline before action:
   - current time/host;
   - `hermes gateway status` and current PID;
   - `~/.hermes/gateway_state.json` active agent count / platform state;
   - recent gateway logs;
   - targeted tests or smoke for the changed area.
2. If drain is green, write a fresh restart attribution row before the actual restart:
   - actor/source/reason/target PID/timestamp MSK/correlation_id/expected downtime/evidence log.
3. Do not restart synchronously while composing the same Telegram reply that authorizes the action. Create a small rollout runner script that:
   - sleeps briefly so the current Telegram final response can leave;
   - requests `hermes gateway restart`;
   - waits for PID change and healthy process;
   - runs post-restart smoke;
   - posts a concise GREEN/RED Telegram status to the same topic.
4. Start the runner with Hermes `terminal(background=true)`, not shell wrappers such as `nohup ... &`; Hermes rejects shell-level backgrounding and cannot track it.
5. Verify execution permissions before launching (`chmod 700 script.sh`) and poll the tracked process once to catch immediate `Permission denied`/syntax failures.

## Minimal smoke shape

Prefer non-destructive smoke first:

- import/compile changed modules;
- deterministic local command-level smoke (for example task-panel create → callback parse/apply → `/done` by reply id in a temp DB);
- gateway status + log check after restart;
- if live Telegram UI is part of the feature, state clearly whether the actual button click was live-tested or only code-smoked.

## Pitfalls

- A green code/test result is not live-runtime acceptance until the running gateway has actually reloaded the changed module.
- A restart audit record is stale if PID/drain state changes; write it close to the actual restart window.
- Shell-level background wrappers (`nohup`, trailing `&`, `disown`, `setsid`) are not acceptable inside Hermes `terminal`; use `background=true`.
- The first post-restart message may only prove command/local smoke. Inline button callbacks need a real Telegram click unless a callback update is injected through a production-shaped test path.
