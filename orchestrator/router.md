# Orchestrator V1 — Rule-Based Router

V1 deliberately does **not** use an LLM to decide which skills to call.
A fixed routing table is easier to debug, test, and trust while the Skill
Contract itself is still stabilizing. LLM-based planning is a V2 upgrade
once idea-analysis and market-research have proven the contract works.

## Routing table (V1)

| User signal (keyword/intent) | Skills to run, in order |
|---|---|
| Full analysis requested ("حلل المشروع", "هل الفكرة قابلة للتنفيذ") | idea-analysis → market-research → competitor-analysis → feasibility-study → financial-analysis → risk-analysis → recommendation-engine → report-builder |
| Only mentions an idea, nothing else | idea-analysis |
| Explicitly asks for competitors only ("تحليل منافسين بس") | competitor-analysis |
| Explicitly asks for market only | market-research |
| Explicitly asks for feasibility/جدوى | feasibility-study (auto-runs idea-analysis first if no prior idea-analysis artifact exists) |

## Execution rules

1. **Always check the Artifact Store first.** If `idea-analysis/data.json`
   already exists for this project, do not re-run idea-analysis — reuse it,
   unless the user says the idea changed.
2. **Respect `recommended_next_skills`.** Each skill's output can suggest
   what to run next (see idea-analysis SKILL.md). The router treats this as
   a suggestion, not a command — the table above still decides what
   actually executes for V1.
3. **One skill's output is the next skill's input context**, not its
   literal `input_schema`. E.g. market-research's input schema expects
   `idea`, `market`, `country`, `target_customer` — the orchestrator maps
   those fields from idea-analysis's `idea_summary` / `target_segments`.
   Similarly, competitor-analysis maps `idea`/`value_proposition` from
   idea-analysis and `market`/`known_opportunities` from market-research —
   see `skills/competitor-analysis/SKILL.md` for the exact mapping. This is
   why competitor-analysis runs *after* market-research in the table above,
   not in parallel: it needs market-research's opportunities to check which
   ones are already contested.
4. **Stop and ask, don't guess.** If a skill's `open_questions` list
   contains something that changes which skills should run next (e.g.
   funding status changes whether financial-analysis is useful yet),
   surface it to the user before continuing — don't silently proceed.
5. **Validate before writing.** Before persisting `data.json`, validate it
   against the skill's own `output` schema. On failure, retry once with
   the schema validation errors appended to the prompt; on second failure,
   surface the raw error to the user instead of writing invalid artifacts.

## Artifact Store layout (filesystem, no DB in V1)
