# Delegated Chat Supervision Notes

Use this reference when supervising a task delegated through Telegram/chat or another public coordination topic rather than a native Kanban API.

## Staleness watchdog pattern

- Treat `sent` as only a transport event. The useful states are `accepted`, `in-progress`, `blocked`, `ready-for-review`, `verified`, and `rolled out`.
- Carry a stable `correlation_id` in all public status checks and executor replies.
- If no visible progress appears for the agreed watchdog window (commonly ~90 minutes for background implementation work), send a concise public status-check asking for exactly one of: `ACK`, `BLOCKED <reason>`, or `ready-for-review`.
- Ask the executor to self-diagnose and safely fix implementation issues before escalating.
- Escalate to the user only for permissions/access/secrets, destructive restarts, or scope-changing product decisions.

## Safe BLOCKED triage

When the executor reports `BLOCKED`, investigate before routing escalation:

1. Check local coordination files and logs for the `correlation_id`.
2. Inspect `git status`, relevant diffs, and touched tests/artifacts.
3. Run safe diagnostics/tests if code exists; avoid live restarts or destructive cleanup.
4. If the fix is clearly in-scope and low risk, apply it or route it back to the executor.
5. If the fix needs secrets, permissions, destructive restart, or product-scope change, prepare a 3-6 bullet decision request for the user.

## Ready-for-review validation package

When the executor says `ready-for-review`, do not treat that as complete. Verify and report:

- changed files / artifact list, separating unrelated dirty files from the MVP scope;
- canonical targeted test command and result;
- smoke test for the user-facing lifecycle, using a temp DB or sandbox where possible;
- whitespace/lint sanity such as `git diff --check`;
- added-line scan for obvious secret/security footguns, redacting any credential-shaped values;
- rollout gates still needed, especially task-drain checks and explicit approval before live gateway restart.

For manager-facing summaries, keep public updates concise, in the user's requested language, and lead with the state: `accepted`, `stale`, `blocked`, `ready-for-review`, `verified`, or `rollout waiting for approval`.