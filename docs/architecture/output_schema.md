# System Overview

This document provides a high-level overview of the **Job Fit & Application Strategy System**, a  
multi-agent decision-support system designed to help users evaluate job applications in a  
structured, explainable, and actionable way.

The system focuses on **decision quality**, not content generation.

---

## Problem Statement

Job seekers often struggle to answer three critical questions when reviewing a job posting:

1. Should I apply for this role?  
2. What are the hidden risks or expectations?  
3. If I apply, what should I improve in my resume?

Existing tools typically focus on keyword matching or full resume rewriting, which:  
- lack decision transparency,  
- ignore implicit role signals,  
- provide limited guidance on *why* a role may or may not be a good fit.

This system addresses these gaps using a **multi-agent architecture**.

---

## Design Goals

The system is designed around the following principles:

- **Decision-first**: prioritize clear recommendations over content generation.  
- **Explainability**: every decision is traceable to evidence.  
- **Modularity**: each agent has a single, focused responsibility.  
- **Evaluability**: outputs follow a fixed schema for comparison.  
- **Scoped complexity**: avoid unnecessary automation.

---

## System Architecture

The system consists of **seven specialized agents** coordinated by a central **Orchestrator Agent**.

### Agent Roles

- **JD Analysis Agent**: extracts explicit job requirements and role signals.  
- **Resume Profiling Agent**: builds a structured candidate capability profile.  
- **Hard Match Agent**: computes objective alignment between resume and job description.  
- **Hidden Signal Agent** *(optional)*: infers implicit expectations such as ownership and seniority.  
- **Application Strategy Agent**: determines whether to apply and generates resume improvement guidance.  
- **Evidence / Citation Agent** *(optional)*: links conclusions to source text.  
- **Orchestrator Agent**: controls execution, resolves conflicts, and produces the final output.

Each agent operates independently and communicates through structured JSON contracts.

---

## Orchestrator-Centric Design

The Orchestrator is the core of the system.

Even though the final output schema is fixed, the Orchestrator is responsible for:

- controlling execution order and optional branching,  
- resolving conflicting signals across agents,  
- applying global decision rules,  
- enforcing schema consistency.

This separation ensures that analytical logic remains modular while decision logic remains centralized.

---

## Workflow Summary

At a high level, the system workflow is:

1. Parse the job description.  
2. Profile the resume.  
3. Compute objective fit.  
4. *(Optional)* interpret hidden role signals.  
5. Generate application decision and resume suggestions.  
6. *(Optional)* attach supporting evidence.  
7. Assemble and return the final output.

Detailed step-by-step logic is described in `workflow_technical.md`.

---

## Technology Stack

- **Agent Framework**: Google Agent Development Kit (ADK)  
- **Language Models**: Large Language Models (LLMs)  
- **Data Contracts**: JSON schemas  
- **Control Logic**: Orchestrator-managed rules and thresholds

Google ADK is used to modularize agents and support orchestration logic, not as a single monolithic agent.

---

## Output Model

The system produces two aligned outputs:

- **Canonical JSON Output**  
  Used for evaluation, comparison, and downstream processing.

- **Human-Readable Report**  
  A presentation layer derived from the canonical JSON.

Both outputs conform to the schema defined in `output_schema.md`.

---

## Scope and Limitations

To maintain focus and feasibility:

- The system provides **resume change suggestions**, not full resume rewriting.  
- Decisions are advisory and do not guarantee interview outcomes.  
- Optional agents enhance explainability but are not required for core functionality.

---

## Summary

This system demonstrates how a **multi-agent architecture with a central orchestrator**  
can deliver transparent, structured, and actionable decision support for job applications.

By separating analysis, decision-making, and presentation, the design balances  
practical usefulness with academic rigor.
