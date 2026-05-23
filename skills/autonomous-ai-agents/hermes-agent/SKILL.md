---
name: hermes-agent
description: "Configure, extend, or contribute to Hermes Agent."
version: 2.1.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, setup, configuration, multi-agent, spawning, cli, gateway, development]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [claude-code, codex, opencode]
---

# Hermes Agent

Hermes Agent is an open-source AI agent framework by Nous Research that runs in your terminal, messaging platforms, and IDEs. It belongs to the same category as Claude Code (Anthropic), Codex (OpenAI), and OpenClaw — autonomous coding and task-execution agents that use tool calling to interact with your system. Hermes works with any LLM provider (OpenRouter, Anthropic, OpenAI, DeepSeek, local models, and 15+ others) and runs on Linux, macOS, and WSL.

What makes Hermes different:

- **Self-improving through skills** — Hermes learns from experience by saving reusable procedures as skills. When it solves a complex problem, discovers a workflow, or gets corrected, it can persist that knowledge as a skill document that loads into future sessions. Skills accumulate over time, making the agent better at your specific tasks and environment.
- **Persistent memory across sessions** — remembers who you are, your preferences, environment details, and lessons learned. Pluggable memory backends (built-in, Honcho, Mem0, and more) let you choose how memory works.
- **Multi-platform gateway** — the same agent runs on Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, and 10+ other platforms with full tool access, not just chat.
- **Provider-agnostic** — swap models and providers mid-workflow without changing anything else. Credential pools rotate across multiple API keys automatically.
- **Profiles** — run multiple independent Hermes instances with isolated configs, sessions, skills, and memory.
- **Extensible** — plugins, MCP servers, custom tools, webhook triggers, cron scheduling, and the full Python ecosystem.

People use Hermes for software development, research, system administration, data analysis, content creation, home automation, and anything else that benefits from an AI agent with persistent context and full system access.

**This skill helps you work with Hermes Agent effectively** — setting it up, configuring features, spawning additional agent instances, troubleshooting issues, finding the right commands and settings, and understanding how the system works when you need to extend or contribute to it.

**Docs:** https://hermes-agent.nousresearch.com/docs/

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Interactive chat (default)
hermes

# Single query
hermes chat -q "What is the capital of France?"

# Setup wizard
hermes setup

# Change model/provider
hermes model

# Check health
hermes doctor
```

---

## CLI Reference

### Global Flags

```
hermes [flags] [command]

  --version, -V             Show version
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --pass-session-id         Include session ID in system prompt
```

No subcommand defaults to `chat`.

### Chat

```
hermes chat [flags]
  -q, --query TEXT          Single query, non-interactive
  -m, --model MODEL         Model (e.g. anthropic/claude-sonnet-4)
  -t, --toolsets LIST       Comma-separated toolsets
  --provider PROVIDER       Force provider (openrouter, anthropic, nous, etc.)
  -v, --verbose             Verbose output
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --source TAG              Session source tag (default: cli)
```

### Configuration

```
hermes setup [section]      Interactive wizard (model|terminal|gateway|tools|agent)
hermes model                Interactive model/provider picker
hermes config               View current config
hermes config edit          Open config.yaml in $EDITOR
hermes config set KEY VAL   Set a config value
hermes config path          Print config.yaml path
hermes config env-path      Print .env path
hermes config check         Check for missing/outdated config
hermes config migrate       Update config with new options
hermes login [--provider P] OAuth login (nous, openai-codex)
hermes logout               Clear stored auth
hermes doctor [--fix]       Check dependencies and config
hermes status [--all]       Show component status
```

### Tools & Skills

```
hermes tools                Interactive tool enable/disable (curses UI)
hermes tools list           Show all tools and status
hermes tools enable NAME    Enable a toolset
hermes tools disable NAME   Disable a toolset

