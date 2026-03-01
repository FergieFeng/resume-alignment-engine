"""
PetCare Triage & Smart Booking Agent -- API Server

Author: Syed Ali Turab
Date:   March 1, 2026

Flask-based API server that serves the frontend and handles
intake requests through the orchestrator agent pipeline.

This server provides:
  - Static file serving for the frontend chat UI
  - REST API endpoints for session management and message handling
  - A /api/voice/transcribe endpoint for Whisper-based speech-to-text
  - A /api/voice/synthesize endpoint for OpenAI TTS text-to-speech
  - In-memory session storage (suitable for POC; swap to Redis/DB for prod)

Endpoints:
  GET  /                              → Serve the chat UI (index.html)
  GET  /api/health                    → Health check with version info
  POST /api/session/start             → Create a new intake session
  POST /api/session/<id>/message      → Send a text message to the agent
  GET  /api/session/<id>/summary      → Retrieve the clinic-facing summary
  POST /api/voice/transcribe          → Transcribe audio via OpenAI Whisper
  POST /api/voice/synthesize          → Convert text to speech via OpenAI TTS
"""

import os
import io
import json
import uuid
import logging
import tempfile
from datetime import datetime

from flask import Flask, request, jsonify, send_from_directory, send_file
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Load environment variables from .env file (API keys, port, log level, etc.)
load_dotenv()

# Create Flask app, serving the frontend folder as static files.
# The static_url_path='' means files in ../frontend are served at the root.
app = Flask(__name__, static_folder='../frontend', static_url_path='')

# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------

# Configure logging to both console (StreamHandler) and a log file.
# Log level is configurable via the LOG_LEVEL env var (default: INFO).
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.path.join(os.path.dirname(__file__), 'logs', 'api_server.log')
        )
    ]
)
logger = logging.getLogger('petcare_api')

# ---------------------------------------------------------------------------
# In-Memory Session Store
# ---------------------------------------------------------------------------

# Active intake sessions keyed by session_id (UUID string).
# Each session holds: pet_profile, symptoms, conversation messages,
# agent outputs, and current workflow state.
# NOTE: This is in-memory only -- sessions are lost on server restart.
# For production, replace with Redis, SQLite, or a database.
sessions = {}


# ===========================================================================
# Routes: Static File Serving
# ===========================================================================

@app.route('/')
def serve_index():
    """Serve the main frontend page (index.html) from the frontend/ folder."""
    return send_from_directory(app.static_folder, 'index.html')


