# Zoom browser capture verification notes

Lessons from an ad-hoc Zoom web attendance session where joining succeeded but transcription did not.

## What went wrong

- The agent joined the Zoom web meeting and correctly detected participant count / in-meeting UI, but did not verify a real transcription source early enough.
- A scheduled monitor reported that the meeting started, but the scheduled run had its own fresh browser context and was only useful for status pings. It did not preserve the original joined meeting or provide audio capture.
- The browser Zoom UI exposed participant/video state but no captions, chat content, or transcript text. Visual observation alone was not enough for meeting notes.
- `ffmpeg`/Whisper availability is insufficient unless an actual system/browser audio input is available and recording has started.

## Future runbook

1. Split state explicitly:
   - joined/waiting;
   - in meeting;
   - capture source verified;
   - transcript/notes flowing.
2. If the meeting starts and no captions/chat/audio recording is verified within a few minutes, send a blunt status: “I’m in, but nothing is being recorded/transcribed yet.”
3. Use cron only for start/status notifications. Keep a live main-session process or a deterministic recording process for actual capture.
4. Prefer one of these before promising rolling transcript chunks:
   - provider captions/live transcript visible in DOM or screenshot;
   - cloud/local recording enabled and retrievable;
   - native app or OS-level loopback audio capture confirmed by a short test recording;
   - user-supplied recording after the meeting.
5. If only visual observation is available, label output as visual-only and summarize only visible screens/chat/speaker names, not spoken content.
