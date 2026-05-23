# Zoom browser notetaking runbook

Use for ad-hoc Zoom meetings when the user wants the agent to attend, monitor, transcribe, and summarize.

## Minimal prerequisites from user

- Zoom URL
- display name
- start time or “now”
- passcode if not embedded in URL
- permission expectation for recording/transcription if applicable

## Browser join pattern

1. Navigate to the Zoom join URL.
2. If Zoom tries native app first, dismiss the app prompt and click “Join from browser” / “Присоединиться в браузере”.
3. Choose “continue without microphone and camera” rather than requesting browser permissions.
4. Enter the display name.
5. Click Join.
6. If the screen says “Waiting for the host to start the meeting”, send a concise waiting status.

## If native Zoom install is attempted

- Homebrew cask install may require sudo/admin interaction.
- If it fails for lack of sudo, do not stall the meeting task. Fall back to browser and note briefly that browser join is working.

## Monitoring cadence

If the user asks to be notified when the meeting starts:
- create a short periodic monitor (for example every 3 minutes) when available;
- output only concise status while waiting;
- when started, report immediately and check whether captions/audio/chat are accessible.

Important: scheduled monitor jobs usually run in a fresh browser/session. Use them for start/waiting pings only; keep the actual meeting attendance and transcription state in a dedicated active browser/process. A monitor should report “started” only after seeing real in-meeting evidence such as participant count, Leave button, meeting toolbar, or participant/video tiles — not just a loading/pre-join transition.

Example waiting status:

```text
Zoom статус: встреча ещё не началась.
```

Example start status:

```text
Zoom статус: встреча началась. Проверяю, получается ли слушать/транскрибировать; следующий статус через несколько минут.
```

## Rolling output

Send chunks rather than one large end-only report when requested:

```text
Промежуточно:
- Статус: слушаю / captions есть / только чат / частично
- Главное: …
- Решения: …
- Action items: …
- Риски/вопросы: …
```

End with a compact final summary:
- outcome
- decisions
- action items with owners/deadlines
- risks/open questions
- transcript availability/coverage caveat

## Terms to explain simply

- Captions = live subtitles / transcript inside Zoom.
- Recording = saved meeting audio/video, locally or in Zoom cloud.

## Privacy and memory

Do not write the meeting URL, passcode, transcript, participant list, or meeting-specific facts into long-term memory or SKILL.md. If a durable workflow improvement emerges, update this runbook only with the generalized pattern.
