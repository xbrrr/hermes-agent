# OpenClaw session compaction guard

Use this when OpenClaw/Bud/Hermes gateway sessions are near or over context limits and the question is whether to compact, restart, or rely on safeguard auto-compaction.

## Key lesson

Do not assume `safeguard` mode is a continuous background collector for all oversized transcripts. In OpenClaw-style agent runtimes, auto-compaction often triggers only at safe points: after assistant usage/threshold checks, before a new prompt, or during overflow recovery. A session that is already oversized and idle can remain above 100% until a new safe turn or an explicit `sessions.compact` action.

## Baseline commands

```bash
openclaw sessions --agent main --json --limit all
openclaw gateway status
```

Classify sessions by token pressure:

- `>90%`: early warning.
- `>95%`: report + compaction candidate.
- `>110%`: urgent compaction candidate.
- `>100%` on an idle/deleted/retired topic: likely needs explicit cleanup/compaction rather than waiting for safeguard.

## Safe guard algorithm

1. List sessions and calculate `totalTokens / contextTokens`.
2. For each candidate, check whether the gateway/session is active:
   - active run or trajectory in progress;
   - `queueDepth > 0`, queued messages, or `processing` state;
   - recent update inside the quiet-window threshold.
3. If active, **do not compact**. Report `deferred: active run/queue` and re-check after a quiet 30–60s idle window.
4. If idle, ensure there is an archive/backup path or at least an explicit compaction audit record: actor, timestamp, session key, tokens before, expected rollback/reference path.
5. Run explicit compaction for the session only after the idle gate is green.
6. Re-list sessions and verify tokens after, `compactionCount`/freshness where available, and gateway connectivity.
7. Report GREEN/RED with before→after counts and any deferred sessions.

## Avoid as normal operation

- Do not use `maxLines`/tail truncation as the normal solution. Treat it as emergency recovery only, because it can discard useful context even if archived.
- Do not interrupt an active session just to reduce token counts unless the user explicitly approves the interruption.
- Do not call source-of-truth config like `agents.defaults.compaction.mode=safeguard` runtime proof by itself. Confirm the low-level runtime settings that actually enable compaction, such as `settings.compaction.enabled`, `reserveTokens`, and `keepRecentTokens` (or the equivalent for the current runtime version).

## Reporting shape for Mikhail

Keep it short and operational:

- `oversized`: list session/topic, tokens/context, percent.
- `action`: compacted / deferred / no-op.
- `reason`: idle gate green, or active queue/run blocker.
- `risk`: whether any active work would be interrupted.
- `next`: exact safe follow-up (quiet-window recheck, explicit compact, or config-runtime verification).
