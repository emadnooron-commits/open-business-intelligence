# Skill: market-research

## Purpose
Ground the idea in real-world market evidence: demand, trends,
opportunities, and risks — and explicitly test the assumptions
idea-analysis flagged as `needs_validation_by: market-research`.

Unlike idea-analysis, this skill **requires** the Research Interface
(`provider_requirements.research: true`). It must not fabricate market
size, demand figures, or trends without a source. If research access is
unavailable, it must say so in `market_overview` and return empty/omitted
figure fields rather than invented numbers.

## Input
See `schema.json#/input`. The orchestrator maps these from idea-analysis
output — see orchestrator/router.md rule 3. `assumptions_to_validate` is
optional but should be populated whenever idea-analysis flagged relevant
assumptions.

## Instructions (for the LLM + Research Interface)

1. Run research queries covering: market overview, demand signals, recent
   trends (last 1-2 years), and 2-4 concrete opportunities/risks. Prefer
   primary/official sources (industry reports, government data, trade
   associations) over aggregator blogs.

2. `market_overview`: 3-5 sentences, no invented specifics. If reliable
   sizing data isn't found, say so plainly rather than estimating silently.

3. `market_size`: only include this field if a sourced figure exists.
   Always attach `basis` (where it came from) and a `confidence` level.
   Omit the whole field rather than guess.

4. `demand` / `trends` / `opportunities` / `risks`: short, evidence-backed
   bullets. Each claim should be traceable to something in `sources`.

5. `assumption_findings`: for each item in `assumptions_to_validate`,
   research it specifically and return a verdict:
   - `supported` — evidence backs the assumption
   - `contradicted` — evidence conflicts with it (flag this loudly; it
     should visibly affect `recommended_next_skills` downstream)
   - `inconclusive` — no reliable evidence either way

6. `sources`: every source actually used, with a real, working URL. No
   source should appear here without also supporting at least one claim
   in the output above.

## Output
See `schema.json#/output`. Must validate against the schema exactly.

## Artifacts produced
- `data.json` — schema-conformant output.
- `report.md` — human-readable rendering (Overview, Market Size, Demand,
  Trends, Opportunities, Risks, Assumption Findings, Sources).
- `sources.json` — same array as `output.sources`, kept separately so
  other skills (e.g. report-builder) can dedupe/aggregate citations
  across all skills without re-parsing `data.json`.

## Failure modes to avoid
- Never invent a market size number to fill the schema — omit the field.
- Never present a contradicted assumption softly; it changes downstream
  decisions (e.g. financial-analysis, feasibility-study) and must be
  visible, not buried in a sub-field.
- Don't restate idea-analysis's content — only add what's new (market
  evidence), assuming the report-builder will merge both later.
