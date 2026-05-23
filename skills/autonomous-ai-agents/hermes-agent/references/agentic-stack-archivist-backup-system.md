# Agentic Stack Archivist backup system

## Trigger

Use when Mikhail asks to design or operate a durable backup/archive system for Hermes, OpenClaw, Agentic Stack, skills, memory, sessions, secrets, or a future `Archivist` topic.

## Core distinction

Do not collapse all backup work into `git push`.

- **GitHub** is for clean code and reviewed documentation only.
- **Full operational recovery** needs a separate private/encrypted archive for memory, sessions, skills, workspace state, routing files, cron jobs, helper scripts, launch agents, and selected logs.
- **Secrets** need a separate encrypted-only lane; never push them to GitHub, even private repos, unless explicitly designed as encrypted secret material.
- **Caches and bulk logs** are usually disposable unless needed for forensic recovery.

## Data classes

Class every source before backing it up:

1. `public-code-docs`: safe for GitHub after manifest review and secret scan.
2. `private-operational`: internal rules, topic maps, sessions, memory, skills, runbooks; backupable but not broadly publishable.
3. `secret-encrypted-only`: `.env`, auth tokens, cookies, SSH keys/config, `.secrets/`, credentials, keychains/exports.
4. `runtime-rebuildable`: virtualenvs, node_modules, caches, generated temp data; exclude unless explicitly needed.
5. `large-state`: music/media/browser/workspace backups; handle by separate retention policy.

## Source map to start from on Mikhail's Mac

- `/Users/xbr/.agentic-stack` — Agentic Stack source of truth, routing, task logs/state.
- `/Users/xbr/.openclaw/workspace` — OpenClaw workspace, skills/docs/memory; can be large and contains `.secrets/`.
- `/Users/xbr/.hermes/skills` — reusable Hermes skills and references.
- `/Users/xbr/.hermes/sessions` — Hermes conversation/session state.
- `/Users/xbr/.hermes/cron` — scheduled job definitions and outputs.
- `/Users/xbr/.local/src/hermes-agent` — Hermes source repo and local modifications.
- `/Users/xbr/.local/bin`, `/Users/xbr/bin` — local helper/watchdog scripts.
- `/Users/xbr/Library/LaunchAgents` — launchd units for runtime/watchdogs.
- `/Users/xbr/.ssh` — secret-encrypted-only.

Re-discover live paths before acting; this list is a seed, not a permanent manifest.

## Safe MVP sequence

1. **Inventory only**: generate a manifest with source path, class, reason, include/exclude rules, expected size, owner, and restore purpose.
2. **Dry-run staging**: copy only manifest-approved files to a fresh staging directory; do not follow symlinks.
3. **Scanners**: deny-path scan (`.env`, `auth.json`, `credentials`, `.secrets`, cookies, SSH keys), deny-regex scan, entropy scan, and gitleaks/trufflehog if available.
4. **Local archive**:
   - clean GitHub-safe staging can become a local commit or GitHub PR after approval;
   - private/secret staging becomes an encrypted archive or encrypted restic/borg repository.
5. **First replica**: copy encrypted archive/repo to the Windows computer on the same LAN. Prefer a resumable transport (`rsync` over SSH, SMB with checksums, or restic/borg remote) and record destination path.
6. **Second replica**: later add an offsite destination in another network; do not block the LAN MVP on this decision.
7. **Restore smoke**: on a clean temp directory or spare machine, prove that at least routing files, skills, sessions index, cron definitions, and one encrypted secret sample can be restored. Report restore evidence, not just backup creation.

## Archivist topic concept

Purpose: one topic owns preservation, retention, recovery drills, and backup policy. It is not a general ops incident room and not a dumping ground for every status.

Recommended split:

- `Archivist`: policy, inventory, retention, restore drills, backup reports, destination health.
- `Server-doctor`: runtime work needed to mount/copy/restart/smoke backup services.
- `Coding`: scripts, manifests, scanners, bot/button implementation.
- `Web Admin`: UX/rules for task/topic management if the archive system needs Telegram controls.

## Done means restore works

DoD for any backup milestone:

- Manifest reviewed and committed locally.
- Secret scan passed or findings explicitly quarantined.
- Archive exists with checksum/size and timestamp.
- At least one replica outside the source disk exists.
- Restore smoke succeeded into an isolated directory/device.
- Report names what is protected, what is excluded, and what remains a single point of failure.

## Pitfalls

- Do not say “guaranteed backup” without naming limits: power loss, disk corruption before first replica, expired credentials, unmounted destination, ransomware/silent corruption, and untested restore.
- Do not use broad globs (`tar ~/`, `git add .`, `rsync -a ~`) as policy.
- Do not let secret scanners create confidence that private operational context is safe for GitHub.
- Do not include old backups inside new backups by default; this creates recursive size growth.
- Do not report only `backup created`; always include restore status or the next restore drill.
