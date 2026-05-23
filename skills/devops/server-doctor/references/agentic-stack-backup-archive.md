# Agentic Stack backup/archive runbook

Session-derived pattern for safe backup/archive work in Agentic Stack / Server-doctor.

## Core policy

- GitHub is only for open code/docs after review; never use it for secrets, private state, sessions, cookies, service env, memory stores, or runtime databases.
- Backups must be encrypted before leaving the local machine.
- A plaintext archive must not be kept as a durable artifact. If a tar/stream is needed, make it ephemeral and remove it immediately, or stream directly into encryption.
- Encrypted backup archives may include secrets and private state: `.env`, service-env, sessions, private sqlite/jsonl, memory/subconscious state, skills, workspace, and launch/runtime state.
- Public/safe artifacts may include only metadata manifests and reports with no file contents and no secret values.
- A backup without restore smoke is not accepted as complete.

## MVP sequence

1. **Read-only inventory / manifest**
   - Build a manifest from explicit source roots.
   - Record path/class/size/mtime/mode/check metadata as needed.
   - Do not read or print secret values, tokens, cookies, sessions, or file contents.
   - Classify sensitive roots instead of inspecting secret contents.

2. **Human blockers before off-machine copy**
   - Destination: Windows LAN SMB share path (`//HOST/Share/path`) or SSH target (`user@host:/path`).
   - Encryption key policy: macOS Keychain, `age` identity, password manager/vault, or manual passphrase.
   - Put these blockers into the local TODO when requested so they are not lost.

3. **Encrypted archive creation**
   - Include secret/private state inside the encrypted archive if policy allows.
   - Ensure plaintext archive is not left behind.
   - Emit only encrypted blob + safe manifest/report.

4. **Copy to Windows LAN**
   - Copy encrypted blob and safe manifest/report only.
   - Do not copy plaintext staging files.

5. **Restore smoke**
   - Restore/decrypt into a temp directory only.
   - Verify archive opens and manifest matches expected scope.
   - Sample restore non-secret files.
   - Run sqlite integrity checks on copied DBs where applicable.
   - Do not restart services as part of restore smoke unless explicitly approved.

## Closure/status checklist

When Mikhail asks whether all tasks in a thread are closed:

- Check session TODO status.
- Check local TODO for waiting human blockers and newly discovered technical tails.
- Check cron/watchdog jobs related to the thread and remove stale one-shot watchdogs after ACKs.
- Check live service/status only where relevant, but do not restart.
- Report as: closed items, open items waiting on Mikhail, open items not waiting on Mikhail, verification evidence.
- Keep it manager-style: 3–6 bullets, conclusion first.

## Pitfalls

- Do not say “backup is done” when only manifest/design exists. Say “first safe step done; actual encrypted copy waits on target/key policy.”
- Do not exclude secrets from the encrypted archive just because manifests/reports must be redacted. The encrypted archive and safe manifest have different disclosure rules.
- Do not hide needed human input in chat only; add it to `/Users/xbr/.agentic-stack/local-todo.md` when asked.
- Do not turn a backup/archive task into a Perplex/routing incident just because both shared a Bud wake/parser failure. Preserve the original correlation_id and task intent.
