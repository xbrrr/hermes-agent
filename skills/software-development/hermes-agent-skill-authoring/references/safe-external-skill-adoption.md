# Safe External Skill / Playbook Adoption

Use this when a user provides a large external `SKILL.md`, playbook, or methodology and asks whether to install it.

## Decision frame

- Treat the source artifact as a **knowledge source**, not automatically as runtime code.
- Preserve useful methodology, but do not import unreviewed automation, broad external claims, credential examples, or vendor-specific assumptions as persistent rules.
- Prefer a **class-level runtime extraction** over a one-session narrow skill.

## Minimal safe adoption flow

1. **Audit first**
   - Count lines/chars and `description` length.
   - Validate YAML frontmatter.
   - Identify whether it is an article/workshop/reference pack masquerading as a runtime skill.
   - Check for embedded scripts, install commands, MCP setup, external URLs, benchmark claims, and secrets/placeholders.

2. **Install conservative runtime skill**
   - Short `SKILL.md` only.
   - Trigger-focused description under 1024 chars; target 150-300 chars.
   - Keep operational procedure, safety defaults, output format, and quality checks.
   - Exclude executable scripts unless reviewed and needed.
   - Exclude broad benchmark claims as rules; rephrase as hypotheses if necessary.
   - Exclude URL/reference sprawl unless the runtime skill genuinely needs it.

3. **Protect secrets**
   - Do not copy API keys, tokens, `.env` contents, credentials, or real private examples.
   - Use placeholders such as `<API_KEY>` only.
   - Verify with a simple pattern scan when tools are available.

4. **Sync executor runtimes separately**
   - Installing a skill for Hermes does not automatically install it for Bud/OpenClaw or other agents.
   - Copy/sync to the executor only if it improves execution quality.
   - Do not restart live runtimes just to pick up the skill unless the user explicitly wants that; note that current sessions may need reload/new session.

5. **Schedule audits only as read-only by default**
   - Health-check cron jobs should avoid restarts, edits, installs, or secret printing unless explicitly approved.
   - Reports should be concise and Telegram-friendly: status, drift, top risks, top actions, verification.

## Output pattern for Mikhail

Keep it short:

- Installed: `<skill-name>`
- Scope: what it will help with
- Excluded: scripts / URLs / unverified claims / secrets
- Verified: frontmatter, length, no secret patterns
- Runtime note: whether Bud/OpenClaw also received it and whether reload/restart is needed
