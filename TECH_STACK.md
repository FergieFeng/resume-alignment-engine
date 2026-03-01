# PetCare Triage & Smart Booking Agent -- Technology Stack

**Author:** Syed Ali Turab
**Date:** March 1, 2026

---

## Core Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Backend** | Python | 3.10+ | Primary language for all server-side logic |
| **Web Framework** | Flask | latest | REST API server, serves static frontend, session management |
| **Frontend** | HTML5 / CSS3 / JavaScript (ES6+) | -- | Chat-based intake UI, voice controls |
| **Containerization** | Docker | latest | Single-container deployment, reproducible builds |

---

## AI / LLM Layer

| Component | Technology | Pricing | Purpose |
|-----------|-----------|---------|---------|
| **Primary LLM** | OpenAI GPT-4.1 / GPT-4.1-mini | $2-10/1M tokens | Intake parsing, triage classification, guidance generation |
| **Alternative LLM** | Anthropic Claude 3.5+ | $3-15/1M tokens | Configurable fallback; strong at safety-critical reasoning |
| **LLM Framework** | LangChain + LangChain-OpenAI | -- | Agent prompting, structured output, model abstraction |
| **Observability** | LangSmith (optional) | Free tier available | LLM call tracing, latency monitoring, prompt debugging |

---

## Voice Layer

The system supports three tiers of voice interaction, each building on the previous:

### Tier 1: Browser-Native Voice (Free -- No API Cost)

| Component | Technology | Cost | Notes |
|-----------|-----------|------|-------|
| **Speech-to-Text** | Web Speech API (`SpeechRecognition`) | Free | Browser-native; Chrome/Edge full support, Safari partial |
| **Text-to-Speech** | Web Speech API (`SpeechSynthesis`) | Free | Broad browser support (Chrome 33+, Firefox 49+, Safari 7+) |

**How it works:**
- User clicks mic button → browser captures speech → transcribed to text client-side
- Text is sent to the backend through the normal `/api/session/<id>/message` endpoint
- Backend response text is spoken aloud via browser TTS
- Zero additional cost, zero server load for voice processing
- Limitation: recognition quality varies by browser/OS; no custom voice

### Tier 2: OpenAI Whisper + TTS (Higher Quality)

| Component | Technology | Cost | Notes |
|-----------|-----------|------|-------|
| **Speech-to-Text** | OpenAI Whisper API | $0.006/min (~$0.36/hr) | Highly accurate, multilingual, handles noisy audio |
| **Text-to-Speech** | OpenAI TTS (tts-1) | $15/1M chars | 13 voices, streaming, multiple formats (MP3, WAV, Opus) |
| **Text-to-Speech HD** | OpenAI TTS (tts-1-hd) | $30/1M chars | Higher quality synthesis |

**How it works:**
- User clicks mic → browser records audio → sent to backend as audio blob
- Backend forwards to Whisper API → returns transcribed text
- Text processed through normal agent pipeline
- Response text sent to OpenAI TTS → audio streamed back to browser
- Better quality than browser-native; consistent across all browsers/devices

### Tier 3: OpenAI Realtime API (Interactive Voice Conversation)

| Component | Technology | Cost | Notes |
|-----------|-----------|------|-------|
| **Real-time Voice** | OpenAI Realtime API | ~$0.15-0.20/min | Sub-500ms latency, speech-to-speech, WebSocket |
| **Audio Input** | gpt-realtime model | $32/1M audio input tokens | Bidirectional audio streaming |
| **Audio Output** | gpt-realtime model | $64/1M audio output tokens | Natural interruption handling |

**How it works:**
- WebSocket connection established between browser and OpenAI Realtime API
- Bidirectional audio streaming -- user speaks, agent responds in voice in real-time
- Sub-500ms latency (vs 1.7-3.5s for traditional STT→LLM→TTS pipeline)
- Native interruption handling (user can cut in mid-response)
- Function calling mid-conversation (can trigger triage pipeline)
- 10 available voices including Cedar and Marin (optimized for natural speech)
- No session limits (removed Feb 2025)

**Why this is compelling for PetCare:**
- Pet owners are often stressed, holding their pet, hands not free to type
- Voice is the natural intake modality (mirrors calling a clinic)
- Sub-500ms response feels like talking to a real receptionist
- Strong differentiator for the demo

### Voice Tier Comparison

