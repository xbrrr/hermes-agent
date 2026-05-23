# Skill inventory and Shaw adoption note — 2026-05-21

Use this as a compact reference when Mikhail asks whether to connect a skill everywhere, audit skill usage, or adopt an imported coding workflow.

## What was verified

- Hermes local skill library contained 93 skills across 24 categories.
- Observed direct usage was concentrated in a small set: `hermes-agent`, `server-doctor`, `critical-collaboration`, GitHub/repo workflow skills, `macos-computer-use`, `zoom-meeting-capture`, and the software-development skills.
- Many skills had no observed direct `skill_view`/cron-load usage in the current session store. Treat that as an inventory signal, not proof they are useless; many are niche/on-demand.
- Curator sidecar usage was strongest for `server-doctor`, `critical-collaboration`, and `zoom-meeting-capture`.

## Shaw finding

A `shaw` skill candidate was found in OpenClaw workspace material, not as an installed Hermes skill:

- `/Users/xbr/.openclaw/workspace/incoming_skills/shaw-20260225-1437/SKILL.md`
- exported copy under `/Users/xbr/.openclaw/workspace/exports/github-ready/openclaw-development-workflow-skills/skills/shaw/`

It describes a production coding workflow: staged execution, Plan → Implement → Verify → Learn, anti-stall controls, feature gates, A/B/C architecture options, ROI-based subagent routing, and tri-review contracts.

## Adoption rule

Do **not** globally auto-load heavy workflow skills like `shaw` into every topic. They consume context and turn simple conversations into process overhead.

Preferred pattern:

1. Keep global always-on skills small.
2. Bind skills by topic/lane:
   - `Coding`: coding workflow skills and optional `shaw` pilot.
   - `Web Admin`: only when work becomes real implementation/refactor/code review.
   - `Server-doctor`: ops/runbook skills first; use coding workflow only for internal code changes.
   - `Subconscious`, `Picasso`, HR, Music, CFO, Research: do not inherit coding workflow skills by default.
3. Before installing an imported skill into Hermes, run a safe-adoption pass:
   - validate frontmatter and description length;
   - inspect scripts before copying or executing;
   - separate compact `SKILL.md` from bulky references/scripts;
   - avoid copying OpenClaw-specific commands into Hermes as if already wired;
   - pilot on one real Coding task before making it a default binding.

## Reporting shape for Mikhail

Keep the answer managerial and short:

- what the skill is;
- where it lives;
- whether it is installed;
- whether to connect globally or topic-scoped;
- whether it is useful;
- top-used and least-used groups;
- next decision.

Avoid long exhaustive dumps unless he asks for the file/report path.