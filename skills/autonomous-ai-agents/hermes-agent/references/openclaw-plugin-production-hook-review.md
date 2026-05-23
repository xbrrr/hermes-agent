# OpenClaw plugin production hook review notes

Use when reviewing OpenClaw/Hermes-adjacent runtime plugins that register typed hooks such as `before_prompt_build`.

## Key production-shaped facts

- Typed `before_prompt_build` handlers are called as `handler(event, ctx)`.
- The production `event` shape is minimal: `{ prompt, messages }`.
- Runtime/channel/session data is in `ctx`, not `event.context`.
- Plugin config should be captured from the registration API (`api.pluginConfig`) during `register(api)`, with a fallback to the config snapshot if needed.
- A smoke test that passes `event.context.pluginConfig` can be misleading: it exercises a legacy/test-only shape, not the production typed-hook path.

## Review checklist

1. Inspect the plugin registration path:
   - `register(api)` captures config from `api.pluginConfig` or `api.config.plugins.entries[pluginId].config`.
   - hook body does not depend on `event.context.pluginConfig` for production behavior.
2. Confirm typed hook registration is visible in `openclaw plugins inspect <id> --runtime --json`.
3. Run a production-shaped smoke:
   - dry-run: event `{ prompt, messages }` + real `ctx` should return `undefined` and log dry-run.
   - live-mode fixture: same event/context should return `{ appendContext }` or equivalent expected mutation.
4. Validate prompt injection policy and timeout in config (`hooks.allowPromptInjection`, hook timeout).
5. Check runtime freshness:
   - compare gateway process start time to plugin file mtime.
   - if files changed after gateway start, the running gateway likely has the old module in memory.
6. Only after a controlled restart, verify a real Telegram/user turn in dry-run logs before declaring runtime ready.

## Manager verdict pattern

- Code fix accepted/rejected.
- Runtime accepted/rejected separately.
- State the blocker in one sentence.
- Next safe step: usually controlled restart → dry-run real turn → log verification → live-mode decision.

## Pitfall

Do not call `doctor` “green” just because it exits 0. Report warnings separately and distinguish relevant blockers from unrelated hygiene items.