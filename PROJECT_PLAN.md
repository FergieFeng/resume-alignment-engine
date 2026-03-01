# PetCare Triage & Smart Booking Agent -- Project Plan

**Author:** Syed Ali Turab
**Date:** March 1, 2026

## Overview

This project plan outlines the development of the PetCare Triage & Smart Booking Agent, a multi-agent POC for the MMAI 2026 Capstone. The system automates pet symptom intake, triage urgency classification, appointment routing, and provides safe owner guidance through an orchestrator-coordinated sub-agent architecture.

---

## Phase 0: Foundation & Architecture (Week 1)

**Goal:** Establish project scaffolding, finalize architecture, and align on design decisions.

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Clone repo and create `PetCare` branch | -- | Done | Branch created from `main` |
| Adapt architecture docs from main branch to PetCare domain | -- | Done | 7 sub-agents + orchestrator |
| Finalize Agent Design Canvas | -- | Done | Submitted as deliverable |
| Define I/O contracts for all sub-agents | -- | In Progress | JSON schemas |
| Create synthetic test data (pet scenarios) | -- | Not Started | 15-20 cases covering common + urgent |
| Set up .env, requirements, project structure | -- | Done | Flask + OpenAI/Anthropic |

### Deliverables
- [x] Repository with PetCare branch
- [x] Architecture documentation (adapted)
- [x] Agent Design Canvas (completed)
- [ ] I/O contracts for all 7 sub-agents
- [ ] Synthetic test dataset (v1)

---

## Phase 1: Core Agent Development (Weeks 2-3)

**Goal:** Implement the critical-path agents that form the minimum viable intake flow.

### Sprint 1 (Week 2): Intake + Safety + Triage

| Task | Owner | Status | Priority |
|------|-------|--------|----------|
| Implement Intake Agent (Sub-Agent A) | -- | Not Started | P0 |
| Implement Safety Gate Agent (Sub-Agent B) | -- | Not Started | P0 |
| Implement Triage Agent (Sub-Agent D) | -- | Not Started | P0 |
| Create clinic rules knowledge base (`clinic_rules.json`) | -- | Not Started | P0 |
| Create red flags reference (`red_flags.json`) | -- | Not Started | P0 |
| Unit test each agent with fixture data | -- | Not Started | P0 |

### Sprint 2 (Week 3): Routing + Scheduling + Confidence

| Task | Owner | Status | Priority |
|------|-------|--------|----------|
| Implement Confidence Gate Agent (Sub-Agent C) | -- | Not Started | P0 |
| Implement Routing Agent (Sub-Agent E) | -- | Not Started | P0 |
| Implement Scheduling Agent (Sub-Agent F) | -- | Not Started | P1 |
| Create mock schedule data (`available_slots.json`) | -- | Not Started | P1 |
| Integration test: Intake → Safety → Triage → Routing | -- | Not Started | P0 |

### Deliverables
- [ ] 6 working sub-agents (A through F)
- [ ] Clinic rules + red flags knowledge base
- [ ] Mock scheduling data
- [ ] Unit tests passing for each agent

---

## Phase 2: Orchestration & Summary (Week 4)

**Goal:** Wire all agents together through the orchestrator and add the guidance/summary agent.

| Task | Owner | Status | Priority |
|------|-------|--------|----------|
| Implement Guidance & Summary Agent (Sub-Agent G) | -- | Not Started | P0 |
| Implement Orchestrator Agent | -- | Not Started | P0 |
| Build Flask API server (`api_server.py`) | -- | Not Started | P0 |
| End-to-end flow: input → all agents → output | -- | Not Started | P0 |
| Error handling and graceful degradation | -- | Not Started | P1 |
| Session memory management across agents | -- | Not Started | P1 |

### Deliverables
- [ ] Orchestrator coordinating all 7 sub-agents
- [ ] API server serving end-to-end flow
- [ ] End-to-end tests passing

---

## Phase 3: Frontend & Integration (Week 5)

**Goal:** Build the user-facing chat interface and integrate with the backend.

| Task | Owner | Status | Priority |
|------|-------|--------|----------|
| Build chat UI (owner-facing intake flow) | -- | Not Started | P0 |
| Connect frontend to Flask API | -- | Not Started | P0 |
| Display triage result + guidance to owner | -- | Not Started | P0 |
| Display clinic-facing summary (vet view) | -- | Not Started | P1 |
| Add loading states, error handling in UI | -- | Not Started | P1 |
| Mobile-responsive design | -- | Not Started | P2 |

### Deliverables
- [ ] Working chat-based intake UI
- [ ] Integrated frontend ↔ backend
- [ ] Owner-facing and clinic-facing views

---

## Phase 3.5: Voice Integration (Week 5-6)

