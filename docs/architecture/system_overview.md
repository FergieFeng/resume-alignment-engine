# System Overview

## Purpose

The PetCare Triage & Smart Booking Agent automates veterinary clinic intake by collecting pet symptoms, detecting emergencies, classifying urgency, routing to the correct appointment type, and producing structured handoff summaries for the clinical team -- all while providing safe, non-diagnostic guidance to pet owners.

## High-Level Architecture

1. **Input Layer**
   - Accepts owner free-text describing pet symptoms, species, and basic profile via web chat interface.

2. **Intake Layer (Sub-Agent A)**
   - Conducts adaptive, multi-turn symptom collection with species-specific follow-up questions.

3. **Safety Layer (Sub-Agent B)**
   - Rule-based red-flag detection; immediately escalates emergencies.

4. **Validation Layer (Sub-Agent C)**
   - Confidence gate: verifies required fields are captured and signals are coherent.

5. **Analysis Layer (Sub-Agents D + E)**
   - Triage Agent: classifies urgency tier (Emergency / Same-day / Soon / Routine).
   - Routing Agent: maps symptom category to appointment type and provider pool.

6. **Action Layer (Sub-Agent F)**
   - Scheduling Agent: proposes available slots or generates booking request.

7. **Output Layer (Sub-Agent G)**
   - Produces owner-facing guidance ("do/don't while waiting") and clinic-facing structured JSON summary.

8. **Orchestration Layer**
   - Coordinates execution order, manages session state, resolves conflicts, enforces safety rules.

## Design Characteristics

- **Safety-first:** red-flag detection runs before any routing or scheduling.
- **Composable:** each sub-agent can be swapped or improved independently.
- **Auditable:** every triage decision maps to symptom evidence.
- **Schema-driven:** outputs follow strict validation for clinic integration.
- **Provider-agnostic:** orchestration can call different LLM providers.

## Non-Goals (POC Phase)

- Providing medical diagnoses or prescriptions
- Integrating with real EMR/CRM systems
- Multi-clinic deployment
- User accounts or persistent profiles
- Payment processing

## Success Criteria

- Triage tier agreement with clinic staff ≥ 80%
- Routing accuracy ≥ 80%
- Intake completeness ≥ 90%
- Full intake flow completes in < 15 seconds (excluding interactive turns)
- Zero missed emergency red flags in test set
