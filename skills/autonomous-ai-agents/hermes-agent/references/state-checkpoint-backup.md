# State checkpoint + backup workflow

Use this when the user asks to "фиксировать текущую работу", preserve current state, update/push skills, or avoid losing work before a reset/migration.

## Scope discovery

1. Identify source-of-truth state before acting:
   - `/Users/xbr/.agentic-stack/chats.yaml`
   - `/Users/xbr/.openclaw/workspace/chats.md`
   - active Hermes repo, usually `/Users/xbr/.local/src/hermes-agent`
   - OpenClaw workspace, usually `/Users/xbr/.openclaw/workspace`
   - user-local skills, usually `/Users/xbr/.hermes/skills`
   - existing backup roots, especially `/Users/xbr/.hermes/backups` and `/Users/xbr/.openclaw/workspace/backups`
2. For every git repo found, capture:
   - current branch and remote
   - `git status --short --branch`
   - dirty tracked/untracked files
   - whether a remote exists before promising a push

## Skills first: update, commit, push without secrets

1. Run the Hermes skill updater (`hermes skills update` / `hermes skills check`) if available.
2. For exported skill repos under `exports/github-ready/*`, sync only the corresponding skill files from the workspace into the export repo. Avoid copying broad reference trees blindly when they contain vendored repos, media, or large files.
3. Before committing, run a lightweight secret scan over staged files. At minimum catch:
   - `sk-...`
   - `ghp_...`
   - `github_pat_...`
   - `xox...`
   - `AIza...`
   - suspicious `api_key|token|secret|password = long value`
   Allow examples/placeholders such as `***`, `<...>`, `your-token`, `example`, `dummy`, and `12345678`.
4. Commit class-level skill updates with concise conventional commits, e.g. `docs: refresh yandex metrica skill guidance` or `chore: checkpoint skill updates`.
5. Push only repos that have remotes. Verify with `git ls-remote` or local/remote HEAD equality. If a workspace has no remote, say so and rely on the local commit + backup bundle.

## Backup everything else, redacted

Create a timestamped directory next to previous backups, usually:

```text
~/.hermes/backups/state-YYYYMMDD-HHMMSS/
```

Include:

- tarballs of important state trees (`.agentic-stack`, `.openclaw/workspace`, `.hermes/skills`)
- redacted config snapshots (`~/.hermes/config.yaml`, not `.env`)
- git captures for active repos:
  - `status.txt`
  - `remote.txt`
  - `log.txt`
  - `diff.patch`
  - `staged.diff.patch`
  - `untracked.txt`
  - `git bundle create <repo>.bundle --all`
- a `manifest.json` with source paths, file counts, skipped counts, notes, and bundle exit codes
- `.skipped.txt` files beside each tarball

Exclude obvious secrets and runtime/cache bulk:

- `.env`, `auth.json`, `credentials.json`, `token.json`, `.netrc`
- `secrets/`, `.secrets/`
- `.git`, `__pycache__`, virtualenvs, `node_modules`, pytest/mypy/ruff caches
- browser profiles/caches, logs, temp dirs, `Cookies`, cookie journals
- very large files unless they are explicitly part of the requested state

## Verification before reporting

Before final response:

1. Test every created tarball with `tar -tzf`.
2. Scan archive member names for obvious secret paths (`.env`, `auth.json`, `credentials.json`, `token.json`, `secrets`, `.secrets`).
3. Verify pushed repos are clean and local HEAD equals remote HEAD.
4. For local-only repos, verify the local checkpoint commit exists and a post-commit git bundle was added to the backup.
5. Report only essentials: pushed commit(s), local commit(s), backup path/size, secret-safety checks, and any remaining dirty work that was intentionally only backed up.

## Pitfalls

- Do not promise a push for a repo with no remote. Say "local commit + backup bundle".
- Do not copy whole external reference/vendor trees into public skill repos unless explicitly reviewed; they may contain large files or licensing/security issues.
- Do not include raw `.env`, auth, cookie, browser profile, or `.secrets` paths in backups.
- If the backup is created before a final local commit, add a post-commit git capture/bundle so the backup includes the actual final checkpoint.
- Keep the user-facing summary concise; Mikhail wants the result, not a long process narrative.