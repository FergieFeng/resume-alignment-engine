# System Overview

## Purpose

The system evaluates how well a candidate's resume aligns with a target job description and outputs structured, explainable recommendations.

## High-Level Architecture

1. **Input Layer**
   - Accepts raw job description and resume text (or parsed structured input).
2. **Normalization Layer**
   - Cleans and standardizes text, sections, dates, and skill terminology.
3. **Analysis Layer (Specialist Agents)**
   - Skill matching
   - Experience relevance
   - Achievement impact
   - Gap detection
4. **Scoring Layer**
   - Applies weighted rubric to produce category and overall scores.
5. **Synthesis Layer**
   - Merges findings into a coherent narrative with recommendations.
6. **Output Layer**
   - Emits validated JSON per `output_schema.md`.

## Design Characteristics

- **Composable:** each analyzer can be swapped independently.
- **Auditable:** every score should map to supporting evidence.
- **Schema-driven:** outputs must pass strict validation.
- **Provider-agnostic:** orchestration can call different model providers.

## Non-Goals (Initial Phase)

- Resume writing UI
- ATS submission automation
- Persistent user profile management

## Success Criteria

- Stable output schema across runs
- Reproducible scoring for same inputs and config
- High recommendation usefulness (human-evaluated)
