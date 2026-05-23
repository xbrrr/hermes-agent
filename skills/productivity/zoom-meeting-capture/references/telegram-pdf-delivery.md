# Telegram PDF delivery fallback for meeting summaries

When the final meeting summary is packaged as a PDF or document, do not assume a `MEDIA:/path/file.pdf` reply succeeded just because the file exists locally. Telegram delivery can fail or warn at the Hermes gateway layer.

## Verification

After sending a meeting-summary document, verify the platform message actually contains the attachment. If the gateway warns or the user reports no file, resend with Telegram Bot API directly.

## Direct Bot API fallback

Use the bot token from Hermes env and `sendDocument`:

```bash
set -a
source <(grep -v '^TELEGRAM_HOME_CHANNEL_NAME=' /Users/xbr/.hermes/.env)
set +a

curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument" \
  -F chat_id="<telegram_chat_id>" \
  -F document=@"/absolute/path/to/meeting-summary.pdf" \
  -F caption="Главное по встрече, PDF"
```

Parse the JSON response and require `ok: true`; record the returned `message_id` in the final status.

## Notes

- Keep the direct fallback as a delivery workaround, not the primary path.
- Do not hard-code a chat ID into the skill; use the active platform target when known, or list/resolve targets before sending to a different chat.
- For Telegram replies, mention that the PDF was sent as a separate document message and include the filename/size if available.