**Goal:** Add voice input/output for hands-free intake.

### Sprint: Voice Tiers

| Task | Owner | Status | Priority |
|------|-------|--------|----------|
| Implement Tier 1: Browser Web Speech API (STT + TTS) | -- | Not Started | P0 |
| Add mic button + TTS toggle to frontend | -- | Not Started | P0 |
| Implement Tier 2: OpenAI Whisper transcription endpoint | -- | Not Started | P1 |
| Implement Tier 2: OpenAI TTS synthesis endpoint | -- | Not Started | P1 |
| Test voice input across browsers (Chrome, Safari, Edge) | -- | Not Started | P1 |
| Evaluate Tier 3: OpenAI Realtime API feasibility | -- | Not Started | P2 |
| Prototype Tier 3: WebSocket real-time voice (stretch goal) | -- | Not Started | P2 |

### Deliverables
- [ ] Voice input working (Tier 1 at minimum)
- [ ] TTS response playback
- [ ] Voice works alongside text input (user can switch)
- [ ] Tier 2 endpoints functional (if OPENAI_API_KEY configured)

---

## Phase 4: Evaluation & Testing (Week 6)

**Goal:** Evaluate against success metrics using the synthetic test set.

| Task | Owner | Status | Priority |
|------|-------|--------|----------|
| Prepare final test set (20+ scenarios) | -- | Not Started | P0 |
| Evaluate triage tier agreement (target ≥ 80%) | -- | Not Started | P0 |
| Evaluate routing accuracy (target ≥ 80%) | -- | Not Started | P0 |
| Evaluate intake completeness (target ≥ 90%) | -- | Not Started | P0 |
| Document strong example + failure case | -- | Not Started | P0 |
| Measure latency per intake session | -- | Not Started | P1 |
| Receptionist time-savings estimation | -- | Not Started | P1 |

### Deliverables
- [ ] Evaluation results table
- [ ] At least 1 strong example documented
- [ ] At least 1 failure case documented with learnings
- [ ] Metrics summary for report

---

## Phase 5: Report, Video & Polish (Week 7)

**Goal:** Complete all assignment deliverables.

| Task | Owner | Status | Priority |
|------|-------|--------|----------|
| Write technical report (`technical_report.md`) | -- | Not Started | P0 |
| Record POC demo video (10-15 min) | -- | Not Started | P0 |
| Deploy to cloud (Render / Railway) | -- | Not Started | P1 |
| Docker containerization + start scripts | -- | Not Started | P1 |
| Final README polish | -- | Not Started | P1 |
| Code cleanup and documentation | -- | Not Started | P2 |

### Deliverables
- [ ] Technical report (complete)
- [ ] Demo video (10-15 minutes)
- [ ] Live deployment
- [ ] Final codebase on `PetCare` branch

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Under-triage (serious case labeled routine) | High | Medium | Conservative red-flag rules + mandatory escalation messaging |
| Over-triage (too many cases flagged urgent) | Medium | Medium | Calibrate thresholds using scenario tests; allow receptionist override |
| Bad routing (wrong appointment type) | Medium | Medium | Maintain clinic-owned routing map + version control |
| LLM hallucination in guidance | High | Low | Strict non-diagnostic language constraints; rule-based safety gate |
| API latency exceeds 15s target | Medium | Medium | Limit model calls via routing; cache clinic rules |
| Incomplete intake (owner abandons flow) | Medium | High | Keep intake concise; show progress; allow partial submission |

---

## Key Decisions Log

| Decision | Rationale | Date |
|----------|-----------|------|
| 7-sub-agent + orchestrator architecture | Matches canvas design; enables modular testing and clear safety boundaries | -- |
| Session-only memory (no persistent PII) | Privacy-by-design; no need for cross-session data in POC | -- |
| Synthetic data for all testing | No real PHI needed; enables rapid iteration and shareable test sets | -- |
| Flask backend + vanilla JS frontend | Lightweight, fast to develop, consistent with capstone project patterns | -- |
| Conservative triage defaults | Safety-first: when uncertain, escalate rather than under-triage | -- |

---

## Assignment Deliverables Checklist

- [ ] Completed Agent Design Canvas
- [ ] POC Demo Video (10-15 minutes)
  - [ ] Problem definition and value proposition
  - [ ] Live demo with realistic scenarios
  - [ ] Results and learning (strong example + failure)
- [ ] Report + Appendix
  - [ ] Executive summary
  - [ ] End-to-end description
  - [ ] Key results
  - [ ] Trade-offs discussion (latency vs accuracy, safety vs convenience)
  - [ ] Risk analysis and mitigation
  - [ ] Viability beyond POC
  - [ ] Technical appendix (screenshots, test sets, code, prompts)