hermes skills list          List installed skills
hermes skills search QUERY  Search the skills hub
hermes skills install ID    Install a skill (ID can be a hub identifier OR a direct https://…/SKILL.md URL; pass --name to override when frontmatter has no name)
hermes skills inspect ID    Preview without installing
hermes skills config        Enable/disable skills per platform
hermes skills check         Check for updates
hermes skills update        Update outdated skills
hermes skills uninstall N   Remove a hub skill
hermes skills publish PATH  Publish to registry
hermes skills browse        Browse all available skills
hermes skills tap add REPO  Add a GitHub repo as skill source
```

### MCP Servers

```
hermes mcp serve            Run Hermes as an MCP server
hermes mcp add NAME         Add an MCP server (--url or --command)
hermes mcp remove NAME      Remove an MCP server
hermes mcp list             List configured servers
hermes mcp test NAME        Test connection
hermes mcp configure NAME   Toggle tool selection
```

### Gateway (Messaging Platforms)

```
hermes gateway run          Start gateway foreground
hermes gateway install      Install as background service
hermes gateway start/stop   Control the service
hermes gateway restart      Restart the service
hermes gateway status       Check status
hermes gateway setup        Configure platforms
```

Supported platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI connects via the API Server adapter.

Platform docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

### Sessions

```
hermes sessions list        List recent sessions
hermes sessions browse      Interactive picker
hermes sessions export OUT  Export to JSONL
hermes sessions rename ID T Rename a session
hermes sessions delete ID   Delete a session
hermes sessions prune       Clean up old sessions (--older-than N days)
hermes sessions stats       Session store statistics
```

### Cron Jobs

```
hermes cron list            List jobs (--all for disabled)
hermes cron create SCHED    Create: '30m', 'every 2h', '0 9 * * *'
hermes cron edit ID         Edit schedule, prompt, delivery
hermes cron pause/resume ID Control job state
hermes cron run ID          Trigger on next tick
hermes cron remove ID       Delete a job
hermes cron status          Scheduler status
```

### Webhooks

```
hermes webhook subscribe N  Create route at /webhooks/<name>
hermes webhook list         List subscriptions
hermes webhook remove NAME  Remove a subscription
hermes webhook test NAME    Send a test POST
```

### Profiles

```
hermes profile list         List all profiles
hermes profile create NAME  Create (--clone, --clone-all, --clone-from)
hermes profile use NAME     Set sticky default
hermes profile delete NAME  Delete a profile
hermes profile show NAME    Show details
hermes profile alias NAME   Manage wrapper scripts
hermes profile rename A B   Rename a profile
hermes profile export NAME  Export to tar.gz
hermes profile import FILE  Import from archive
```

### Credential Pools

```
hermes auth add             Interactive credential wizard
hermes auth list [PROVIDER] List pooled credentials
hermes auth remove P INDEX  Remove by provider + index
hermes auth reset PROVIDER  Clear exhaustion status
```

### Other

```
hermes insights [--days N]  Usage analytics
hermes update               Update to latest version
hermes pairing list/approve/revoke  DM authorization
hermes plugins list/install/remove  Plugin management
hermes honcho setup/status  Honcho memory integration (requires honcho plugin)
hermes memory setup/status/off  Memory provider config
hermes completion bash|zsh  Shell completions
hermes acp                  ACP server (IDE integration)
hermes claw migrate         Migrate from OpenClaw
hermes uninstall            Uninstall Hermes
```

---

## Slash Commands (In-Session)

Type these during an interactive chat session. New commands land fairly
often; if something below looks stale, run `/help` in-session for the
authoritative list or see the [live slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands).
The registry of record is `hermes_cli/commands.py` — every consumer
(autocomplete, Telegram menu, Slack mapping, `/help`) derives from it.

### Session Control
```
/new (/reset)        Fresh session
/clear               Clear screen + new session (CLI)
/retry               Resend last message
/undo                Remove last exchange
/title [name]        Name the session
/compress            Manually compress context
/stop                Kill background processes
/rollback [N]        Restore filesystem checkpoint
/snapshot [sub]      Create or restore state snapshots of Hermes config/state (CLI)
/background <prompt> Run prompt in background
/queue <prompt>      Queue for next turn
/steer <prompt>      Inject a message after the next tool call without interrupting
/agents (/tasks)     Show active agents and running tasks
/resume [name]       Resume a named session
/goal [text|sub]     Set a standing goal Hermes works on across turns until achieved
                     (subcommands: status, pause, resume, clear)
/redraw              Force a full UI repaint (CLI)
```

### Configuration
```
/config              Show config (CLI)
/model [name]        Show or change model
/personality [name]  Set personality
/reasoning [level]   Set reasoning (none|minimal|low|medium|high|xhigh|show|hide)
/verbose             Cycle: off → new → all → verbose
/voice [on|off|tts]  Voice mode
/yolo                Toggle approval bypass
/busy [sub]          Control what Enter does while Hermes is working (CLI)
                     (subcommands: queue, steer, interrupt, status)
/indicator [style]   Pick the TUI busy-indicator style (CLI)
                     (styles: kaomoji, emoji, unicode, ascii)
/footer [on|off]     Toggle gateway runtime-metadata footer on final replies
/skin [name]         Change theme (CLI)
/statusbar           Toggle status bar (CLI)
```

### Tools & Skills
```
/tools               Manage tools (CLI)
/toolsets            List toolsets (CLI)
/skills              Search/install skills (CLI)
/skill <name>        Load a skill into session
/reload-skills       Re-scan ~/.hermes/skills/ for added/removed skills
/reload              Reload .env variables into the running session (CLI)
/reload-mcp          Reload MCP servers
/cron                Manage cron jobs (CLI)
/curator [sub]       Background skill maintenance (status, run, pin, archive, …)
/kanban [sub]        Multi-profile collaboration board (tasks, links, comments)
/plugins             List plugins (CLI)
```

### Gateway
```
/approve             Approve a pending command (gateway)
/deny                Deny a pending command (gateway)
/restart             Restart gateway (gateway)
/sethome             Set current chat as home channel (gateway)
/update              Update Hermes to latest (gateway)
/topic [sub]         Enable or inspect Telegram DM topic sessions (gateway)
/platforms (/gateway) Show platform connection status (gateway)
```

### Utility
```
/branch (/fork)      Branch the current session
/fast                Toggle priority/fast processing
/browser             Open CDP browser connection
/history             Show conversation history (CLI)
/save                Save conversation to file (CLI)
/copy [N]            Copy the last assistant response to clipboard (CLI)
/paste               Attach clipboard image (CLI)
/image               Attach local image file (CLI)
```

### Info
```
/help                Show commands
/commands [page]     Browse all commands (gateway)
/usage               Token usage
/insights [days]     Usage analytics
/gquota              Show Google Gemini Code Assist quota usage (CLI)
/status              Session info (gateway)
/profile             Active profile info
/debug               Upload debug report (system info + logs) and get shareable links
```

### Exit
```
/quit (/exit, /q)    Exit CLI
```

---

## Key Paths & Config

```
~/.hermes/config.yaml       Main configuration
~/.hermes/.env              API keys and secrets
$HERMES_HOME/skills/        Installed skills
~/.hermes/sessions/         Session transcripts
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/hermes-agent/     Source code (if git-installed)
```

Profiles use `~/.hermes/profiles/<name>/` with the same layout.

### Config Sections

Edit with `hermes config edit` or `hermes config set section.key value`.

| Section | Key options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |

Full config reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration

### Providers

20+ providers supported. Set via `hermes model` or `hermes setup`.

#### User-facing brevity for setup incidents

When Mikhail asks for a shorter answer (e.g. “короче”) or corrects verbosity during Hermes setup/auth work, switch immediately and permanently for the thread to a minimal Telegram format: 3–5 bullets max, no article-style explanations, no long recommendation lists, no repeated background. Include only: conclusion, what it means, next action. Deep dives only if he explicitly asks.

#### Choosing Claude paths for Hermes

When a user asks whether to run Claude through OpenRouter or Claude Code, distinguish the roles clearly and answer concisely first — especially for Telegram. Start with the recommendation, then only the commands needed.

- **Claude via OpenRouter** is best as a Hermes model/provider path: ordinary chat, Telegram sessions, planning, coordination, cron, lightweight code review, and multi-model fallback. It is simpler to operate, keeps Hermes in control of tool use, and is usually lower operational/account risk than automating a separate CLI heavily.
- **Claude Code CLI** is best as a specialized coding worker: bug fixes, feature implementation, repository refactors, test-fix loops, PR/security review, and long autonomous codebase work. Treat it as an executor that Hermes supervises rather than as a replacement for Hermes' main brain.
- **Subscriptions, third-party OAuth, and usage-credit limits:** Claude Pro/Max can authenticate Claude Code / third-party OAuth flows, but the API may reject third-party inference with a message like `Third-party apps now draw from your extra usage...`. Do not assume the UI exposes a separate `extra usage` control for every account/plan/region; report the exact API error, verify model IDs and OAuth credential state, and if the UI shows only ordinary Claude limits, treat this as an Anthropic account/plan gating issue rather than a Hermes proxy/auth failure. Once usage credits are enabled, OAuth may become partially usable: Haiku can succeed while Sonnet/Opus still return `429 rate_limit_error`. That is usually a model-class/session/weekly/acceleration limiter, not missing auth or broken proxy. Test OAuth-only explicitly when an API key is also configured, and do not use the API key if the user told you not to. OpenRouter is a separate account/balance; Anthropic API is separate token-metered billing. See `references/claude-oauth-usage-credits-rate-limits.md` for the per-model OAuth smoke pattern, 429 interpretation, retry guidance, and Haiku-vs-Sonnet positioning.
- **Recommended architecture for most users:** keep a stable/default Hermes model for general coordination, add OpenRouter Claude as an alternate or Claude-first provider when desired, and use Claude Code only for heavy repository tasks. If budget or account safety is a concern, prefer selective Claude use over making expensive Claude models the default for every Telegram turn.
- **Anthropic/OpenRouter auth-path triage:** keep Anthropic OAuth, Anthropic Console API key, and OpenRouter tests separate; do not change the default model/provider or restart the gateway after adding a key unless the user explicitly asks. For OAuth-only smoke when an API key is also present, load the OAuth credential from the pool directly so env `ANTHROPIC_API_KEY` cannot satisfy the test. See `references/claude-auth-provider-triage.md`.
- **Anthropic credential pool diagnostics:** when reporting OAuth vs API key usage, inspect `auth_type` (not `type`), `request_count` (not `usage_count`), and `access_token` prefix (`sk-ant-oat` = OAuth, `sk-ant-api` = Console API key). OAuth credentials bill against Claude Pro/Max subscription (subject to third-party extra-usage limits); API keys bill against Anthropic Console credits. See `references/anthropic-credential-pool-diagnostics.md`.
- **Cost framing:** API/OpenRouter billing is token-metered and can burn quickly during agent loops because file contents, tool outputs, diffs, logs, and repeated context all count. Subscriptions such as Claude Max may feel larger for manual/Claude Code usage, but still have usage limits; avoid uncontrolled parallelism or attempts to bypass limits.
- **Region/proxy-sensitive Claude setup:** if the user wants Claude/Anthropic to use the same VPS egress as ChatGPT/Codex without a full-device exit node, verify the gateway process env (`HTTP_PROXY`/`HTTPS_PROXY`, upper+lowercase), direct vs proxied egress, and restart-durable service env before authentication. For Claude subscription/OAuth, do not assume `--no-browser` is honored for Anthropic in all Hermes versions: the current Anthropic PKCE path may call `webbrowser.open()` directly. Use a safe `BROWSER` wrapper that launches the dedicated VPS Chrome profile (`--user-data-dir=$HOME/.chrome-vps-profile`, `--proxy-server=http://100.100.1.1:18080`, DNS block rules, QUIC disabled), or patch the Anthropic auth helper to accept/pass an `open_browser` flag, so login/payment/OAuth happen from the same VPS route. If the user gives the auth code via a local file/clipboard, keep it out of Telegram and logs; if the OAuth process restarts, require a fresh code from the newly opened URL because codes are state-bound. See `references/claude-anthropic-vps-oauth-file-code-runbook.md`. For Anthropic Console API billing, use `hermes auth add anthropic --type api-key` or `.env`, but do not pass keys on the command line or reveal them in summaries; when taking a key from clipboard/file, validate shape/suffix if provided, backup `.env`, smoke through the VPS proxy, then clear clipboard/temp files. If Claude OAuth is authenticated but third-party inference is gated, or if the user asks to use OpenRouter instead, use the OpenRouter fallback flow and credit-smoke interpretation in `references/claude-openrouter-vps-setup.md`. See also `references/claude-anthropic-vps-oauth-api-setup.md`.

| Provider | Auth | Key env var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |

OpenRouter key pitfall: user-provided keys may be pasted as the raw hex/body without the visible `sk-or-v1-` prefix. Normalize to `sk-or-v1-<body>` before storing in `~/.hermes/.env`, set file mode `600`, and verify with `GET https://openrouter.ai/api/v1/key` using `Authorization: Bearer <key>`. A 401 saying `Missing Authentication header` for the raw body can mean the prefix is missing, not that the key is necessarily invalid.
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` |
| Google Gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Z.AI / GLM | API key | `GLM_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| MiniMax CN | API key | `MINIMAX_CN_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| Alibaba / DashScope | API key | `DASHSCOPE_API_KEY` |
| Xiaomi MiMo | API key | `XIAOMI_API_KEY` |
| Kilo Code | API key | `KILOCODE_API_KEY` |
| AI Gateway (Vercel) | API key | `AI_GATEWAY_API_KEY` |
| OpenCode Zen | API key | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | API key | `OPENCODE_GO_API_KEY` |
| Qwen OAuth | OAuth | `hermes login --provider qwen-oauth` |
| Custom endpoint | Config | `model.base_url` + `model.api_key` in config.yaml |
| GitHub Copilot ACP | External | `COPILOT_CLI_PATH` or Copilot CLI |

Full provider docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

### Toolsets

Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.

| Toolset | What it provides |
|---------|-----------------|
| `web` | Web search and content extraction |
| `search` | Web search only (subset of `web`) |
| `browser` | Browser automation (Browserbase, Camofox, or local Chromium) |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `vision` | Image analysis |
| `image_gen` | AI image generation |
| `video` | Video analysis and generation |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `messaging` | Cross-platform message sending |
| `todo` | In-session task planning and tracking |
| `kanban` | Multi-agent work-queue tools (gated to workers) |
| `debugging` | Extra introspection/debug tools (off by default) |
| `safe` | Minimal, low-risk toolset for locked-down sessions |
| `spotify` | Spotify playback and playlist control |
| `homeassistant` | Smart home control (off by default) |
| `discord` | Discord integration tools |
| `discord_admin` | Discord admin/moderation tools |
| `feishu_doc` | Feishu (Lark) document tools |
| `feishu_drive` | Feishu (Lark) drive tools |
| `yuanbao` | Yuanbao integration tools |
| `rl` | Reinforcement learning tools (off by default) |
| `moa` | Mixture of Agents (off by default) |

Full enumeration lives in `toolsets.py` as the `TOOLSETS` dict; `_HERMES_CORE_TOOLS` is the default bundle most platforms inherit from.

Tool changes take effect on `/reset` (new session). They do NOT apply mid-conversation to preserve prompt caching.

---

## Security & Privacy Toggles

Common "why is Hermes doing X to my output / tool calls / commands?" toggles — and the exact commands to change them. Most of these need a fresh session (`/reset` in chat, or start a new `hermes` invocation) because they're read once at startup.

### Secret redaction in tool output

Secret redaction is **off by default** — tool output (terminal stdout, `read_file`, web content, subagent summaries, etc.) passes through unmodified. If the user wants Hermes to auto-mask strings that look like API keys, tokens, and secrets before they enter the conversation context and logs:

```bash
hermes config set security.redact_secrets true       # enable globally
```

**Restart required.** `security.redact_secrets` is snapshotted at import time — toggling it mid-session (e.g. via `export HERMES_REDACT_SECRETS=true` from a tool call) will NOT take effect for the running process. Tell the user to run `hermes config set security.redact_secrets true` in a terminal, then start a new session. This is deliberate — it prevents an LLM from flipping the toggle on itself mid-task.

Disable again with:
```bash
hermes config set security.redact_secrets false
```

### PII redaction in gateway messages

Separate from secret redaction. When enabled, the gateway hashes user IDs and strips phone numbers from the session context before it reaches the model:

```bash
hermes config set privacy.redact_pii true    # enable
hermes config set privacy.redact_pii false   # disable (default)
```

### Command approval prompts

By default (`approvals.mode: manual`), Hermes prompts the user before running shell commands flagged as destructive (`rm -rf`, `git reset --hard`, etc.). The modes are:

- `manual` — always prompt (default)
- `smart` — use an auxiliary LLM to auto-approve low-risk commands, prompt on high-risk
- `off` — skip all approval prompts (equivalent to `--yolo`)

```bash
hermes config set approvals.mode smart       # recommended middle ground
hermes config set approvals.mode off         # bypass everything (not recommended)
```

Per-invocation bypass without changing config:
- `hermes --yolo …`
- `export HERMES_YOLO_MODE=1`

Note: YOLO / `approvals.mode: off` does NOT turn off secret redaction. They are independent.

### Shell hooks allowlist

Some shell-hook integrations require explicit allowlisting before they fire. Managed via `~/.hermes/shell-hooks-allowlist.json` — prompted interactively the first time a hook wants to run.

### Disabling the web/browser/image-gen tools

To keep the model away from network or media tools entirely, open `hermes tools` and toggle per-platform. Takes effect on next session (`/reset`). See the Tools & Skills section above.

---

## Voice & Transcription

### STT (Voice → Text)

Voice messages from messaging platforms are auto-transcribed.

Provider priority (auto-detected):
1. **Local faster-whisper** — free, no API key: `pip install faster-whisper`
2. **Groq Whisper** — free tier: set `GROQ_API_KEY`
3. **OpenAI Whisper** — paid: set `VOICE_TOOLS_OPENAI_KEY`
4. **Mistral Voxtral** — set `MISTRAL_API_KEY`

Config:
```yaml
stt:
  enabled: true
  provider: local        # local, groq, openai, mistral
  local:
    model: base          # tiny, base, small, medium, large-v3
```

### TTS (Text → Voice)

| Provider | Env var | Free? |
|----------|---------|-------|
| Edge TTS | None | Yes (default) |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid |
| MiniMax | `MINIMAX_API_KEY` | Paid |
| Mistral (Voxtral) | `MISTRAL_API_KEY` | Paid |
| NeuTTS (local) | None (`pip install neutts[all]` + `espeak-ng`) | Free |

Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.

---

## Spawning Additional Hermes Instances

Run additional Hermes processes as fully independent subprocesses — separate sessions, tools, and environments.

### When to Use This vs delegate_task

| | `delegate_task` | Spawning `hermes` process |
|-|-----------------|--------------------------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Tool access | Subset of parent's tools | Full tool access |
| Interactive | No | Yes (PTY mode) |
| Use case | Quick parallel subtasks | Long autonomous missions |

### One-Shot Mode

```
terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)

