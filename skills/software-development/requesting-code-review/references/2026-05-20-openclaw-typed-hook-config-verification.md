# OpenClaw typed-hook config verification (2026-05-20)

Use when reviewing OpenClaw/Hermes plugin claims around `before_prompt_build`, memory preflight, dry-run cutovers, or live prompt injection.

## Failure pattern found

A plugin can pass its local smoke test while still being a no-op in production if the smoke fabricates a richer event than the real typed-hook runtime provides.

Observed case:

- Plugin registered typed hook via `api.on("before_prompt_build", ...)`.
- Smoke passed by calling the handler with `event.context.pluginConfig` manually supplied.
- Installed OpenClaw typed-hook runtime called `before_prompt_build` with an event shaped like `{ prompt, messages }` and separate hook context containing runtime fields such as `sessionKey` / `messageProvider`.
- The legacy `registerHook` wrapper injected `context.pluginConfig`, but the typed-hook `api.on` / `registerTypedHook` path did not.
- Plugin normalized missing config to disabled and returned `null`, producing no dry-run log and no `appendContext`.

Runtime-shaped simulation result to reproduce the class of check:

```json
{
  "runtimeShapedResult": null,
  "logs": []
}
```

## Review rule

For plugin/runtime hook claims, verify the **actual production hook shape**, not just the plugin's own smoke helper.

Acceptance requires all relevant layers to be proven separately:

1. Plugin installed/loaded.
2. Hook registration observed.
3. Config source available on the real hook path.
4. Dry-run produces a real runtime log and no injection.
5. Live mode returns the expected append/injection object only after dry-run is proven.
6. Scope isolation checked for topic, DM, and general chat without cross-topic fallback.

## Specific checks for OpenClaw prompt-build plugins

- Inspect runtime code around typed hook invocation and result resolution:
  - `runBeforePromptBuild` / hook runner: what `event` is passed?
  - `resolvePromptBuildHookResult`: how `appendContext` is applied?
  - plugin loader: whether config is injected for `api.on` typed hooks or only for legacy hooks.
- Add a smoke that invokes the handler with production-shaped event `{ prompt, messages }` plus whatever separate context the real runtime passes.
- Search gateway logs for the plugin's dry-run marker after an actual routed message.
- Do not accept `smoke OK` as evidence if the smoke manually injects fields the runtime does not provide.

## Fix direction for the observed bug

Capture plugin config at `register(api)` time from the supported plugin API/config object or an explicit closure, instead of reading it from `event.context.pluginConfig` inside a typed hook.

After patching:

1. Run plugin smoke.
2. Run production-shaped handler simulation.
3. Run unit tests / config validation.
4. Restart/reload only with user approval.
5. Verify real dry-run logs before considering `dryRun=false`.

## Report shape for Mikhail

Keep it short and managerial:

- verdict first: `accept`, `reject`, or `partial`;
- what is accepted;
- exact blocker;
- one next step.

Avoid agreeable framing. Treat another agent's `completed`/`ready` as a claim, not evidence.