| Feature | Tier 1: Browser Native | Tier 2: Whisper + TTS | Tier 3: Realtime API |
|---------|----------------------|----------------------|---------------------|
| **Cost** | Free | ~$0.02/session | ~$0.50-1.00/session |
| **Latency** | ~100ms (client-side) | ~1-2s (API round-trip) | <500ms (WebSocket) |
| **Quality** | Varies by browser | High (Whisper) | Highest (native) |
| **Interruption** | Manual (click to stop) | Manual | Native (natural) |
| **Browser Support** | Chrome/Edge best | All browsers | All browsers |
| **Conversation Feel** | Walkie-talkie | Walkie-talkie | Natural phone call |
| **Implementation** | ~2 hours | ~4 hours | ~8 hours |
| **API Key Required** | No | Yes (OpenAI) | Yes (OpenAI) |

### Recommended Approach for POC

1. **Implement Tier 1 first** (browser-native) -- free, fast to build, good enough for demo
2. **Add Tier 2 as upgrade** (Whisper + TTS) -- better quality, ~$0.02/session cost
3. **Tier 3 as stretch goal** (Realtime API) -- impressive for demo but higher cost + complexity

---

## Data Layer

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Session Storage** | In-memory (Python dict) | Active intake sessions (no persistence needed for POC) |
| **Clinic Rules** | JSON config files | Triage rules, routing maps, red-flag lists, provider data |
| **Mock Schedule** | JSON file | Simulated appointment availability |
| **Logging** | Python `logging` + file handler | API requests, agent execution, errors |

### Data Sources (External)

| Source | URL | What It Provides |
|--------|-----|-----------------|
| HuggingFace Pet Health Dataset | [karenwky/pet-health-symptoms-dataset](https://huggingface.co/datasets/karenwky/pet-health-symptoms-dataset) | 2,000 labeled symptom samples (5 conditions) |
| ASPCA AnTox Database | [aspcapro.org/antox](https://www.aspcapro.org/antox) | 1M+ poisoning cases, toxin reference |
| ASPCA Top Toxins 2024 | [aspcapro.org/resource/top-10-toxins-2024](https://www.aspcapro.org/resource/top-10-toxins-2024) | Prioritized toxin categories |
| Vet-AI Symptom Checker | [vet-ai.com/symptomchecker](https://www.vet-ai.com/symptomchecker) | 165 vet-written triage algorithms |
| SAVSNET / PetBERT | [github.com/SAVSNET/PetBERT](https://github.com/SAVSNET/PetBERT) | Veterinary NLP model reference |

---

## Infrastructure & Deployment

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Container Runtime** | Docker | Reproducible builds, single-container deployment |
| **Cloud Hosting** | Render / Railway | Free-tier deployment for POC |
| **Version Control** | Git + GitHub | Source code, branching (`PetCare` branch) |
| **Start Scripts** | `start.sh` (Bash) / `start.ps1` (PowerShell) | One-click setup (key prompts, build, run) |

---

## Python Dependencies

| Package | Purpose |
|---------|---------|
| `flask` | Web server and REST API |
| `python-dotenv` | Environment variable management from `.env` |
| `pydantic` | Data validation and JSON schema enforcement |
| `openai` | OpenAI API client (GPT-4.1, Whisper, TTS, Realtime) |
| `anthropic` | Anthropic API client (Claude) |
| `langchain` | LLM abstraction, prompt templating, agent tooling |
| `langchain-openai` | LangChain ↔ OpenAI integration |
| `langchain-anthropic` | LangChain ↔ Anthropic integration |
| `streamlit` | Optional: quick prototyping UI (from main branch) |

---

## Security & Privacy

| Concern | Approach |
|---------|----------|
| **API Keys** | Stored in `.env` (gitignored), never committed |
| **Owner PII** | Session-only memory; no persistent storage |
| **Medical Safety** | Non-diagnostic language enforced; Safety Gate runs before all routing |
| **Data Retention** | Anonymized logs only; no PHI stored |
| **Transport** | HTTPS in production (Render/Railway default) |

---

## Future Integrations (Post-POC)

| Integration | Technology | Purpose |
|-------------|-----------|---------|
| Clinic Scheduling API | REST / FHIR | Real-time appointment booking |
| EMR/CRM | HL7 FHIR / proprietary | Patient record handoff |
| SMS/Email | Twilio / SendGrid | Appointment confirmation, follow-up |
| Mobile App | React Native / Flutter | Native mobile intake experience |
| Analytics | PostHog / Mixpanel | Usage tracking, triage accuracy monitoring |
