# Secure artifact backup to GitHub for agent workspaces

## Trigger

Use when Mikhail asks for automatic backup, commit, or push of Hermes/OpenClaw/Agentic Stack artifacts such as skills, runbooks, agent docs, or workspace policy files.

## Verdict pattern

Automatic GitHub push is an external data export even to a private repo. Default verdict should be:

- approve the idea only with controls;
- start with local-only dry-run;
- do not enable network push until manifest and repo are manually approved.

## Threat model gaps to check

- Skills/runbooks/docs can contain private names, chat IDs, IPs, local paths, internal rules, personal preferences, and operational details.
- `SOUL.md`, `USER.md`, `TOOLS.md`, `chats.md` are not automatically safe.
- Secret scanners miss context-sensitive secrets and private operational data.
- A single bad push can leave data in GitHub history; deleting the file later is not remediation.
- Cron logs can leak findings if they print secret values or file contents.
- Broad globs (`*.md`, `git add .`) are unsafe.
- PATs can leak through env/config/process logs if handled casually.

## Required controls

- Use an exact manifest, not globs:
  - source path;
  - destination path;
  - data class (`public-ish`, `private-ok-for-GitHub`, `local-only`);
  - owner;
  - reason for inclusion.
- Build a fresh staging directory every run.
- Copy only manifest files.
- Do not follow symlinks.
- Enforce deny-path and deny-regex rules before commit.
- Run entropy checks plus tools such as gitleaks/trufflehog if available.
- Abort on any finding before commit and before push.
- Reports show only path, rule id, severity, and count; never secret values.
- Start with local-only bare repo/no remote.
- GitHub remote only after human approval.
- PAT must be fine-grained, one private repo only, contents read/write only.
- Token should live in Keychain or a separate `0600` file outside sync scope; never in Hermes config/env outputs or repo.
- Any policy/manifest/scanner change requires dry-run + approval before push resumes.
- Kill switch: any scanner finding disables push until manual review.

## Safe MVP sequence

1. Draft manifest.
2. Dry-run staging.
3. Deny-path, deny-regex, entropy, and scanner pass.
4. Report:
   - added/changed/deleted count;
   - file list;
   - scanner result without values;
   - `push_allowed=false`.
5. Local-only commit into a clean local/bare repo without remote.
6. Review manifest and local history.
7. Only then discuss GitHub remote and PAT.

## Role split

- Hermes owns policy: what artifacts are valuable, what is excluded, and how results are summarized for Mikhail.
- Bud/OpenClaw owns cron/job runner, staging, scanning, local backup, and eventual push after approval.
- GitHub token should not be held by Hermes.
- Push should live in Bud's maintenance contour with a kill switch.

## What Mikhail must approve before push

- GitHub private repo is acceptable as external storage.
- Owner/repo name.
- First manifest.
- Whether chat IDs, names, local paths, and internal rules may be stored there.
- Fine-grained PAT for that one repo.
- Schedule: start daily dry-run; push no more than daily at first; 4h cadence only after stable operation.
- Emergency rule: scanner finding disables push until manual review.