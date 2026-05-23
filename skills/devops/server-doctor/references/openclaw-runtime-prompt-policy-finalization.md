# OpenClaw runtime prompt policy finalization

Use this when a policy has already been added to source-of-truth docs (for example `chats.yaml` / `chats.md`) but the user asks whether it is actually live for Bud/OpenClaw.

## Key distinction

- **Policy-level ready** means the rule exists in durable source-of-truth docs or skills.
- **Runtime-level ready** means OpenClaw's loaded config/session prompts include the rule and the gateway has reloaded them.

Do not call the work complete until the intended layer is explicit.

## Safe finalization pattern

1. **Backup config first**
   - Copy `~/.openclaw/openclaw.json` to a timestamped local backup, for example `~/.openclaw/backups/openclaw.json.before-<change>-YYYYMMDD-HHMMSS`.

2. **Patch the live config deliberately**
   - Add the policy to the group `systemPrompt`, every relevant topic `systemPrompt`, and wildcard `topics.*.systemPrompt` when inheritance behavior is ambiguous.
   - Keep the text short and operational. Example for coding routing:
     - `Глобальное правило кодинга: если задача в любом активном топике становится существенной разработкой (feature/refactor/risky bugfix/tests/PR/bot/gateway/integration/runtime/multi-file), используй shaw; лёгкие read-only/explanation/one-line/research задачи не утяжеляй.`

3. **Validate before restart**
   - Parse JSON from disk.
   - Count checked prompts.
   - Report `missing=[]` or exact missing prompt paths.
   - Run read-only status/doctor checks to catch obvious config/service issues.

4. **Restart only as a safe rollout**
   - Capture baseline PID/status.
   - Write a fresh restart-attribution/audit record with actor, reason, target service/PID, rollback path, and smoke plan.
   - Use `openclaw gateway restart --safe` rather than unsafe process killing.
   - Poll until PID changes and `Connectivity probe: ok`.

5. **Post-restart smoke**
   - Re-validate prompt rule from config.
   - Check `openclaw gateway status` and `openclaw status --deep`.
   - Confirm gateway reachable, event loop OK, Telegram OK, and no active/queued/running tasks unless expected.

## Reporting shape

For Mikhail, answer in human terms first:

- `Готово, финализировал.`
- What changed.
- What proof exists: prompts covered, PID changed, connectivity OK, Telegram OK, tasks idle.
- Whether another restart is needed.
- Separate unrelated hygiene warnings from blockers.

Avoid long log dumps unless asked.