# Background for long tasks:
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)
```

### Interactive PTY Mode (via tmux)

Hermes uses prompt_toolkit, which requires a real terminal. Use tmux for interactive spawning:

```
# Start
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)

# Wait for startup, then send a message
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)

# Read output
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)

# Send follow-up
terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)

# Exit
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

### Multi-Agent Coordination

```
# Agent A: backend
terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)

# Agent B: frontend
terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)

# Check progress, relay context between them
terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)
terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)
```

### Session Resume

```
# Resume most recent session
terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)

# Resume specific session
terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)
```

### Tips

- **Prefer `delegate_task` for quick subtasks** — less overhead than spawning a full process
- **Use `-w` (worktree mode)** when spawning agents that edit code — prevents git conflicts
- **Set timeouts** for one-shot mode — complex tasks can take 5-10 minutes
- **Use `hermes chat -q` for fire-and-forget** — no PTY needed
- **Use tmux for interactive sessions** — raw PTY mode has `\r` vs `\n` issues with prompt_toolkit
- **For scheduled tasks**, use the `cronjob` tool instead of spawning — handles delivery and retry

---

### Durable & Background Systems

Four systems run alongside the main conversation loop. Quick reference
here; full developer notes live in `AGENTS.md`, user-facing docs under
`website/docs/user-guide/features/`.

