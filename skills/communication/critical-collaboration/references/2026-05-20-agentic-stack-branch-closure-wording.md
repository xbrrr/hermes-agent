# Agentic Stack topic-closure wording and DoD nuance — 2026-05-20

Session learning from Mikhail's correction during MM+Bud/Subconscious rollout discussion.

## Correction

When Mikhail says to close a `branch/ветка` in this context, do not assume the underlying subject workstream is being stopped.

Specific case:

- Close: temporary `MM + Bud` coordination/control-room branch/thread.
- Continue: `Subconscious` topic/workstream and local subconscious usage.
- Rollout state: `subconscious-preflight` accepted only at `dry-run`; live/canary still require a separate explicit decision.

## Better phrasing

Use:

```text
Закрываем временную MM+Bud координацию по этому rollout.
Subconscious остаётся активным направлением.
Live/canary — только отдельным решением.
```

Avoid:

```text
Эта ветка закрыта.
```

because it is ambiguous: it can sound like closing the code branch, the Telegram topic, or the whole Subconscious direction.

## If asked “can I delete MM+Bud?”

Answer by layers, not with a blanket yes:

1. Stop using as working topic/control-room: yes, if smoke/migration branch is done.
2. Physical delete/archive: only after source-of-truth cleanup and preserving needed history/links.
3. Source of truth: check whether `chats.yaml` still says `deprecation_pending` or already `retired/archived`.
4. Runtime/enforcement: distinguish `documented_only` policy from hard routing enforcement.
5. DoD: do not claim fully achieved if DoD checks are not green.

## Manager-style answer pattern

```text
Коротко: как рабочий топик — можно закрывать. Как полностью завершённую миграцию — ещё нет.

Что уже применено:
- ...

Что не закрыто:
- ...

Практический следующий шаг:
- ...
```
