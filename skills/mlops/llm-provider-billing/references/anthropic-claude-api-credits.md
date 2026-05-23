# Anthropic / Claude API Credits and Balance

Session-derived reference for answering Claude billing terminology questions. Keep exact policy claims grounded in current Anthropic/Claude docs before relying on them for decisions.

## Captured Sources

- Claude Help Center: `How do I pay for my Claude API usage?` (`support.claude.com/en/articles/8977456-how-do-i-pay-for-my-claude-api-usage`), observed 2026-05-22.
- Claude Help Center: `I have a paid Claude subscription (Pro, Max, Team, or Enterprise plans). Why do I have to pay separately to use the Claude API and Console?` (`support.claude.com/en/articles/9876003-...`), observed 2026-05-22.
- Claude API docs: `Rate limits` (`platform.claude.com/docs/en/api/rate-limits`), observed 2026-05-22.

## Durable Terminology

- **Usage credits**: prepaid credits purchased before using Claude API / Workbench. They are applied to usage according to current pricing.
- **API balance / available credit balance**: the organization's remaining available credits in Claude Console billing. It is the current remaining amount of the purchased/granted credits.
- **Auto-reload**: optional billing setting that buys more credits when balance falls below a configured threshold.
- **Paid Claude subscription**: Claude Pro/Max/Team/Enterprise web/chat product entitlement. Anthropic documents it as separate from Claude Console/API billing.
- **Spend limits**: maximum monthly API cost an organization can incur. This is a cap/limit layer, not the same thing as balance.
- **Rate limits**: throughput controls such as requests/tokens over time, tied to usage tiers and organization limits.

## User-Facing Explanation Shape

For a simple Russian Telegram question like “в чем отличие claude api баланса и usage credits”:

```text
Коротко: это почти одно и то же, но на разных уровнях.

- Usage credits — предоплаченные кредиты/деньги, которые покупаешь в Claude Console для API/Workbench/Claude Code usage.
- API balance — текущий остаток этих credits на организации.

Пример: купил $100 credits, потратил $17.43 → API balance $82.57.

Не путать:
- Claude Pro/Max/Team подписка ≠ API balance; API оплачивается отдельно.
- Credits ≠ rate limits/tier; credits — деньги, rate limits — пропускная способность.
```

## Policy Details to Re-check When Important

Anthropic support page observed in this session stated:

- Failed API requests are not charged; successful API calls and completed tasks are billed.
- If credits run out, API/Workbench use stops until credits are added.
- Purchased credits expire one year from purchase date, expiration cannot be extended, and purchases are non-refundable.

These are provider policy details, so re-check current docs before giving financial/legal advice.
