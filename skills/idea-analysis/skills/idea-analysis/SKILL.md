# Skill: idea-analysis

## Purpose
Take a raw, often messy business idea and turn it into a structured first-pass
analysis that every downstream skill (market-research, feasibility-study,
business-model, ...) can consume without re-asking the user basic questions.

This skill does **not** do market research, financial modeling, or
competitor analysis. It only clarifies and structures. Anything it can't
determine from the input becomes an `open_question` or a `low`-confidence
`assumption` — never a guess presented as fact.

## Input
See `schema.json#/input`. Only `idea` is required. Everything else improves
output quality but the skill must degrade gracefully without it.

## Instructions (for the LLM Provider)

1. Read the idea text. Identify:
   - The core problem being solved (not the solution — the problem).
   - The proposed solution / product / service.
   - Who it's for (if not stated, infer candidate segments and mark them
     as assumptions with `confidence: "low"`).

2. Write a 2-4 sentence `idea_summary` in plain language, no jargon.

3. Write a one-sentence `value_proposition`: "For [segment], [product] does
   [benefit], unlike [alternative]." Adapt the template naturally.

4. List `assumptions`: anything the idea depends on that hasn't been proven.
   Examples: available raw material supply, a regulatory approval, a price
   point the market will accept. For each, set a `confidence` and, where
   sensible, a `needs_validation_by` pointing at the skill id that should
   check it (e.g. `market-research`, `feasibility-study`, `risk-analysis`).

5. List `open_questions`: things the orchestrator should ask the user
   directly, because no skill can safely assume them (e.g. "is funding
   already secured?"). Keep this list short — 5 items max. Prioritize
   questions that would change which skills should run next.

6. `risks_preview`: 2-5 risks visible from the idea alone (not a full
   risk-analysis — that's a separate skill). Flag, don't analyze.

7. `recommended_next_skills`: an ordered list of skill ids. Default
   ordering for a from-scratch physical-product idea is typically
   `["market-research", "competitor-analysis", "feasibility-study"]`, but
   adjust based on what the idea actually needs. If the user asked a
   narrow question (e.g. "just tell me if this is a good idea"), still
   populate this field — the orchestrator decides whether to act on it.

## Output
See `schema.json#/output`. Must be valid JSON matching the schema exactly —
no extra prose outside the JSON when called by the orchestrator.

## Artifacts produced
- `data.json` — the raw schema-conformant output above.
- `report.md` — the same content rendered as readable Markdown for a human
  (headers: Summary, Value Proposition, Assumptions, Open Questions, Risks,
  Suggested Next Steps).
- `sources.json` — empty array `[]` for this skill (it does no external
  research); kept for artifact-shape consistency across all skills.

## Failure modes to avoid
- Do not invent market size, competitor names, or financial figures — that
  is not this skill's job and produces false confidence downstream.
- Do not silently drop a required input field; if `idea` is missing, return
  a schema violation, not a best-guess idea.