**Subconscious / long-term cognition development:** when the user asks how Hermes' "subconscious" works or how to develop it, treat this as the combined system of built-in memory, session search, skills, memory-provider plugins, cron reflection, and delegation feedback. Start with a plain-language summary, then propose a layered roadmap (working, episodic, semantic, procedural memory; recall-before-answer; reflection; forgetting/hygiene). For Agentic Stack topic `1347 / Subconscious`, keep Hermes in the coordinator/reviewer role and have Bud/OpenClaw execute after approval; verify Bud's implementation with smoke/status checks before reporting completion. Do not switch from active `subconscious` to Hindsight/Mem0 just because plugin files exist: first audit dependencies, keys/URLs, local instance readiness, and run Hindsight in staging if heavy install or secrets are needed. For major upgrades (metrics, forgetting, conflict detection), write a formal spec document covering schema, methods, tests, acceptance criteria, and rollout plan; delegate implementation to Bud via shaw; verify with baseline smoke after merge. See `references/subconscious-memory-development.md` for the condensed repo/social research notes, Hindsight readiness checks, and recommended architecture. See `references/subconscious-upgrade-spec-20260522.md` for the metrics/forgetting/conflict-detection upgrade pattern. See `references/subconscious-decision-memory-research.md` for the decision-state layer pattern: append-only decisions/cancellations, owner/next-action tracking, derived current state, recall-before-answer briefs, stale/conflict detection, and the Perplex/Sonar social-research workflow. See `references/local-subconscious-hindsight-staging.md` for the local-first implementation pattern: active `subconscious` as main provider, topic-aware graph/hybrid recall, fact-based daily/morning reports, weekly consciousness/autonomy reports with explicit next steps, what-was-reflected/what-improved/what-next blocks, multiple improvements when tests justify them, and fully local/no-pay Hindsight staging with Ollama/local LLM. Mikhail expects the Subconscious/Server-doctor improvement loop to be grounded in probes/stress tests, slow-process detection, garbage cleanup, architecture refactoring, and deep research of agentic best practices (GitHub, docs/blogs, social via Perplex/Sonar; no direct x.com scraping as primary path). Perplex/Sonar helper pitfall on this Mac: the working key lives in `/Users/xbr/.openclaw/workspace/.env`; dotenv lines may be `NAME=value` without `export`, so Bash helpers must explicitly export Perplexity vars or parse only `PERPLEXITY_*` keys before launching Python/cron subprocesses. Do not `source` arbitrary Hermes/OpenClaw `.env` files wholesale because shell-unsafe values with spaces can break non-interactive runs. See `references/local-subconscious-nightly-quality-review.md` for the product-style nightly review pattern: soft hygiene, 5-7 recall quality probes over durable decisions, explicit Hindsight separation, and the limitation that lexical probes are only a baseline before live recall smoke. See `references/subconscious-manager-report-format.md` for Mikhail-facing Subconscious reports: conclusions first, concrete improvements + what they give, weak architecture gaps, next work, and no meaningless metrics/raw cron logs. See `references/subconscious-finish-plan-review-20260521.md` for the concrete finish-plan pattern after Mikhail's correction: always include next steps, weekly consciousness/autonomy blocks, hard-negative recall probes, explicit Hermes-vs-Bud completion status, concise Russian manager reporting, and the Bud non-response close-the-loop rule (`@iq5000_bot /task ...` explicit wake, board sync/verification, no watcher-only stopping point). See `references/subconscious-hindsight-comparison-runbook.md` for the 24h comparison pattern: baseline snapshot, silent 6h sampler, one-shot final report, recall probes, and concise verdict format.

- **Agentic Stack / Subconscious topic execution rule:** in `Agentic Stack` topic `1347 / Subconscious`, Hermes remains coordinator/reviewer. Bud/OpenClaw is the executor after Bud approval; do not self-execute implementation/runtime/file changes in that lane unless Mikhail explicitly reassigns execution to Hermes. Hermes should fact-check, route work publicly with a `correlation_id`, wait for Bud's approval/execution report, then verify and summarize. Hindsight should be staged only after dependency/auth readiness is proven; if not ready, keep the active local `subconscious` provider as the safe fallback.

- **Agentic Stack global coding/Shaw rule:** substantial software work in any active topic (feature, refactor, risky bugfix, tests, PR, bot/gateway/integration/runtime code, or multi-file implementation) routes to Bud/OpenClaw using `shaw`; trivial read-only inspection, explanation, one-line edits, and research stay lightweight. When verifying this rule, distinguish source-of-truth docs (`chats.yaml`, `chats.md`, skills) from OpenClaw runtime prompts in `~/.openclaw/openclaw.json`; runtime acceptance needs a safe OpenClaw reload/restart and status smoke, covered by the `server-doctor` reference `openclaw-runtime-prompt-policy-finalization.md`.

**Agentic Stack architecture map:** maintain the durable map before proposing architecture changes. Generator: `/Users/xbr/.agentic-stack/architecture_map.py`; outputs: `/Users/xbr/.agentic-stack/architecture/agentic-stack-architecture-map.md`, `.json`, and `.html`. The map must tie together processes, topic routing, Bud/OpenClaw roles, memory/state stores, cron jobs, and bottlenecks. A silent drift cron (`Agentic Stack architecture map drift check`) runs every 6h and reports to `Server-doctor` only on material drift. Weekly architecture deep research must read/regenerate this map first and use it as the baseline.

**Reviewing OpenClaw/Hermes runtime plugin fixes:** verify production-shaped typed hooks, not just hand-built smoke fixtures. For `before_prompt_build`, production calls handlers as `handler({ prompt, messages }, ctx)`; config should come from `api.pluginConfig` captured at `register(api)` or a config snapshot fallback, not from `event.context.pluginConfig`. Separate code acceptance from runtime acceptance: if the gateway process started before the plugin file mtime, a restart is required before a real dry-run Telegram turn can prove the fix. See `references/openclaw-plugin-production-hook-review.md` for the checklist.

**Hermes → Bud capability sync rule:** when Hermes installs, creates, or significantly improves a skill/workflow/helper for itself, explicitly assess whether the executor Bud/OpenClaw would benefit. If yes, sync the class-level skill/workflow to Bud as well, adapting paths/secrets and verifying the copied artifact. This keeps Bud from lagging behind Hermes in reusable operational knowledge.

**Agentic Stack Subconscious execution rule:** in Telegram Agentic Stack / Subconscious topic 1347, Hermes' role stays coordinator/reviewer. Bud/OpenClaw is the executor after Bud's public approval. Do not silently implement the six-point subconscious roadmap yourself in that topic; hand the approved plan to Bud, wait for Bud's approve/changes, then have Bud execute and return smoke/status. Hermes may fact-check, prepare context, review results, and summarize, but implementation should be routed to Bud unless Mikhail explicitly changes roles.

### Delegation (`delegate_task`)

Synchronous subagent spawn — the parent waits for the child's summary
before continuing its own loop. Isolated context + terminal session.

- **Single:** `delegate_task(goal, context, toolsets)`.
- **Batch:** `delegate_task(tasks=[{goal, ...}, ...])` runs children in
  parallel, capped by `delegation.max_concurrent_children` (default 3).
- **Roles:** `leaf` (default; cannot re-delegate) vs `orchestrator`
  (can spawn its own workers, bounded by `delegation.max_spawn_depth`).
- **Not durable.** If the parent is interrupted, the child is
  cancelled. For work that must outlive the turn, use `cronjob` or
  `terminal(background=True, notify_on_complete=True)`.

Config: `delegation.*` in `config.yaml`.

### Cron (scheduled jobs)

Durable scheduler — `cron/jobs.py` + `cron/scheduler.py`. Drive it via
`cronjob` tool, the `hermes cron` CLI (`list`, `add`, `edit`,
`pause`, `resume`, `run`, `remove`), or the `/cron` slash command.

- **Schedules:** duration (`"30m"`, `"2h"`), "every" phrase
  (`"every monday 9am"`), 5-field cron (`"0 9 * * *"`), or ISO timestamp.
