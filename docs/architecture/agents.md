# Agents

## Agent Model

Agents are specialized analyzers that return structured outputs with evidence and confidence. The orchestrator coordinates execution and merges results.

## Core Agents

1. **Skill Match Agent**
   - Maps required/preferred job skills to resume evidence.
   - Output: matched skills, missing skills, inferred proficiency.

2. **Experience Relevance Agent**
   - Evaluates role history against job responsibilities and seniority.
   - Output: relevant experiences, weak matches, timeline concerns.

3. **Impact Agent**
   - Assesses quantified achievements and business impact signals.
   - Output: high-impact bullets, low-signal bullets, rewrite suggestions.

4. **Gap & Risk Agent**
   - Identifies substantive gaps and potential hiring risks.
   - Output: gap list, severity, mitigation recommendations.

5. **Recommendation Agent**
   - Produces ordered, practical improvements with expected impact.
   - Output: prioritized action plan with rationale.

## Common Output Contract

Each agent should return:

- `agent_name`
- `findings[]` (structured items)
- `confidence` (0-1)
- `evidence[]` (text snippets or extracted facts)
- `warnings[]` (if degraded/uncertain)

## Agent Quality Guidelines

- Do not fabricate resume facts not present in input.
- Prefer evidence-backed claims over speculative assertions.
- Keep recommendations actionable and specific.

# Agents

This document lists the **7 core agents** in the Job Fit & Application Strategy system.  
Each agent has a **single, focused responsibility** and returns **structured JSON outputs**.

---

## Agent Overview (One Line per Agent)

| # | Agent Name | Core Responsibility | Input | Output |
|---|---|---|---|---|
| 1 | JD Analysis Agent | Parse the job description into explicit requirements and role signals | Job description | Structured JD signals (skills, responsibilities, seniority) |
| 2 | Resume Profiling Agent | Convert the resume into a structured candidate capability profile | Resume | Candidate profile (skills, experience, projects, domain) |
| 3 | Hard Match Agent | Compute objective fit between resume and JD | JD signals + candidate profile | Match score, strengths, critical gaps |
| 4 | Hidden Signal Agent | Infer implicit expectations not explicitly stated in the JD | Job description | Hidden risk signals (ownership, ambiguity, true seniority) |
| 5 | Application Strategy Agent | Decide whether to apply and generate resume change suggestions | Match results + hidden signals | Apply / Edge Apply / No Apply + rationale + resume suggestions |
| 6 | Evidence / Citation Agent | Attach supporting JD and resume evidence to each conclusion | All agent outputs + source texts | Claim-to-evidence mappings |
| 7 | Orchestrator Agent | Control workflow, resolve conflicts, and produce final output | All agent outputs | Canonical JSON + human-readable report |

---

## Design Notes

- Each agent operates independently with a **clear input/output contract**.
- Agents do **not** rewrite full resumes; they provide **decision support and guidance**.
- The Orchestrator is responsible for **rule execution, conflict resolution, and schema enforcement**.