# ===========================================================================
# Routes: Health Check
# ===========================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    Returns server status, current timestamp, and version.
    Useful for monitoring and deployment verification.
    """
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'voice_enabled': bool(os.getenv('OPENAI_API_KEY'))
    })


# ===========================================================================
# Routes: Session Management
# ===========================================================================

@app.route('/api/session/start', methods=['POST'])
def start_session():
    """
    Start a new intake session.

    Creates a unique session ID and initializes the session state with
    empty pet_profile, symptoms, messages, and agent_outputs.

    Returns:
        JSON with session_id, welcome message, and initial state.
    """
    session_id = str(uuid.uuid4())

    # Initialize the session data structure.
    # 'state' tracks where we are in the intake flow:
    #   'intake' → 'safety_check' → 'triage' → 'routing' → 'complete'
    sessions[session_id] = {
        'id': session_id,
        'created_at': datetime.utcnow().isoformat(),
        'state': 'intake',           # Current workflow state
        'pet_profile': {},            # Species, breed, age, weight, name
        'symptoms': {},               # Chief complaint + symptom details
        'messages': [],               # Full conversation history
        'agent_outputs': {},          # Outputs from each sub-agent
        'clarification_count': 0      # How many times we looped for clarity
    }

    logger.info(f"Session started: {session_id}")

    return jsonify({
        'session_id': session_id,
        'message': (
            "Hello! I'm the PetCare Triage Assistant. I'll help you assess "
            "your pet's symptoms and find the right care.\n\n"
            "Let's start — what type of pet do you have (dog, cat, or other)?"
        ),
        'state': 'intake'
    })


@app.route('/api/session/<session_id>/message', methods=['POST'])
def handle_message(session_id):
    """
    Handle an incoming message from the pet owner.

    Accepts a JSON body with a 'message' field containing the owner's text.
    The message may come from typed text or from voice transcription.
    Passes the message through the orchestrator pipeline and returns
    the agent's response.

    Args:
        session_id: UUID string identifying the active session.

    Request Body:
        { "message": "My dog has been vomiting since yesterday" }

    Returns:
        JSON with the agent's response message, current state, and session_id.
        If session not found, returns 404.
    """
    # Validate session exists
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404

    data = request.json
    user_message = data.get('message', '')
    session = sessions[session_id]

    # Record the user's message in the conversation history
    session['messages'].append({
        'role': 'user',
        'content': user_message,
        'timestamp': datetime.utcnow().isoformat(),
        'source': data.get('source', 'text')  # 'text' or 'voice'
    })

    # -----------------------------------------------------------------------
    # TODO: Wire up the Orchestrator pipeline here
    #
    # The orchestrator coordinates the 7-sub-agent pipeline:
    #   1. Intake Agent (A)      → parse message, update pet profile + symptoms
    #   2. Safety Gate (B)       → check for red flags → escalate if needed
    #   3. Confidence Gate (C)   → validate completeness → loop if needed
    #   4. Triage Agent (D)      → classify urgency tier
    #   5. Routing Agent (E)     → map to appointment type
    #   6. Scheduling Agent (F)  → propose available slots
    #   7. Guidance/Summary (G)  → generate owner guidance + clinic summary
    #
    # Example integration:
    #   from orchestrator import Orchestrator
    #   orch = Orchestrator(session)
    #   response = orch.process(user_message)
    # -----------------------------------------------------------------------

    # Placeholder response until the orchestrator is wired up
    response = {
        'message': (
            f"[POC STUB] Received: '{user_message}'. "
            "The orchestrator pipeline is not yet implemented. "
            "This is a placeholder response."
        ),
        'state': session['state'],
        'session_id': session_id
    }

    # Record the assistant's response in the conversation history
    session['messages'].append({
        'role': 'assistant',
        'content': response['message'],
        'timestamp': datetime.utcnow().isoformat()
    })

    return jsonify(response)


@app.route('/api/session/<session_id>/summary', methods=['GET'])
def get_summary(session_id):
    """
    Retrieve the clinic-facing summary for a session.

    Returns the structured intake data including pet profile, symptom details,
    agent outputs (triage tier, routing, scheduling), and full conversation log.
    This is the data that would be sent to the veterinary clinic's system.

    Args:
        session_id: UUID string identifying the session.

    Returns:
        JSON with full session data. 404 if session not found.
    """
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404

    session = sessions[session_id]
    return jsonify({
        'session_id': session_id,
        'state': session['state'],
        'pet_profile': session.get('pet_profile', {}),
        'agent_outputs': session.get('agent_outputs', {}),
        'messages': session.get('messages', [])
    })


# ===========================================================================
# Routes: Voice Endpoints
# ===========================================================================

@app.route('/api/voice/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio to text using OpenAI Whisper API (Tier 2 voice).

    Accepts an audio file upload (WAV, MP3, WebM, etc.) and returns
    the transcribed text. This endpoint is called by the frontend when
    the user records a voice message and Tier 2 (Whisper) is selected.

    The transcribed text can then be sent to /api/session/<id>/message
    just like a typed message.

    Request:
        multipart/form-data with 'audio' file field

    Returns:
        JSON with 'text' (transcribed string) and 'duration' (seconds).
        Returns 503 if OPENAI_API_KEY is not configured.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return jsonify({
            'error': 'Voice transcription requires OPENAI_API_KEY'
        }), 503

    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    try:
        # Import OpenAI client for Whisper transcription
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Save the uploaded audio to a temporary file.
        # Whisper API requires a file object with a filename.
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name

        # Call OpenAI Whisper API for transcription.
        # Model: whisper-1 | Cost: $0.006/minute
        with open(tmp_path, 'rb') as f:
            transcript = client.audio.transcriptions.create(
                model='whisper-1',
                file=f,
                response_format='text'
            )

        # Clean up the temp file
        os.unlink(tmp_path)

        logger.info(f"Voice transcribed: {len(transcript)} chars")

        return jsonify({
            'text': transcript.strip(),
            'source': 'whisper'
        })

    except Exception as e:
        logger.error(f"Whisper transcription failed: {e}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500


@app.route('/api/voice/synthesize', methods=['POST'])
def synthesize_speech():
    """
    Convert text to speech using OpenAI TTS API (Tier 2 voice).

    Accepts a JSON body with 'text' and optional 'voice' fields.
    Returns an MP3 audio file that the frontend can play.

    This endpoint is called by the frontend to speak the agent's response
    aloud when Tier 2 (OpenAI TTS) is selected.

    Request Body:
        { "text": "Your pet should be seen today.", "voice": "nova" }

    Available voices: alloy, ash, ballad, coral, echo, fable, nova,
                      onyx, sage, shimmer, cedar, marin

    Returns:
        Audio file (MP3) streamed to the client.
        Returns 503 if OPENAI_API_KEY is not configured.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return jsonify({
            'error': 'Voice synthesis requires OPENAI_API_KEY'
        }), 503

    data = request.json
    text = data.get('text', '')
    voice = data.get('voice', 'nova')  # 'nova' is warm and friendly

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Call OpenAI TTS API.
        # Model: tts-1 ($15/1M chars) or tts-1-hd ($30/1M chars)
        # Response is streamed as MP3 audio.
        response = client.audio.speech.create(
            model='tts-1',
            voice=voice,
            input=text
        )

        # Stream the audio bytes back to the client as an MP3 file
        audio_bytes = io.BytesIO(response.content)
        logger.info(f"TTS generated: {len(text)} chars, voice={voice}")

        return send_file(
            audio_bytes,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='response.mp3'
        )

    except Exception as e:
        logger.error(f"TTS synthesis failed: {e}")
        return jsonify({'error': f'Synthesis failed: {str(e)}'}), 500


# ===========================================================================
# Server Entry Point
# ===========================================================================

if __name__ == '__main__':
    # Ensure the logs directory exists before starting
    os.makedirs(os.path.join(os.path.dirname(__file__), 'logs'), exist_ok=True)

    port = int(os.getenv('PORT', 5002))
    debug = os.getenv('APP_ENV', 'development') == 'development'

    logger.info(f"Starting PetCare API server on port {port}")
    logger.info(f"Voice enabled: {bool(os.getenv('OPENAI_API_KEY'))}")

    app.run(host='0.0.0.0', port=port, debug=debug)
