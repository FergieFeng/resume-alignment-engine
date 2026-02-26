# Orchestrator Agent

This document describes the role and responsibilities of the **Orchestrator Agent** in the  
**7-Agent Job Fit & Application Strategy System**.

The Orchestrator is the **control and decision layer** of the system.  
Even though the final output structure is fixed, the Orchestrator is required to manage  
*how* that output is produced.

---

## Why an Orchestrator Is Needed

A fixed output schema defines **what the final result looks like**, but it does not define:

- which agents should run,  
- in what order they should run,  
- how to resolve conflicting conclusions,  
- how to apply decision rules consistently.

Without an Orchestrator, the system would be a collection of independent agent outputs  
rather than a coherent decision-making system.

---

## Core Responsibilities

The Orchestrator performs five key functions:

### 1. Workflow Control
- Determines the execution order of agents.  
- Handles optional steps (e.g., Hidden Signal Agent, Evidence Agent).  
- Skips unnecessary steps based on user preferences or early-stop conditions.

### 2. Context Management
- Builds a shared request context from user inputs.  
- Passes only relevant, normalized data to each agent.  
- Ensures consistency across agent calls.

### 3. Decision Arbitration
- Resolves conflicts between agent outputs.  
- Applies conservative logic when signals disagree.  
- Example:  
  - High match score + high hidden risk → downgrade from **Apply** to **Edge Apply**.

### 4. Business Rule Execution
- Enforces system-level rules, such as:  
  - match score thresholds  
  - risk-based downgrades  
  - when resume suggestions should be generated  
- These rules are centralized in the Orchestrator, not embedded in sub-agents.

### 5. Output Schema Enforcement
- Validates that the final output conforms to the canonical schema.  
- Fills default values if optional agents are skipped.  
- Guarantees consistent, evaluable outputs.

---

## Orchestrator Workflow

1. Receive structured outputs from sub-agents.  
2. Evaluate decision rules and risk signals.  
3. Resolve inconsistencies or ambiguities.  
4. Assemble the canonical JSON output.  
5. Generate the human-readable report.

---

## Inputs and Outputs

### Inputs
- Structured JSON outputs from all executed sub-agents.  
- User preferences (e.g., decision-only vs decision + suggestions).

### Outputs
- **Canonical JSON output** (used for evaluation and comparison).  
- **Human-readable report** (used by end users).

---

## Design Principles

- **Separation of concerns:** sub-agents analyze; the Orchestrator decides.  
- **Deterministic structure:** output format is fixed.  
- **Flexible logic:** execution paths adapt to the case.  
- **Explainability:** decisions are traceable and evidence-backed.

---

## Scope Notes

- The Orchestrator does not perform analysis itself.  
- It does not rewrite resumes or generate new content directly.  
- Its role is to **coordinate, decide, and finalize** the system output.

---

## Summary

The Orchestrator Agent transforms multiple independent analyses into a single,  
consistent, and explainable decision. It is the component that makes the  
multi-agent system behave like a unified decision-support engine rather than  
a set of disconnected LLM calls.
