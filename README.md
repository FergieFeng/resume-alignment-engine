# PetCare Triage & Smart Booking Agent

**Author:** Syed Ali Turab
**Date:** March 1, 2026

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

## Architecture Diagram

![PetCare Triage Workflow](docs/images/architecture_workflow.png)

The diagram above shows the full sub-agent workflow: Trigger → Intake (A) → Safety Gate (B) → Confidence Gate (C) → Triage (D) → Routing (E) → Scheduling (F) → Guidance & Summary (G), with branching for emergency escalation and clarification loops.

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

### What the Start Script Does

1. Checks if `.env` exists; if not, prompts for `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`
2. Pulls latest code from the `PetCare` branch
3. Builds the Docker image (`petcare-agent`)
4. Starts the container, mapping port `5002` and mounting `.env`
5. Opens http://localhost:5002

### Docker Manual Build

```bash
docker build -t petcare-agent .
docker run -p 5002:5002 --env-file .env petcare-agent
```

---

## Quick Start (Local Python)

Requires Python 3.10+ and pip.

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
# Edit .env and add your API keys (at minimum: OPENAI_API_KEY)

# Start the server
cd backend
python api_server.py
```

Open [http://localhost:5002](http://localhost:5002) in your browser.

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes (if using OpenAI) | OpenAI API key for GPT-4.1 |
| `ANTHROPIC_API_KEY` | Yes (if using Anthropic) | Anthropic API key for Claude |
| `DEFAULT_LLM_PROVIDER` | No | `openai` (default) or `anthropic` |
| `DEFAULT_LLM_MODEL` | No | Model name (default: `gpt-4.1-mini`) |
| `PORT` | No | Server port (default: `5002`) |
| `LOG_LEVEL` | No | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

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
├── Dockerfile                   # Docker containerization
├── start.sh                     # One-click start (macOS / Linux)
├── start.ps1                    # One-click start (Windows PowerShell)
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

## Data Sources

The PetCare agent draws triage knowledge, symptom data, and red-flag rules from the following sources:

### Symptom & Triage Knowledge

| Source | Type | Usage |
|--------|------|-------|
| [Hugging Face: pet-health-symptoms-dataset](https://huggingface.co/datasets/karenwky/pet-health-symptoms-dataset) | Open dataset (2,000 labeled samples) | Symptom classification training/validation -- covers skin irritations, digestive issues, parasites, ear infections, mobility problems |
| [Vet-AI Symptom Checker](https://www.vet-ai.com/symptomchecker) | Reference | Triage logic patterns -- 165 algorithms built by veterinarians, 4M+ questions processed |
| [SAVSNET / PetBERT](https://github.com/SAVSNET/PetBERT) | NLP model (500M+ words from 5.1M UK vet records) | Reference for veterinary NLP and disease coding patterns |

### Safety & Toxicology

| Source | Type | Usage |
|--------|------|-------|
| [ASPCA Animal Poison Control (AnTox)](https://www.aspcapro.org/antox) | Reference database (1M+ cases) | Red-flag rules for toxin ingestion -- top toxins, species-specific risks |
| [ASPCA Top Toxins 2024](https://www.aspcapro.org/resource/top-10-toxins-2024) | Published list | Prioritized toxin list for Safety Gate agent (OTC meds 16.5%, food/drink 16.1%, chocolate 13.6%, etc.) |
| Veterinary emergency textbooks | Clinical reference | Emergency red-flag definitions (GDV, urinary blockage, dyspnea, seizure, etc.) |

### Clinic Operations (Synthetic / Mock)

| Source | Type | Usage |
|--------|------|-------|
| `backend/data/clinic_rules.json` | Synthetic config | Triage rules, routing maps, provider specialties, species notes |
| `backend/data/red_flags.json` | Curated list (50+ entries) | Emergency red-flag triggers compiled from ASPCA + veterinary emergency guidelines |
| `backend/data/available_slots.json` | Mock data | Simulated clinic schedule for appointment booking POC |

### Data Strategy

- **POC phase:** All data is synthetic or publicly available. No real patient/pet health information (PHI) is used.
- **Future integration:** Clinic scheduling APIs, EMR/CRM systems, real-time appointment availability.
- **Privacy:** Session-only memory. No persistent storage of owner PII. Anonymized logs for evaluation only.

---

## Current Status

This branch contains the **PetCare Triage & Smart Booking Agent** project scaffolding, architecture documentation, and implementation stubs.

Active development is in progress on the `PetCare` branch.

---

## Summary

This project demonstrates how a **multi-agent architecture with a central orchestrator** can deliver structured, safe, and explainable decision support for veterinary intake triage and appointment booking, while maintaining clear scope and academic rigor.
