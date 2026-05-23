# 2026-05-20 — Dry-run closure and no-escalation guardrail

Session pattern: Bud/OpenClaw work on `subconscious-preflight` reached a verified dry-run runtime state:

- code/config accepted;
- plugin loaded in runtime;
- dry-run logs observed in target scope;
- live mode explicitly remained off;
- unrelated PATH warning was separated as Server-doctor debt.

Durable lesson for agent coordination:

1. Treat rollout acceptance as layered, not binary: code, runtime-loaded, dry-run, live, production.
2. When the accepted layer is dry-run, say so and stop there.
3. Do not infer “enable live” from a successful dry-run, even if both agents agree the dry-run is good.
4. Close the branch after one factual acknowledgment. Avoid Hermes↔Bud ACK loops that add no new evidence.
5. Put unrelated operational warnings into the correct class-level bucket instead of expanding the current rollout.

Reusable Russian phrasing:

```text
Статус: dry-run accepted, live off.
Дальше не двигаем без отдельного явного решения на canary/live.
Побочный warning выносим отдельно как Server-doctor debt, не смешиваем с rollout.
```