- **Per-job knobs:** `skills`, `model`/`provider` override, `script`
  (pre-run data collection; `no_agent=True` makes the script the whole
  job), `context_from` (chain job A's output into job B), `workdir`
  (run in a specific dir with its `AGENTS.md` / `CLAUDE.md` loaded),
  multi-platform delivery.
- **Invariants:** 3-minute hard interrupt per run, `.tick.lock` file
  prevents duplicate ticks across processes, cron sessions pass
  `skip_memory=True` by default, and cron deliveries are framed with a
  header/footer instead of being mirrored into the target gateway
  session (keeps role alternation intact).

**Reporting style for broad autonomous/cron investigations.** When a cron
job produces a dense architecture or reconnaissance report for a Telegram
conversation, do not deliver only the raw engineering artifact. Start with a
plain-language layer: "what this means", 3-5 key takeaways, the recommended
next decision, and the practical plan. Put paths, schema details, line-item
backlog, and implementation notes after that. If the user says they did not
understand the report, immediately translate it into human terms rather than
adding more jargon.

**Agentic Stack local TODO reminders.** When Mikhail asks to transform a raw
TODO/reminder list into a useful management format, update the Markdown source
and any reminder script together. Use a compact project/time-management shape,
but make the user-facing wording short and Russian-only: `Приоритет`, `Статус`,
`Этап`, `Ответственный`, `Пересмотр` (MSK), `Лимит времени`, `Результат`, and
exactly one `Следующий шаг`. Avoid English labels such as `Lane`, `Owner`,
`Timebox`, `Backlog`, `next`, `pending` in Telegram reports. Daily reminder
output should show max 3 focus items plus a short "Позже" section, not a flat
backlog; include blocker/decision only when it changes the user's next step. For
purchase/credential tasks such as buying Claude or integrating a Telegram user
account, track the human decision/purchase/security boundary separately from
agent setup/smoke-test work, start with read-only/draft mode when personal
accounts are involved, and never store secrets in TODO. See
`references/agentic-stack-local-todo-reminder.md`.

**Agentic Stack Telegram TODO topic / task-manager design.** When designing a
new Telegram TODO/Tasks topic, treat it as an index/control panel rather than a
new catch-all execution topic: work remains in Web Admin, Coding, Server-doctor,
Subconscious, etc.; TODO stores cards, status, owner, priority, stale/blocker
state, and source-context links. Prefer a small status vocabulary, one actionable
`Следующий шаг`, inline buttons for `В работу`/`Закрыть`/`Блокер`/`Пересмотр`/
`Приоритет`/`Назначить`, and SQLite/Hermes Kanban as the durable source of truth
with Telegram cards as UI. Important UX rule: buttons are for humans; agents
must manage agent-owned tasks through backend/API/DB/command handlers and update
cards themselves, not make Mikhail manually click through routine status changes.
For implementation gotchas — `/done` by reply, `source_message_id`/
`panel_message_id`, callback scope checks, `asyncio.to_thread` for SQLite,
agent control-plane vs human buttons, short-lived live-button watchers, and live
button acceptance — see `references/agentic-stack-telegram-todo-mvp-implementation.md`.
See `references/agentic-stack-telegram-todo-topic.md`.

User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron

**Cron report inventory and delivery audits.** When Mikhail asks which reports are scheduled, already ran, or where they will arrive, follow `references/cron-report-inventory-delivery-audit.md`: combine `cronjob list`, `~/.hermes/cron/jobs.json`, cron output files, and delivery logs; report in MSK; distinguish local-only jobs from Telegram topic deliveries.

### Curator (skill lifecycle)

Background maintenance for agent-created skills. Tracks usage, marks
idle skills stale, archives stale ones, keeps a pre-run tar.gz backup
so nothing is lost.

**Manual state checkpoint requests.** When the user asks to preserve current work, update/push skills, or make a backup before losing state, follow the active checkpoint recipe in `references/state-checkpoint-backup.md`: discover source-of-truth paths, update/commit/push skill repos with staged secret scan, create a timestamped redacted backup under `~/.hermes/backups/`, include git bundles/diffs/status, and verify tarballs plus remote HEADs before reporting. For automatic backup/commit/push of Hermes/OpenClaw/Agentic Stack artifacts to GitHub, treat it as external data export and follow `references/secure-agent-artifact-backup-github.md`: manifest-only, fresh staging, scanners + deny rules, local-only dry-run first, and Bud-owned cron/push with human approval. For full Agentic Stack preservation/Archivist design, use `references/agentic-stack-archivist-backup-system.md`: split GitHub-safe code/docs from encrypted private/secrets archives, classify data, replicate first to the Windows LAN machine, and verify by restore smoke rather than backup creation alone.

- **CLI:** `hermes curator <verb>` — `status`, `run`, `pause`, `resume`,
  `pin`, `unpin`, `archive`, `restore`, `prune`, `backup`, `rollback`.
- **Slash:** `/curator <subcommand>` mirrors the CLI.
- **Scope:** only touches skills with `created_by: "agent"` provenance.
  Bundled + hub-installed skills are off-limits. **Never deletes** —
  max destructive action is archive. Pinned skills are exempt from
  every auto-transition and every LLM review pass.
- **Telemetry:** sidecar at `~/.hermes/skills/.usage.json` holds
  per-skill `use_count`, `view_count`, `patch_count`,
  `last_activity_at`, `state`, `pinned`.

Config: `curator.*` (`enabled`, `interval_hours`, `min_idle_hours`,
`stale_after_days`, `archive_after_days`, `backup.*`).
User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/curator

### Kanban (multi-agent work queue)

Durable SQLite board for multi-profile / multi-worker collaboration.
Users drive it via `hermes kanban <verb>`; dispatcher-spawned workers
see a focused `kanban_*` toolset gated by `HERMES_KANBAN_TASK` so the
schema footprint is zero outside worker processes.

- **CLI verbs (common):** `init`, `create`, `list` (alias `ls`),
  `show`, `assign`, `link`, `unlink`, `comment`, `complete`, `block`,
  `unblock`, `archive`, `tail`. Less common: `watch`, `stats`, `runs`,
  `log`, `dispatch`, `daemon`, `gc`.
- **Worker toolset:** `kanban_show`, `kanban_complete`, `kanban_block`,
  `kanban_heartbeat`, `kanban_comment`, `kanban_create`, `kanban_link`.
- **Dispatcher** runs inside the gateway by default
  (`kanban.dispatch_in_gateway: true`) — reclaims stale claims,
  promotes ready tasks, atomically claims, spawns assigned profiles.
  Auto-blocks a task after ~5 consecutive spawn failures.
- **Isolation:** board is the hard boundary (workers get
  `HERMES_KANBAN_BOARD` pinned in env); tenant is a soft namespace
  within a board for workspace-path + memory-key isolation.

User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban

---

## Windows-Specific Quirks

Hermes runs natively on Windows (PowerShell, cmd, Windows Terminal, git-bash
mintty, VS Code integrated terminal). Most of it just works, but a handful
of differences between Win32 and POSIX have bitten us — document new ones
here as you hit them so the next person (or the next session) doesn't
rediscover them from scratch.

### Input / Keybindings

**Alt+Enter doesn't insert a newline.** Windows Terminal intercepts Alt+Enter
at the terminal layer to toggle fullscreen — the keystroke never reaches
prompt_toolkit. Use **Ctrl+Enter** instead. Windows Terminal delivers
Ctrl+Enter as LF (`c-j`), distinct from plain Enter (`c-m` / CR), and the
CLI binds `c-j` to newline insertion on `win32` only (see
`_bind_prompt_submit_keys` + the Windows-only `c-j` binding in `cli.py`).
Side effect: the raw Ctrl+J keystroke also inserts a newline on Windows —
unavoidable, because Windows Terminal collapses Ctrl+Enter and Ctrl+J to
the same keycode at the Win32 console API layer. No conflicting binding
existed for Ctrl+J on Windows, so this is a harmless side effect.

mintty / git-bash behaves the same (fullscreen on Alt+Enter) unless you
disable Alt+Fn shortcuts in Options → Keys. Easier to just use Ctrl+Enter.

**Diagnosing keybindings.** Run `python scripts/keystroke_diagnostic.py`
(repo root) to see exactly how prompt_toolkit identifies each keystroke
in the current terminal. Answers questions like "does Shift+Enter come
through as a distinct key?" (almost never — most terminals collapse it
to plain Enter) or "what byte sequence is my terminal sending for
Ctrl+Enter?" This is how the Ctrl+Enter = c-j fact was established.

