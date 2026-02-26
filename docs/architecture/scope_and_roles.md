# Scope and Roles

This document defines the **collaboration model** for the **Resume Alignment Engine**.
It is designed for **team-based development**, where **each team member owns one sub-agent**
(design + prompt + optional code), and one person owns system integration.

---

## Collaboration Goal

- Split the system into **independent sub-agents** with clear **input/output contracts**.
- Enable teammates to work **in parallel** with minimal coordination overhead.
- Integrate through a single **Orchestrator** that enforces workflow rules and the canonical output schema.

---

## In Scope

- Designing each sub-agent’s **micro-workflow** (2–5 steps), prompt strategy, and edge cases
- Defining **input/output JSON** contracts per agent (schema-aligned)
- Implementing agent logic as:
  - **Prompt-only** (acceptable for POC), or
  - **Prompt + light code** (optional), e.g., scoring helpers, validators
- Adding **example fixtures** for each agent (sample input + sample output)
- Orchestrator integration and schema validation

---

## Out of Scope (for this phase)

- Full resume rewriting or end-to-end resume generation by default
- Production UI, user accounts, storage, authentication
- Automated job application submission
- Legal/HR/compliance advice or guarantees of outcomes

---

## Ownership Model (Who Owns What)

### Role: Orchestrator / Integrator (1 owner)
- Owns **execution order**, optional branching, and rule enforcement
- Resolves conflicts between agent outputs
- Enforces canonical schema and produces:
  - canonical JSON
  - human-readable report
- Owns integration tests and end-to-end demo run

### Role: Sub-Agent Owner (1 owner per agent)
Each sub-agent owner is responsible for:
- **Micro-workflow design** (2–5 steps)
- Prompt + reasoning constraints
- Input/Output contract
- Edge cases and failure behavior
- One example fixture (input + output)

---

## Sub-Agent Assignments (7-Agent Strong Plan)

| Agent # | Agent | Owner | Deliverables (Minimum) |
|---:|---|---|---|
| 1 | JD Analysis Agent | (assign name) | Micro-workflow + I/O JSON + 1 fixture |
| 2 | Resume Profiling Agent | (assign name) | Micro-workflow + I/O JSON + 1 fixture |
| 3 | Hard Match Agent | (assign name) | Scoring logic + I/O JSON + 1 fixture |
| 4 | Hidden Signal Agent *(optional but recommended)* | (assign name) | Risk rubric + I/O JSON + 1 fixture |
| 5 | Application Strategy Agent + Resume Suggestions | (assign name) | Decision rules + suggestion templates + I/O JSON + 1 fixture |
| 6 | Evidence / Citation Agent *(optional but recommended)* | (assign name) | Claim→evidence mapping rules + I/O JSON + 1 fixture |
| 7 | Orchestrator Agent | (assign integrator) | Flow control + conflict resolution + schema enforcement + E2E fixture |

> Notes:
> - If team size is smaller, merge #4 into #5 and/or #6 into #7.
> - Optional agents (#4, #6) can be skipped while still producing schema-valid output.

---

## Definition of Done (Per Sub-Agent)

A sub-agent is considered complete when:
- It produces **schema-aligned JSON** with required keys
- It handles missing/ambiguous inputs gracefully (returns warnings)
- It has at least **one fixture** that can be replayed
- It does not overreach into other agents’ responsibilities

---

## Working Agreement

- **Fixed schema, flexible logic:** schema remains stable; workflows can iterate
- **Single responsibility:** agents analyze; Orchestrator decides
- **Small iterations:** changes should be testable with fixtures

---

## Summary

This ownership model enables **parallel development** by assigning each teammate a sub-agent with clear deliverables, while keeping integration centralized in the Orchestrator. It reduces coordination cost and makes the multi-agent system easier to evaluate and demo.
