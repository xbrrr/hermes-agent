# Zoom web join reference

Session-derived notes for joining Zoom from a browser when the native Zoom app is unavailable or not worth installing.

## Useful sequence

1. Navigate to the `https://...zoom.us/j/...` meeting URL.
2. Dismiss cookie/privacy banners if they block controls.
3. If a native-app launch modal appears, close/dismiss it and choose the browser option.
4. If the page becomes an iframe shell, inspect/navigate to the iframe `src` directly. It may look like:
   - `https://app.zoom.us/wc/<meeting_id>/join?...&pwd=...`
5. When prompted for device access, choose the options equivalent to:
   - continue without microphone and camera;
   - or continue without microphone if a second dialog appears.
6. Enter the requested display name.
7. Join and verify whether the meeting is active, in waiting room, or waiting for host.

## Observed Russian Zoom labels

- `Присоединиться к конференции` — join meeting page.
- `Присоединиться в браузере` — join from browser.
- `Продолжить без микрофона и камеры` — continue without microphone and camera.
- `Продолжить без микрофона` — continue without microphone.
- `Ваше имя` — name input.
- `Войти` — join/enter.
- `Дождитесь, когда организатор начнет конференцию.` — wait for host to start the meeting.

## Installation pitfall

On macOS, `brew install --cask zoom` may fetch the package but fail at the installer step because `sudo` requires an interactive password. If the user allowed either app or browser and browser join works, proceed via browser instead of blocking on installation.

## Quality caveat

A successful browser join does not prove live transcription will work. Verify captions, recording, or audio capture separately before promising a complete transcript.
