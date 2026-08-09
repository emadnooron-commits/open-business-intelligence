# Open Business Intelligence Skills — Phase 1 Foundation

Model-agnostic, open-source AI skills that turn a raw business idea into a
structured business report. Phase 1 "Foundation" is now complete:

1. **Skill Contract** — `schemas/skill-contract.schema.json`
2. **idea-analysis** skill — `skills/idea-analysis/`
3. **market-research** skill — `skills/market-research/`
4. **competitor-analysis** skill — `skills/competitor-analysis/`
5. **Simple rule-based orchestrator** — `orchestrator/router.md`

## How the pieces fit together

Note the sequencing: competitor-analysis runs *after* market-research, not
in parallel, because it needs market-research's `opportunities` to check
which ones are already contested by an existing competitor.

## Try it end-to-end (manual walkthrough)

1. Feed `skills/idea-analysis/examples/project-noor.json` (`input`) to the
   idea-analysis SKILL.md instructions with an LLM — compare against
   `expected_output_shape`.
2. Take that output and apply the mapping in
   `skills/market-research/examples/project-noor-mapped-input.json` to
   build market-research's input; run it with research access.
3. Map `idea-analysis.idea_summary`/`value_proposition` and
   `market-research.output.opportunities` into competitor-analysis's input
   per `skills/competitor-analysis/SKILL.md`; run it.
4. Validate all three outputs against their `schema.json` before treating
   them as artifacts.

This proves the Skill Contract holds across three skills with different
`provider_requirements` (research-free vs. research-required), and that
the orchestrator's field-mapping rule scales beyond one hop.

## Next
- `feasibility-study` (Phase 3) — natural next call for Project Noor,
  since idea-analysis already flagged land/equipment/funding as
  feasibility-tagged assumptions
- Validate/retry logic from orchestrator/router.md rule 5, implemented in
  code rather than described in prose
- Repo scaffolding: LICENSE, CONTRIBUTING.md, SECURITY.md, skill template
  generator (Phase 6 in the original roadmap)
