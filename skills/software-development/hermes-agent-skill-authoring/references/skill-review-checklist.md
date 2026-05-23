# Skill Review Checklist

Use this when reviewing an existing `SKILL.md` or an imported skill/playbook before adopting it into the library.

## Fast measurements

- Count lines and characters; if the body is approaching a long article, recommend a skill bundle: short `SKILL.md` plus `references/`, `templates/`, and `scripts/`.
- Parse YAML frontmatter and check required fields: `name`, `description`.
- Check `description` length (`<=1024` enforced; target 150-250 chars for retrieval quality) and whether it describes trigger conditions rather than the procedure.
- Count code fences and large embedded scripts; production-like scripts should either be complete or clearly labeled as skeleton/pseudocode.

## Consistency checks

- Compare the document's stated rules against itself. Example: if it says SKILL.md bodies should be <=500 lines or concise, flag any self-violation.
- Separate portable/core spec from local or vendor-specific extensions. Do not present local fields such as `verified_at` or `covers` as universal requirements unless the runtime actually enforces them.
- Identify whether the artifact is an executable runtime skill, a long-form article, a workshop script, or a reference pack. If it tries to be all of these, split it.

## Source and claim hygiene

- Extract URLs and run a liveness check when tools are available; classify failures as dead, blocked/403, timeout, or intentional sample links.
- Mark empirical claims by evidence tier: canonical/spec, single-source measurement, practitioner report, internal observation, or hypothesis to test locally.
- Reduce absolute language around benchmark or marketplace claims unless the source is verified and reproducible.

## Recommended remediation shape

For oversized or research-heavy skills, prefer:

```text
<skill-name>/
├── SKILL.md                    # concise router/procedure
├── references/research.md      # evidence, citations, long explanations
├── references/safety.md        # policies and threat model if relevant
├── templates/<artifact>.md     # copy-modify starter artifacts
└── scripts/<probe>.py|sh       # complete deterministic probes/checks
```

## Review output

Return:

1. Verdict: publishable article vs executable skill vs needs split.
2. Top strengths.
3. Blocking issues.
4. Concrete first edits.
5. Source/link check summary if performed.
