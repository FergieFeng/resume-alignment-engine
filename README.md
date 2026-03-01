# PetCare Triage & Smart Booking Agent

**Created by:** Fergie Feng

An AI-powered veterinary triage and smart booking agent that automates pet symptom intake, urgency classification, appointment routing, and provides safe owner guidance -- built as part of the MMAI 2026 Capstone at Queen's University.

The system reduces front-desk workload and improves clinical routing by automating the end-to-end intake workflow: symptom collection, red-flag detection, triage urgency scoring, appointment booking support, and vet-facing structured summaries, while providing safe, non-diagnostic "do/don't" guidance for pet owners during wait time.

---

## Live Demo

The app is deployed and accessible online:

- **URL:** *(deployment URL -- to be added)*
- **Username:** `petcare`
- **Password:** Reach out to the MMAI Capstone team

> First load after inactivity may take ~30-60 seconds (free tier cold start). After that it's instant.

---

## Quick Start (Docker -- Recommended)

Requires only [Git](https://git-scm.com/) and [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### macOS / Linux

```bash
git clone https://github.com/FergieFeng/resume-alignment-engine.git
cd resume-alignment-engine
git checkout PetCare
./start.sh
```

### Windows (PowerShell)

```powershell
git clone https://github.com/FergieFeng/resume-alignment-engine.git
cd resume-alignment-engine
git checkout PetCare
powershell -ExecutionPolicy Bypass -File start.ps1
```

The script prompts for API keys on first run, pulls latest code, builds the Docker container, and starts the server.
Open [http://localhost:5002](http://localhost:5002) in your browser.

> After someone pushes changes, just run the same script again -- it pulls and rebuilds automatically. Keys are saved locally and never need to be re-entered.

---

## Quick Start (Local Python)

```bash
git clone https://github.com/FergieFeng/resume-alignment-engine.git
cd resume-alignment-engine
git checkout PetCare

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Start the server
cd backend
python api_server.py
```

Open [http://localhost:5002](http://localhost:5002) in your browser.

---

## Project Structure

```
├── frontend/                    # Frontend files
│   ├── index.html               # Main HTML (intake chat UI)
│   ├── js/
│   │   └── app.js               # Client-side logic
│   └── styles/
│       └── main.css             # Styles
├── backend/                     # Backend files
│   ├── api_server.py            # Flask API server
│   ├── orchestrator.py          # Orchestrator agent (coordinates sub-agents)
│   ├── agents/                  # Sub-agent implementations
│   │   ├── intake_agent.py      # Sub-Agent A: Adaptive symptom intake
│   │   ├── safety_gate_agent.py # Sub-Agent B: Red-flag detection
│   │   ├── confidence_gate.py   # Sub-Agent C: Field validation + confidence
│   │   ├── triage_agent.py      # Sub-Agent D: Urgency classification
│   │   ├── routing_agent.py     # Sub-Agent E: Symptom → appointment type
│   │   ├── scheduling_agent.py  # Sub-Agent F: Slot proposal / booking
│   │   └── guidance_summary.py  # Sub-Agent G: Owner guidance + vet summary
│   ├── data/                    # Clinic rules, mock schedules, red-flag lists
│   │   ├── clinic_rules.json
│   │   ├── available_slots.json
│   │   └── red_flags.json
│   └── logs/                    # Runtime logs
├── docs/                        # Documentation
│   ├── architecture/            # System-level design docs
│   ├── agent_specs/             # Per-agent design work packages
│   └── current_version/         # Preserved docs from main branch
├── src/                         # Original source (from main branch)
├── technical_report.md          # Technical report (assignment deliverable)
├── PROJECT_PLAN.md              # Project plan and timeline
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
└── .gitignore
```

---

## System Overview

The PetCare Agent uses a **7-sub-agent architecture** coordinated by a central **Orchestrator Agent**:

| # | Sub-Agent | Responsibility |
|---|-----------|---------------|
| A | **Intake Agent** | Collect pet profile + chief complaint + timeline; ask adaptive follow-ups by symptom area |
| B | **Safety Gate Agent** | Detect emergency red flags → immediate escalation messaging |
| C | **Confidence Gate Agent** | Verify required fields and confidence; route to clarification or receptionist review |
| D | **Triage Agent** | Assign urgency tier (Emergency / Same-day / Soon / Routine) with rationale + confidence |
| E | **Routing Agent** | Classify symptom category → appointment type / provider pool |
| F | **Scheduling Agent** | Propose available slots or generate booking request payload |
| G | **Guidance & Summary Agent** | Generate owner "do/don't" guidance + structured clinic-ready intake summary |

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/architecture/system_overview.md](docs/architecture/system_overview.md) | Overall architecture and design rationale |
| [docs/architecture/workflow_technical.md](docs/architecture/workflow_technical.md) | Technical workflow with flowchart, I/O contracts, and examples |
| [docs/architecture/workflow_non_technical.md](docs/architecture/workflow_non_technical.md) | Non-technical workflow overview for general readers |
| [docs/architecture/agents.md](docs/architecture/agents.md) | Agent responsibilities and I/O contracts |
| [docs/architecture/orchestrator.md](docs/architecture/orchestrator.md) | Orchestration logic, rules, and decision ownership |
| [docs/architecture/output_schema.md](docs/architecture/output_schema.md) | Canonical JSON output schema |
| [docs/architecture/scope_and_roles.md](docs/architecture/scope_and_roles.md) | Project scope, ownership, and collaboration model |
| [docs/agent_specs/](docs/agent_specs/) | Per-agent assignable design work packages |
| [PROJECT_PLAN.md](PROJECT_PLAN.md) | Sprint-by-sprint project plan |
| [technical_report.md](technical_report.md) | Technical report (assignment deliverable) |

---

## Core Design Principles

- **Decision-first design**: triage and routing support decisions, not diagnoses
- **Safety by default**: red-flag detection with mandatory escalation; never auto-diagnose
- **Explainability**: every triage decision is traceable to symptom evidence
- **Modularity**: agents are independent and single-responsibility
- **Evaluability**: outputs follow a fixed, validated schema
- **Privacy-by-design**: no long-term storage of owner PII; session-only memory

---

## Outputs

The system produces two aligned outputs per intake session:

1. **Owner-Facing Response**
   - Urgency level + what happens next + appointment confirmation/request + safe do/don't guidance

2. **Clinic-Facing Structured Summary** (JSON)
   - Pet profile, symptom timeline, triage tier + red flags, suggested category, confidence score, notes

See [docs/architecture/output_schema.md](docs/architecture/output_schema.md) for full details.

---

## Success Metrics (MVP)

| Metric | Target |
|--------|--------|
| Triage tier agreement with clinic staff | ≥ 80% |
| Routing accuracy (correct appointment type) | ≥ 80% |
| Intake completeness (required fields captured) | ≥ 90% |
| Receptionist intake time reduction | 30%+ |
| Re-booking / mis-booking reduction | 20%+ |

---

## Current Status

This branch contains the **PetCare Triage & Smart Booking Agent** project scaffolding, architecture documentation, and implementation stubs.

Active development is in progress on the `PetCare` branch.

---

## Summary

This project demonstrates how a **multi-agent architecture with a central orchestrator** can deliver structured, safe, and explainable decision support for veterinary intake triage and appointment booking, while maintaining clear scope and academic rigor.
