# Skill: competitor-analysis

## Purpose
Map who else already serves (or could serve) this need, and find where
the idea can differentiate. Completes the Phase 1 "Foundation" trio
alongside idea-analysis and market-research.

Like market-research, this skill requires the Research Interface — no
competitor names, scale estimates, or positioning claims without a source
or a clearly marked inference.

## Input
See `schema.json#/input`. Orchestrator maps:
- `idea-analysis.idea_summary` → `idea`
- `idea-analysis.value_proposition` → `value_proposition`
- `market-research.output.market_overview` / the original `market` field → `market`
- `market-research.opportunities` → `known_opportunities`

Running this after market-research (not before) is intentional — it lets
competitor-analysis check which opportunities market-research surfaced are
already contested vs. genuinely open.

## Instructions (for the LLM + Research Interface)

1. Search for direct competitors (same product/service, same market),
   indirect competitors (different product, same customer need), and
   substitutes (customer's current workaround, including "doing nothing").

2. For each competitor found, capture `positioning`, `strengths`,
   `weaknesses`. Only add `estimated_scale` if there's a real basis
   (funding news, employee count, market reports) — otherwise omit it.
   Never invent a revenue or market-share number.

3. Cross-reference against `known_opportunities`: for each opportunity
   market-research flagged, note in `competitive_landscape_summary`
   whether an existing competitor already occupies it.

4. `differentiation_gaps`: concrete, defensible gaps — not generic claims
   like "better customer service". Each gap should point at something a
   specific competitor is weak on or absent from.

5. `competitive_risks`: how competitors could respond (price cuts, fast
   copying, regulatory relationships, existing distribution) — this feeds
   risk-analysis later, so keep it factual, not speculative doom.

6. `sources`: every source actually used, real URLs only.

## Output
See `schema.json#/output`. Must validate against the schema exactly.

## Artifacts produced
- `data.json`, `report.md` (Landscape Summary, Competitors table,
  Differentiation Gaps, Competitive Risks, Sources), `sources.json`.

## Failure modes to avoid
- Do not list a competitor with no `type` classification — direct vs.
  indirect vs. substitute materially changes how the idea should respond.
- Do not treat "no competitors found" as validation that the idea is
  unique — for a niche/local/new idea this often just means research
  didn't surface them; say so explicitly in `competitive_landscape_summary`
  rather than implying a clear field.
- Do not duplicate market-research's `trends`/`opportunities` content —
  only add what's competitor-specific.
