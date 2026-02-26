# Agent Task Assignment (One Page)

This page is the single source of truth for assigning ownership and tracking progress for the 7-agent design workstream.

## How to Use

- Assign one folder to one teammate.
- Each teammate documents prompt/workflow/contracts in their assigned folder.
- Keep outputs schema-aligned and fixture-backed.

## Team Assignment Table

| Workstream | Folder | Owner | Backup | Status | Due Date |
|---|---|---|---|---|---|
| JD Analysis Agent | `docs/agent_specs/jd_analysis/` | (assign) | (assign) | Not Started | (date) |
| Resume Profiling Agent | `docs/agent_specs/resume_profiling/` | (assign) | (assign) | Not Started | (date) |
| Hard Match Agent | `docs/agent_specs/hard_match/` | (assign) | (assign) | Not Started | (date) |
| Hidden Signal Agent *(optional but recommended)* | `docs/agent_specs/hidden_signal/` | (assign) | (assign) | Not Started | (date) |
| Application Strategy Agent | `docs/agent_specs/application_strategy/` | (assign) | (assign) | Not Started | (date) |
| Evidence Citation Agent *(optional but recommended)* | `docs/agent_specs/evidence_citation/` | (assign) | (assign) | Not Started | (date) |
| Orchestrator Agent | `docs/agent_specs/orchestrator/` | (assign) | (assign) | Not Started | (date) |

## Agent Folders

- `jd_analysis`
- `resume_profiling`
- `hard_match`
- `hidden_signal`
- `application_strategy`
- `evidence_citation`
- `orchestrator`

## Required Deliverables (Per Agent Owner)

Each owner must complete all items in their assigned folder:

- `README.md` updated with owner name and scope
- `input_output_contract.md` with required and optional fields
- one strategy/rules doc:
  - `prompt_strategy.md`, or
  - `scoring_rules.md` / `risk_rubric.md` / `decision_rules.md` / `mapping_rules.md` / `orchestration_rules.md`
- `fixtures/sample_input.json`
- `fixtures/sample_output.json`

## Definition of Done (Per Agent)

- Output fields are compatible with `docs/architecture/output_schema.md`
- Ambiguous/missing-input behavior is documented
- At least one fixture pair can be replayed by another teammate
- No overlap with responsibilities owned by other agents

## Integration Owner Checklist (Orchestrator Owner)

- Confirm all agent contracts are mutually compatible
- Resolve schema mismatches before integration
- Document conflict-resolution rules in orchestrator spec
- Prepare one end-to-end fixture using all available agent outputs
