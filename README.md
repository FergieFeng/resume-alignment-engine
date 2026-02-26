# Resume Alignment Engine

The **Resume Alignment Engine** is a documentation-first, multi-agent decision-support system
designed to help job seekers decide **whether to apply** for a role and **how to strengthen
their application** in a structured and explainable way.

The system prioritizes **decision quality and transparency**, rather than automatic content generation.

---

## What Problem This Solves

Job seekers typically face three questions when reviewing a job posting:

1. Should I apply for this role?
2. What risks or expectations are not explicitly stated?
3. If I apply, what should I improve in my resume?

Most existing tools focus on keyword matching or full resume rewriting.  
This project instead focuses on **decision-first analysis**, backed by evidence and clear reasoning.

---

## System Overview

The system uses a **7-agent architecture** coordinated by a central **Orchestrator Agent**:

- Analyze job descriptions and resumes independently
- Compute objective fit and identify gaps
- Infer hidden role expectations (optional)
- Produce a clear application recommendation:
  **Apply / Edge Apply / No Apply**
- Generate actionable resume change suggestions (not full rewriting)

Each agent has a single responsibility and communicates via structured JSON outputs.

---

## Documentation Map

- `docs/architecture/system_overview.md` – overall architecture and design rationale  
- `docs/architecture/workflow_technical.md` – technical workflow with flowchart, optional steps, and I/O examples  
- `docs/architecture/workflow_non_technical.md` – non-technical workflow overview for general readers  
- `docs/architecture/agents.md` – one-line responsibilities and I/O contracts for all agents  
- `docs/architecture/orchestrator.md` – orchestration logic, rules, and decision ownership  
- `docs/architecture/output_schema.md` – canonical JSON output schema  
- `docs/architecture/scope_and_roles.md` – project scope, ownership, and collaboration model  
- `docs/agent_specs/` – per-agent assignable design work packages  
- `docs/current_version/` – preserved snapshot of the previous docs version  

---

## Core Design Principles

- **Decision-first design**: analysis supports decisions, not content generation
- **Explainability**: every conclusion is traceable to evidence
- **Modularity**: agents are independent and single-responsibility
- **Evaluability**: outputs follow a fixed, validated schema
- **Scoped automation**: resume suggestions, not automatic rewriting

---

## Outputs

The system produces two aligned outputs:

1. **Canonical JSON Output**  
   - Used for evaluation, comparison, and downstream processing

2. **Human-Readable Report**  
   - A presentation layer derived from the canonical JSON

See `docs/architecture/output_schema.md` for full details.

## Repository Structure

- `docs/architecture/`: active system-level design docs
- `docs/agent_specs/`: per-agent design folders for teammate assignment
- `docs/current_version/`: preserved pre-restructure docs
- `src/`: implementation space for code contributors

## Quick Local Test (JD Analysis)

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Fill `.env`:
   - set `OPENAI_API_KEY`
4. Run the test UI:
   - `streamlit run src/ui/app.py`
5. Paste a JD (or click **Load Sample JD**) and run analysis.

---

## Current Status

This repository contains **documentation-first scaffolding** for the system design.

No production implementation is included.

---

## Suggested Next Steps (Optional)

- Implement agent interfaces using an agent framework (e.g., Google ADK)
- Add schema validation and example output fixtures
- Extend the system with additional optional agents (e.g., industry-specific signals)

---

## Summary

This project demonstrates how a **multi-agent architecture with a central orchestrator**
can deliver structured, explainable, and actionable decision support for job applications,
while maintaining clear scope and academic rigor.
