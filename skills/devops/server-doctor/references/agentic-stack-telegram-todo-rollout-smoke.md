# Agentic Stack Telegram TODO rollout smoke

Use this when a product/admin TODO-task feature lands in the Telegram gateway and Server Doctor is only responsible for the final ops gate.

## Scope split

- Product/admin lane owns: TODO topic concept, UX rules, task lifecycle, priorities, and button semantics.
- Coding lane owns: implementation and tests.
- Server Doctor owns only: safe drain, restart/reload, loaded-runtime acceptance, smoke, and residual-risk report.

## Acceptance checklist

1. **Pre-restart baseline**
   - Capture git/diff or reviewed commit state.
   - Confirm automated tests for the feature passed.
   - Capture current gateway PID/status and log path.
   - Check active/current tasks, queues, sessions, and watchdog/cron jobs that could be interrupted.

2. **Safe restart**
   - Treat drain as a stop/go gate. Require current idle/queued=0 evidence, not just an old idle event.
   - Prefer the normal gateway restart path; record attribution if the restart is agent-initiated.

3. **Loaded-runtime smoke**
   - Verify the PID changed and Telegram connectivity is healthy.
   - Run a non-destructive local runtime smoke that exercises the same handlers the live Telegram path uses:
     - `/task` creates or previews the expected task object/message.
     - Inline button callback such as `В работу` updates status/routing as expected.
     - `/done` on a reply or equivalent completion path closes the task.
   - Distinguish code-level tests from loaded-runtime smoke; both are needed after a gateway restart.

4. **Cleanup / board checks**
   - Confirm temporary rollout cron/watchdog jobs for the feature are gone or intentionally retained.
   - Confirm the agent/task board has no leftover rollout tasks, or list the remaining ones explicitly.

5. **Report shape**
   - Lead with the operational conclusion: GREEN / blocked / partial.
   - Include only decisive evidence: tests passed, PID old→new, Telegram connected, smoke steps OK, board/watchdog state.
   - If no human has clicked the real Telegram button yet, report it as the only residual live-external acceptance item, not as a blocker when local runtime callback smoke passed.