### Config / Files

**HTTP 400 "No models provided" on first run.** `config.yaml` was saved
with a UTF-8 BOM (common when Windows apps write it). Re-save as UTF-8
without BOM. `hermes config edit` writes without BOM; manual edits in
Notepad are the usual culprit.

### `execute_code` / Sandbox

**WinError 10106** ("The requested service provider could not be loaded
or initialized") from the sandbox child process — it can't create an
`AF_INET` socket, so the loopback-TCP RPC fallback fails before
`connect()`. Root cause is usually **not** a broken Winsock LSP; it's
Hermes's own env scrubber dropping `SYSTEMROOT` / `WINDIR` / `COMSPEC`
from the child env. Python's `socket` module needs `SYSTEMROOT` to locate
`mswsock.dll`. Fixed via the `_WINDOWS_ESSENTIAL_ENV_VARS` allowlist in
`tools/code_execution_tool.py`. If you still hit it, echo `os.environ`
inside an `execute_code` block to confirm `SYSTEMROOT` is set. Full
diagnostic recipe in `references/execute-code-sandbox-env-windows.md`.

### Testing / Contributing

**`scripts/run_tests.sh` doesn't work as-is on Windows** — it looks for
POSIX venv layouts (`.venv/bin/activate`). The Hermes-installed venv at
`venv/Scripts/` has no pip or pytest either (stripped for install size).
Workaround: install `pytest + pytest-xdist + pyyaml` into a system Python
3.11 user site, then invoke pytest directly with `PYTHONPATH` set:

```bash
"/c/Program Files/Python311/python" -m pip install --user pytest pytest-xdist pyyaml
export PYTHONPATH="$(pwd)"
"/c/Program Files/Python311/python" -m pytest tests/foo/test_bar.py -v --tb=short -n 0
```

Use `-n 0`, not `-n 4` — `pyproject.toml`'s default `addopts` already
includes `-n`, and the wrapper's CI-parity guarantees don't apply off POSIX.

**POSIX-only tests need skip guards.** Common markers already in the codebase:
- Symlinks — elevated privileges on Windows
- `0o600` file modes — POSIX mode bits not enforced on NTFS by default
- `signal.SIGALRM` — Unix-only (see `tests/conftest.py::_enforce_test_timeout`)
- Winsock / Windows-specific regressions — `@pytest.mark.skipif(sys.platform != "win32", ...)`

Use the existing skip-pattern style (`sys.platform == "win32"` or
`sys.platform.startswith("win")`) to stay consistent with the rest of the
suite.

### Path / Filesystem

**Line endings.** Git may warn `LF will be replaced by CRLF the next time
Git touches it`. Cosmetic — the repo's `.gitattributes` normalizes. Don't
let editors auto-convert committed POSIX-newline files to CRLF.

**Forward slashes work almost everywhere.** `C:/Users/...` is accepted by
every Hermes tool and most Windows APIs. Prefer forward slashes in code
and logs — avoids shell-escaping backslashes in bash.

---

## Troubleshooting

### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `pip install faster-whisper` or set API key
3. If Telegram voice arrives but local STT says `whisper wrapper: model file not found`, verify `WHISPER_CPP_MODEL` and the model file. If the model exists but the cached Telegram `.ogg` still fails, check whether `tools.transcription_tools` is passing `--model base` (a model name) into a `whisper.cpp` compatibility wrapper that expects a file path. Patch the wrapper to resolve model names (`base`, `small`, etc.) to `ggml-*.bin` paths before erroring; also set `stt.local.language` to `auto` or an explicit language so Russian voice is not transcribed as English translation. See `references/local-stt-whisper-wrapper.md` for the concise fix pattern and `references/hermes-telegram-stt-routing-debug.md` for the broader routing/debug smoke commands.
4. Manual recovery path: find the newest/relevant `~/.hermes/cache/audio/*.ogg`, convert it to 16 kHz mono WAV with `ffmpeg -y -i input.ogg -ar 16000 -ac 1 -c:a pcm_s16le /tmp/hermes_voice.wav`, then run `whisper-cli -m "$WHISPER_CPP_MODEL" -f /tmp/hermes_voice.wav -l auto -otxt -of /tmp/hermes_voice` (adjust language as needed). This is a recovery technique, not proof STT is permanently broken.
5. If the user links a private Telegram voice message like `https://t.me/c/<internal_chat>/<message_id>` and it is not in the local audio cache, do not guess from the newest cached `.ogg`. Use the Telegram Bot API recovery path if the bot is a member of the source chat: `forwardMessage` from `chat_id=-100<internal_chat>` and `message_id=<message_id>` into a deletable chat/topic, read the returned `voice.file_id`, `getFile`, download via `/file/bot<TOKEN>/<file_path>`, immediately `deleteMessage` the temporary forward, then transcribe the downloaded file. If forwarding to the user's DM fails with `VOICE_MESSAGES_FORBIDDEN`, forward into an allowed group topic and delete the temporary copy. Bot API has no direct `getMessage`, so forwarding is the practical lookup.
6. Avoid unnecessary restarts while fixing wrapper/config issues: the wrapper is executed per STT call, so wrapper fixes can take effect without restarting the gateway. Config changes still generally need a new session/gateway restart unless the current path re-reads config per call; verify with `transcribe_audio()` smoke before restarting.

### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes login` — re-authenticate OAuth providers
3. Check `.env` has the right API key
4. **Region/proxy ambiguity:** do not equate “Tailscale exit node is off” with “Hermes cannot use the VPS.” Hermes/Bud/OpenClaw may route provider calls through per-process `HTTP_PROXY`/`HTTPS_PROXY` even while the Mac's full-device exit node and macOS system proxy are disabled. For gateway/provider debugging, verify clean direct IP, proxied IP, `chatgpt.com/cdn-cgi/trace`, the actual gateway PID env (`ps eww -p <pid>`), and the LaunchAgent/unit `EnvironmentVariables`. If the live process has proxy but the launchd plist does not, it is not restart-durable; add uppercase/lowercase proxy vars to the service env, then drain/restart/smoke. For Claude/Anthropic account setup through a VPS browser profile plus Hermes proxy env, follow `references/claude-anthropic-vps-oauth-api-setup.md`.
5. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `/skill name` or `hermes -s name`

### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Common gateway problems:
- **Telegram public agent-agent coordination:** a public `@other_bot` mention from Hermes may not wake another Telegram bot even if the executor gateway logs an inbound topic message. If the user requires all agent-agent messages to be visible in the topic, use a public bridge mode as fallback: Hermes posts the handoff publicly, invokes the executor through the reliable local/API bridge, and sends the executor's response publicly back into the topic. For native Telegram bot-to-bot smoke tests, verify the sender identity (`from.username`), `chat_id`, topic/thread id, and correlation ID; do not use the executor's own send helper as proof of Hermes→executor delivery. When the user asks to *demonstrate* Hermes↔Bud communication publicly, send a visible `/task@OtherBot correlation_id=... max_hops=...` handoff, optionally mirror it into the shared local queue/board, and report concrete evidence (`message_id`, `correlation_id`, task id). See `references/telegram-topic-identity-routing.md`, `references/telegram-bot-to-bot-communication.md`, and `references/telegram-public-coordination-demo.md`.
- **Agentic Stack bot wake/routing regression:** In `MM / topic 642` and public Agentic Stack handoffs that need Bud to answer in-topic, do not conflate "Bud is not default responder" with "Bud ignores direct mentions." Quick `@iq5000_bot` questions should wake Bud; quick `@ceo5000_bot` questions should wake Hermes; `/task@iq5000_bot correlation_id=...` is for formal board/watchdog lifecycle tasks but may not be the most reliable wake path in every topic/tool path. If Bud review/ACK is required and `/task@iq5000_bot` stays pending, retry as visible explicit mention: `@iq5000_bot /task correlation_id=... hops=0 max_hops=...`, then ensure the outbound logger/board parser recognizes that format too. Explicit bot mention must override reply context: reply-to-Bud + `@ceo5000_bot` wakes Hermes, and reply-to-Hermes + `@iq5000_bot` wakes Bud. If either bot stops answering direct tags, treat it as a routing/wake regression and check `references/telegram-bud-wake-protocol.md`.
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`

- **Platform-specific issues**
- **Agentic Stack topic inventory + skill preservation**: when mapping Agentic Stack topics, preserve the per-topic skill sets Bud/OpenClaw used and the durable conversation history for each topic; Hermes may answer directly only after loading the relevant topic skills, otherwise it should triage/delegate execution-heavy work to Bud. Global coding rule: if any active topic turns into non-trivial software work (feature, refactor, risky bugfix, tests, PR, bot/gateway/integration/runtime code, or multi-file implementation), delegate Bud/OpenClaw with `use shaw`; keep trivial read-only/one-line/explanation/research work lightweight. When a user provides a Telegram forum link like `https://t.me/c/<internal_chat>/<topic_id>/<message_id>`, parse it as authoritative evidence for the topic ID (`chat_id=-100<internal_chat>`, `topic_id=<second path segment>`) and reconcile any stale historical mappings rather than asking for another ping. If the user pushes with “и?”/“and?”, do not explain what should happen next — immediately execute the missing close-the-loop action (e.g. ask Bud for ACK, mark inventory final, validate files) and report only the result. After closing inventory, be ready to answer the practical follow-up: what is required from the user, which topics have rules, and what skills/context bind to each topic. For 642/723 deprecation or moving coordination into all domain topics, do **not** tell the user to delete Telegram topics immediately: first run/read a dependency audit covering cron delivery, hardcoded board/watchdog/queue/outbound logger/router scripts, docs/skills/memory refs, OpenClaw/Bud topic policies, and history stores; then migrate, smoke in 2–3 domain topics, and only then archive/delete. See `references/agentic-stack-topic-inventory-role-mapping.md` and `references/agentic-stack-topic-deprecation-migration.md`.
- **Agentic Stack topic-642 board sync/autopilot notes**: see `references/telegram-agentic-stack-board-sync-autopilot.md` for the scoped Hermes↔Bud carte-blanche workflow, topic-scoped stack goal framing (`642`/`723` are registered lanes, not the whole stack), safe defaults for other topics, triple-verification expectation after goal completion, minimal fail-open board auto-sync via logging helpers, and the parser pitfall where `approved=yes status=completed` must be treated as completed rather than merely approved. When Mikhail explicitly approves the goal and grants carte blanche, do not wait for per-step approval: coordinate with Bud autonomously until DoD or a real blocker, then stop and report manager-to-manager (value/results/risks/next steps, minimal technical detail unless asked). In user-facing Agentic Stack reports, refer to Telegram topics by visible title (e.g. `MM`, `MM Only`, `Server-doctor`) and omit numeric topic IDs unless Mikhail asks for technical detail or an ID is needed to disambiguate.
- **Telegram forum topics are scoped contexts**: If a user sets a reply/routing rule in a Telegram group topic/thread, scope it to that topic id unless they explicitly say it applies to the whole group. Do not infer that a mentioned `@bot_username` is Hermes; multi-agent groups may contain OpenClaw or other bots with their own tags and rules. Reply-to-specific-agent and explicit mentions should be handled before default response behavior, preferably by pre-LLM gateway routing from a shared topic-scoped file (`chats.md` / `routing-rules.md`). In Hermes' own Telegram adapter, `free_response_topics` and `require_mention` are pre-LLM gates inside `_should_process_message()`; if the user observes "starts answering, then cancels", inspect busy-input interruption/concurrency separately before blaming topic routing. See `references/hermes-telegram-stt-routing-debug.md` for the exact wake-path order and diagnostic grep patterns. If the user quotes/replies with another bot's message, treat that quoted content as visible context rather than saying you did not see it. For multi-agent "Hermes as head / another bot as executor" setups, prefer a shared router + event log + task queue over user-relayed Telegram messages, and roll it out cautiously: documented-only rules → passive logging → dry-run routing → soft enforcement → task queue/bridge. If the user says they communicate only with Hermes/a coordinator bot in a specific topic and expects untagged replies, do **not** rely on memory alone: memory loads after the gateway has already decided whether to wake the agent. Keep global `require_mention` enabled by default and add a chat+topic-specific free-response/default-responder rule instead; see `references/telegram-topic-free-response-routing.md`. If the user wants **all agent-agent messages visible in the topic**, do not treat a private queue/bridge as sufficient two-way communication. Telegram Bot API 10.0 supports native Bot-to-Bot Communication only after BotFather mode is enabled; reliable public addressing is `/command@OtherBot` or direct reply, not a plain `@OtherBot` mention. Probe both bot tokens for `USER_BOT_TO_BOT_DISABLED`, `can_read_all_group_messages`, and privacy/admin state, then add loop guards before enabling autonomous bot↔bot replies. If the user defines a coordinator/executor workflow, follow the explicit sequence: coordinator proposes/designs, executor publicly approves or objects, then executor implements; do not silently start implementation or wait for approval without saying so. For auditable public handoffs, use explicit `correlation_id` values and, if building a watchdog, keep it passive/stdlib-only at first: scan topic-scoped event logs, detect missing ACKs after a timeout, and report JSON/JSONL without sending Telegram messages or changing routing. Important pitfall: a watchdog cannot see coordinator-originated tasks unless Hermes outbound `/task@OtherBot correlation_id=...` sends are logged into the same event log with the returned `message_id`; otherwise `checked_tasks=0` is a logging-visibility problem, not proof that no tasks were sent. For the minimal fix, append an idempotent synthetic outbound event after a successful send, preserving the exact public task text and returned `message_id`; see `references/telegram-bot-to-bot-outbound-logging.md`. In Agentic Stack-style public task workflows, prefer sending Bud/OpenClaw tasks through `send_message` or another explicitly logged outbound path rather than placing `/task@OtherBot ...` only in the assistant's final response; final-response text may be visible in Telegram but bypass the outbound logger, leading to `ack_without_logged_chat_task` watchdog warnings. For the topic-642 board-sync/watchdog pattern, including auto-sync from logging helpers, board-vs-chat consistency checks, and the `approved=yes status=completed` parsing pitfall, see `references/telegram-agentic-stack-board-sync-watchdog.md`. Distinguish approval ACKs from completion ACKs before treating duplicate ACKs as errors. When user participation is needed in a topic, explicitly say what is needed and tag the user's actual username from context, not a display name placeholder. If you store memory, include the group + topic/thread id and keep Hermes identity separate from other bot usernames. See `references/telegram-topic-identity-routing.md`, `references/telegram-bot-to-bot-communication.md`, `references/telegram-bot-to-bot-watchdog.md`, `references/telegram-bot-to-bot-outbound-logging.md`, `references/telegram-agentic-stack-task-board.md`, `references/agentic-stack-topic-router-audit.md`, `references/agentic-stack-architecture-recon.md`, `references/agentic-stack-v2-blueprint-research.md`, `references/agentic-stack-topic-inventory-role-mapping.md`, and `references/telegram-topic-free-response-routing.md` for the proposal→executor-approval→implementation audit pattern, watchdog/outbound logging pattern, topic-642 SQLite task-board lifecycle pattern, read-only architecture recon/report workflow, Agentic Stack v2 role/swarm blueprint recommendations, topic inventory + role mapping, and topic-specific untagged routing pattern.
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows-specific issues** (`Alt+Enter` newline, WinError 10106, UTF-8 BOM config, test suite, line endings): see the dedicated **Windows-Specific Quirks** section above.

### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider <your_provider>
hermes config set auxiliary.vision.model <model_name>
```

---

## Where to Find Things

| Looking for... | Location |
|----------------|----------|
| Config options | `hermes config edit` or [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Available tools | `hermes tools list` or [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) |
| Slash commands | `/help` in session or [Slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands) |
| Skills catalog | `hermes skills browse` or [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `hermes model` or [Providers guide](https://hermes-agent.nousresearch.com/docs/integrations/providers) |
| Platform setup | `hermes gateway setup` or [Messaging docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) |
| MCP servers | `hermes mcp list` or [MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) |
| Profiles | `hermes profile list` or [Profiles docs](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |
| Cron jobs | `hermes cron list` or [Cron docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) |
| Memory | `hermes memory status` or [Memory docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) |
| Env variables | `hermes config env-path` or [Env vars reference](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) |
| CLI commands | `hermes --help` or [CLI reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| Gateway logs | `~/.hermes/logs/gateway.log` |
| Session files | `~/.hermes/sessions/` or `hermes sessions browse` |
| Source code | `~/.hermes/hermes-agent/` |

---

## Contributor Quick Reference

For occasional contributors and PR authors. Full developer docs: https://hermes-agent.nousresearch.com/docs/developer-guide/

### Project Layout

```
hermes-agent/
├── run_agent.py          # AIAgent — core conversation loop
├── model_tools.py        # Tool discovery and dispatch
├── toolsets.py           # Toolset definitions
├── cli.py                # Interactive CLI (HermesCLI)
├── hermes_state.py       # SQLite session store
├── agent/                # Prompt builder, context compression, memory, model routing, credential pooling, skill dispatch
├── hermes_cli/           # CLI subcommands, config, setup, commands
│   ├── commands.py       # Slash command registry (CommandDef)
│   ├── config.py         # DEFAULT_CONFIG, env var definitions
│   └── main.py           # CLI entry point and argparse
├── tools/                # One file per tool
│   └── registry.py       # Central tool registry
├── gateway/              # Messaging gateway
│   └── platforms/        # Platform adapters (telegram, discord, etc.)
├── cron/                 # Job scheduler
├── tests/                # ~3000 pytest tests
└── website/              # Docusaurus docs site
```

Config: `~/.hermes/config.yaml` (settings), `~/.hermes/.env` (API keys).

### Adding a Tool (3 files)

**1. Create `tools/your_tool.py`:**
```python
import json, os
from tools.registry import registry

def check_requirements() -> bool:
    return bool(os.getenv("EXAMPLE_API_KEY"))

def example_tool(param: str, task_id: str = None) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="example_tool",
    toolset="example",
    schema={"name": "example_tool", "description": "...", "parameters": {...}},
    handler=lambda args, **kw: example_tool(
        param=args.get("param", ""), task_id=kw.get("task_id")),
    check_fn=check_requirements,
    requires_env=["EXAMPLE_API_KEY"],
)
```

**2. Add to `toolsets.py`** → `_HERMES_CORE_TOOLS` list.

Auto-discovery: any `tools/*.py` file with a top-level `registry.register()` call is imported automatically — no manual list needed.

All handlers must return JSON strings. Use `get_hermes_home()` for paths, never hardcode `~/.hermes`.

### Adding a Slash Command

1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Add handler in `cli.py` → `process_command()`
3. (Optional) Add gateway handler in `gateway/run.py`

All consumers (help text, autocomplete, Telegram menu, Slack mapping) derive from the central registry automatically.

### Agent Loop (High Level)

```
run_conversation():
  1. Build system prompt
  2. Loop while iterations < max:
     a. Call LLM (OpenAI-format messages + tool schemas)
     b. If tool_calls → dispatch each via handle_function_call() → append results → continue
     c. If text response → return
  3. Context compression triggers automatically near token limit
```

### Testing

```bash
python -m pytest tests/ -o 'addopts=' -q   # Full suite
python -m pytest tests/tools/ -q            # Specific area
```

- Tests auto-redirect `HERMES_HOME` to temp dirs — never touch real `~/.hermes/`
- Run full suite before pushing any change
- Use `-o 'addopts='` to clear any baked-in pytest flags
- When running tests from cron/scheduled Hermes, clear scheduler delivery env in tests that call `send_message_tool` directly (`HERMES_CRON_AUTO_DELIVER_PLATFORM`, `HERMES_CRON_AUTO_DELIVER_CHAT_ID`, `HERMES_CRON_AUTO_DELIVER_THREAD_ID`) or set all three explicitly; otherwise duplicate-delivery guards can make ordinary sends return `skipped=true` and create false failures.

**Windows contributors:** `scripts/run_tests.sh` currently looks for POSIX venvs (`.venv/bin/activate` / `venv/bin/activate`) and will error out on Windows where the layout is `venv/Scripts/activate` + `python.exe`. The Hermes-installed venv at `venv/Scripts/` also has no `pip` or `pytest` — it's stripped for end-user install size. Workaround: install pytest + pytest-xdist + pyyaml into a system Python 3.11 user site (`/c/Program Files/Python311/python -m pip install --user pytest pytest-xdist pyyaml`), then run tests directly:

```bash
export PYTHONPATH="$(pwd)"
"/c/Program Files/Python311/python" -m pytest tests/tools/test_foo.py -v --tb=short -n 0
```

Use `-n 0` (not `-n 4`) because `pyproject.toml`'s default `addopts` already includes `-n`, and the wrapper's CI-parity story doesn't apply off-POSIX.

**Cross-platform test guards:** tests that use POSIX-only syscalls need a skip marker. Common ones already in the codebase:
- Symlink creation → `@pytest.mark.skipif(sys.platform == "win32", reason="Symlinks require elevated privileges on Windows")` (see `tests/cron/test_cron_script.py`)
- POSIX file modes (0o600, etc.) → `@pytest.mark.skipif(sys.platform.startswith("win"), reason="POSIX mode bits not enforced on Windows")` (see `tests/hermes_cli/test_auth_toctou_file_modes.py`)
- `signal.SIGALRM` → Unix-only (see `tests/conftest.py::_enforce_test_timeout`)
- Live Winsock / Windows-specific regression tests → `@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific regression")`

**Monkeypatching `sys.platform` is not enough** when the code under test also calls `platform.system()` / `platform.release()` / `platform.mac_ver()`. Those functions re-read the real OS independently, so a test that sets `sys.platform = "linux"` on a Windows runner will still see `platform.system() == "Windows"` and route through the Windows branch. Patch all three together:

```python
monkeypatch.setattr(sys, "platform", "linux")
monkeypatch.setattr(platform, "system", lambda: "Linux")
monkeypatch.setattr(platform, "release", lambda: "6.8.0-generic")
```

See `tests/agent/test_prompt_builder.py::TestEnvironmentHints` for a worked example.

### Extending the system prompt's execution-environment block

Factual guidance about the host OS, user home, cwd, terminal backend, and shell (bash vs. PowerShell on Windows) is emitted from `agent/prompt_builder.py::build_environment_hints()`. This is also where the WSL hint and per-backend probe logic live. The convention:

- **Local terminal backend** → emit host info (OS, `$HOME`, cwd) + Windows-specific notes (hostname ≠ username, `terminal` uses bash not PowerShell).
- **Remote terminal backend** (anything in `_REMOTE_TERMINAL_BACKENDS`: `docker, singularity, modal, daytona, ssh, vercel_sandbox, managed_modal`) → **suppress** host info entirely and describe only the backend. A live `uname`/`whoami`/`pwd` probe runs inside the backend via `tools.environments.get_environment(...).execute(...)`, cached per process in `_BACKEND_PROBE_CACHE`, with a static fallback if the probe times out.
- **Key fact for prompt authoring:** when `TERMINAL_ENV != "local"`, *every* file tool (`read_file`, `write_file`, `patch`, `search_files`) runs inside the backend container, not on the host. The system prompt must never describe the host in that case — the agent can't touch it.

Full design notes, the exact emitted strings, and testing pitfalls:
`references/prompt-builder-environment-hints.md`.

**Refactor-safety pattern (POSIX-equivalence guard):** when you extract inline logic into a helper that adds Windows/platform-specific behavior, keep a `_legacy_<name>` oracle function in the test file that's a verbatim copy of the old code, then parametrize-diff against it. Example: `tests/tools/test_code_execution_windows_env.py::TestPosixEquivalence`. This locks in the invariant that POSIX behavior is bit-for-bit identical and makes any future drift fail loudly with a clear diff.

### Commit Conventions

```
type: concise subject line

Optional body.
```

Types: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`

### Key Rules

- **Never break prompt caching** — don't change context, tools, or system prompt mid-conversation
- **Message role alternation** — never two assistant or two user messages in a row
- Use `get_hermes_home()` from `hermes_constants` for all paths (profile-safe)
- Config values go in `config.yaml`, secrets go in `.env`
- New tools need a `check_fn` so they only appear when requirements are met
