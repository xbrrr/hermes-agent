# Anthropic Credential Pool Diagnostics

Use this when reporting Anthropic OAuth vs API key usage status or debugging which credential path is active.

## Credential Pool Structure (Current Schema)

The `~/.hermes/auth.json` credential pool uses these fields for Anthropic credentials (as of May 2026):

```json
{
  "credential_pool": {
    "anthropic": [
      {
        "label": "claude-vps",
        "auth_type": "oauth",              // NOT "type" — "auth_type" is authoritative
        "source": "manual:hermes_pkce",
        "access_token": "sk-ant-oat...",   // OAuth session token
        "refresh_token": "...",
        "expires_at_ms": 1234567890,
        "base_url": "https://api.anthropic.com",
        "request_count": 42,               // NOT "usage_count" — "request_count" is authoritative
        "last_status": 200,
        "last_status_at": "2026-05-22T10:30:00Z",
        "last_error_code": null,
        "last_error_message": null,
        "priority": 1
      },
      {
        "label": "ANTHROPIC_API_KEY",
        "auth_type": "api_key",
        "source": "env:ANTHROPIC_API_KEY",
        "access_token": "sk-ant-api...",   // Console API key
        "base_url": "https://api.anthropic.com",
        "request_count": 0,
        "last_status": null,
        "priority": 2
      }
    ]
  }
}
```

## Common Diagnostic Mistakes

### ❌ WRONG: Looking at `type` field
```python
cred.get('type')  # Often returns None; not the right field
```

### ✅ CORRECT: Use `auth_type`
```python
cred.get('auth_type')  # 'oauth' | 'api_key'
```

### ❌ WRONG: Checking `usage_count`
```python
cred.get('usage_count')  # Legacy field, not updated in real-time
```

### ✅ CORRECT: Use `request_count`
```python
cred.get('request_count', 0)  # Incremented per API call
```

### ❌ WRONG: Looking for `session_token`
OAuth credentials store the token in `access_token`, not `session_token`.

### ✅ CORRECT: Check `access_token` prefix
```python
tok = cred.get('access_token', '')
is_oauth = tok.startswith('sk-ant-oat')  # OAuth
is_api_key = tok.startswith('sk-ant-api')  # Console API key
```

## Reliable Diagnostic Script

```python
from pathlib import Path
import json

auth_path = Path('~/.hermes/auth.json').expanduser()
auth_data = json.loads(auth_path.read_text())
pool = auth_data.get('credential_pool', {}).get('anthropic', [])

for i, cred in enumerate(pool, 1):
    label = cred.get('label')
    auth_type = cred.get('auth_type')  # NOT 'type'
    source = cred.get('source')
    request_count = cred.get('request_count', 0)  # NOT 'usage_count'
    
    has_access = bool(cred.get('access_token'))
    has_refresh = bool(cred.get('refresh_token'))
    
    print(f"#{i}: {label}")
    print(f"  auth_type: {auth_type}")
    print(f"  source: {source}")
    print(f"  request_count: {request_count}")
    print(f"  has_access_token: {has_access}")
    print(f"  has_refresh_token: {has_refresh}")
    
    if has_access:
        tok = cred['access_token']
        prefix = tok[:10]
        print(f"  access_token_prefix: {prefix}... (length={len(tok)})")
    
    if cred.get('last_error_code'):
        print(f"  last_error: {cred['last_error_code']} - {cred.get('last_error_message', '')[:80]}")
    
    print()
```

## Determining Active Credential Path

### Method 1: Check `request_count`
The credential with non-zero `request_count` is actively used. Note: may lag behind real-time by a few calls during high-frequency usage.

### Method 2: Check recent errors
If one credential shows `last_error_code: 400` with message `"Third-party apps now draw from your extra usage..."`, that was an OAuth credential that hit subscription limits. The pool may have rotated to the API key after that.

### Method 3: Live API call inspection
Set `HERMES_DEBUG=1` or check `~/.hermes/logs/agent.log` for credential selection logs:
```
INFO agent.credential_pool: selected credential anthropic #1 (claude-vps, priority=1)
```

## OAuth vs API Key: Billing Implications

| Credential | Prefix | Billing |
|------------|--------|---------|
| OAuth (`auth_type: oauth`) | `sk-ant-oat...` | **Claude Pro/Max subscription** (subject to third-party extra-usage limits) |
| API Key (`auth_type: api_key`) | `sk-ant-api...` | **Anthropic Console API credits** (token-metered billing) |

### Third-Party OAuth Limitation
As of May 2026, Anthropic blocks third-party inference (Hermes, Claude Code) through subscription OAuth unless **"extra usage"** is enabled at `claude.ai/settings/usage`. The error:
```
Third-party apps now draw from your extra usage, not your plan limits.
Add more at claude.ai/settings/usage and keep going.
```

If the user says they have **no extra usage toggle** visible in settings, it's an account/plan/region gating issue. The credential pool will rotate to the Console API key as fallback.

## Reporting Template

When the user asks "is this using OAuth or API key?":

```markdown
## Anthropic Credential Status

**Pool:**
- #1: `claude-vps` (OAuth) — request_count: X, access_token: sk-ant-oat...
- #2: `ANTHROPIC_API_KEY` (API key) — request_count: Y, access_token: sk-ant-api...

**Active path:** [infer from request_count, or say "inconclusive — both show 0 requests"]

**Billing:**
- If OAuth active → Claude Pro/Max subscription (third-party usage, subject to extra-usage limits)
- If API key active → Anthropic Console API credits (token-metered)

**Recent errors:** [show last_error_code/message if present]

**Logs:** [grep for credential selection or 'Third-party apps' error]
```

## See Also
- `references/claude-auth-provider-triage.md` — choosing between Anthropic OAuth, Console API, and OpenRouter
- `references/claude-oauth-usage-credits-rate-limits.md` — extra usage credits and rate limits for OAuth
