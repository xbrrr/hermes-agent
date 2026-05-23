# Agentic Stack daily human digest pattern

Use when Mikhail asks to duplicate/summarize today's runs, Subconscious progress, health checks, analysis, refactoring, or nightly jobs in a human/manager-readable way.

## Trigger phrases

- “продублируй сегодняшние прогоны”
- “что было сделано”
- “хелс чеки, проработка, анализ, рефакторинг”
- “гуманитарно отвечай”
- “дай человеческий/управленческий отчёт”

## Evidence to gather

Prefer evidence over memory-only summaries:

1. Current time/date for the reporting window.
2. Cron job list and latest outputs for relevant jobs:
   - Subconscious reflection / morning report / completed-work digest.
   - Server-doctor nightly or weekly health checks.
   - TODO/reminder jobs only if directly relevant.
3. Current generated reports/views for the topic, for example Subconscious manager report, quality probes, current-state, next-actions, and decisions views.
4. Current smoke checks only if safe and non-mutating:
   - topic registry validation;
   - gateway/status overview;
   - board completed tasks for the relevant topic;
   - local structured memory status when the topic is Subconscious.
5. Session search for recent matching work if cron output refers to a prior interactive task.

Do not restart services or switch providers just to produce the digest.

## Human digest format

Keep it short and management-first. Avoid raw JSON, PID dumps, long paths, line numbers, and test logs unless the user asks.

Recommended sections:

1. **Итог** — one clear sentence.
2. **Что было сделано по Subconscious / topic** — product effect, not implementation dump.
3. **Health checks / Server-doctor** — green/yellow/red, what was checked, current risk.
4. **Проработка / анализ** — decisions clarified, boundaries fixed, what this prevents.
5. **Рефакторинг / код** — only meaningful changes and verification result.
6. **Что осталось слабым** — honest limitations and next decision/action.
7. **Управленческий вывод** — concise interpretation.

## Style rules for Mikhail

- Russian by default in Telegram Agentic Stack reports.
- Humanitarian/manager framing first; technical evidence only as support.
- Use topic names over numeric IDs unless the ID prevents ambiguity.
- Critical, not flattering: name weak spots and trade-offs.
- If a cron job was silent, say what that means: usually “ran, found nothing new, suppressed spam,” not “nothing happened.”

## Pitfalls

- Do not equate “cron output exists” with “live runtime accepted.” Separate prepared code, tested code, loaded runtime, and live behavior.
- Do not mix local Subconscious review with Hindsight benchmark unless the user asks for a comparison.
- Do not paste raw cron/job logs into Telegram; summarize the operational meaning.
- Do not report “all good” if live gateway was not restarted and code changes are therefore only prepared/tested, not loaded.
- If Mikhail says standard Subconscious reports were not seen, answer the visibility problem first: classify each job as local-only, silent, topic-only, DM-delivered, or failed. A successful topic delivery is not enough if the practical expectation was “I should personally notice this.” When safe, adjust user-facing standard reports to dual delivery to the relevant topic plus Mikhail DM; keep raw collector/reflection jobs local.
- For silent jobs, explain the product meaning in one sentence: “ran and found nothing new, so it suppressed spam.” Do not make the user infer liveness from absence.
