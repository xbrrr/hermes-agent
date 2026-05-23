---
name: llm-provider-billing
description: "Use when explaining or comparing LLM provider billing concepts: API balances, prepaid credits, subscriptions, rate/spend limits, usage tiers, invoices, and product-specific billing separation. Ground answers in provider docs and separate money balance from access/throughput limits."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm, billing, credits, api, pricing, providers]
    related_skills: [hermes-agent, serving-llms-vllm, huggingface-hub]
---

# LLM Provider Billing

## Overview

LLM providers often use overlapping terms for billing and access: credits, balance, spend limits, rate limits, usage tiers, subscriptions, invoices, and organization/workspace limits. This skill is for answering those questions without conflating money, entitlement, and throughput.

The core discipline: define each term at its layer, then explain how they interact in one example.

## When to Use

Use this skill when the user asks about:

- API balance vs credits / usage credits / prepaid credits
- Claude/OpenAI/Gemini/Mistral/etc. API billing vs chat subscriptions
- Spend limits vs rate limits vs usage tiers
- Why an API key stopped working despite a paid chat plan
- Whether credits expire, auto-reload, invoices, or workspace limits apply
- Comparing billing concepts across model providers or routers

Do **not** use this for deep cost modeling unless the user asks for numbers; then ground the prices with current provider docs before calculating.

## Quick Mental Model

Separate provider billing concepts into four layers:

1. **Money bucket** — prepaid credits, cash balance, grant credits, invoices, payment method.
2. **Metering** — token/request/task usage converted to cost according to the provider's price sheet.
3. **Access entitlement** — subscription plans, API enablement, organization/workspace permissions, product availability.
4. **Throughput control** — rate limits, spend limits, usage tiers, quota, RPM/TPM/concurrency.

Most user confusion comes from mixing layer 1 with layer 3 or 4.

## Answer Pattern

1. Start with the direct equivalence/difference in one sentence.
2. Give the layer definitions:
   - `balance` = remaining money/credits available now.
   - `credits` = purchased/granted billing units that fund usage.
   - `subscription` = product entitlement, often separate from API spend.
   - `rate limit/tier` = throughput allowance, not money.
3. Add a tiny numeric example if it clarifies.
4. Mention the operational consequence:
   - balance reaches zero → paid API calls stop or fail until reloaded;
   - rate limit reached → retry/backoff or request a limit increase;
   - subscription only → may not include API billing.
5. If provider-specific details matter, cite/check current docs.

## Mikhail / Telegram Style

When Mikhail asks in Russian or via Telegram, answer in Russian, concise, and manager-readable:

- Lead with the conclusion.
- Use bullets, not tables.
- Avoid long policy exposition unless asked.
- Use one concrete example instead of a broad taxonomy if the question is simple.

## Provider Notes

See `references/anthropic-claude-api-credits.md` for the Claude/Anthropic terminology captured from support/docs: usage credits, API balance, Claude paid plan separation, expiration, and spend/rate limits.

Add future provider quirks as small reference files rather than bloating this SKILL.md.

## Common Pitfalls

1. **Saying balance and credits are totally different products.** Usually balance is the remaining amount of credits/money; credits are what was purchased/granted.

2. **Conflating chat subscriptions with API billing.** A paid chat plan often improves the web/app experience but does not automatically fund API usage.

3. **Conflating credits with rate limits.** Credits pay for usage; rate limits throttle throughput. A user can have credits and still be rate-limited, or have high rate limits and no remaining balance.

4. **Treating provider docs as stable forever.** Billing language changes. For current pricing, expiration, refunds, and limits, verify with docs before giving exact policy claims.

5. **Over-answering simple term questions.** If the user asks “what is the difference between X and Y,” do not produce a billing treatise. Define, example, consequence, stop.

## Verification Checklist

- [ ] Defined terms at the right layer: money, metering, entitlement, throughput.
- [ ] Did not claim a chat subscription includes API credits unless docs confirm it.
- [ ] Did not present rate/spend limits as available balance.
- [ ] Exact prices/expiration/refund policies are grounded in current provider docs or labeled as provider-specific.
- [ ] Final answer is concise if the user's question is simple.
