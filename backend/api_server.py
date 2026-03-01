"""
PetCare Triage & Smart Booking Agent -- API Server

Author: Syed Ali Turab
Date:   March 1, 2026

Flask-based API server that serves the frontend and handles
intake requests through the orchestrator agent pipeline.
"""

import os
import json
import uuid
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')

logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'logs', 'api_server.log'))
    ]
)
logger = logging.getLogger('petcare_api')

sessions = {}


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/session/start', methods=['POST'])
def start_session():
    """Start a new intake session."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        'id': session_id,
        'created_at': datetime.utcnow().isoformat(),
        'state': 'intake',
        'pet_profile': {},
        'symptoms': {},
        'messages': [],
        'agent_outputs': {}
    }
    logger.info(f"Session started: {session_id}")
    return jsonify({
        'session_id': session_id,
        'message': "Hello! I'm the PetCare Triage Assistant. I'll help you assess your pet's symptoms and find the right care. Let's start — what type of pet do you have (dog, cat, or other)?",
        'state': 'intake'
    })


@app.route('/api/session/<session_id>/message', methods=['POST'])
def handle_message(session_id):
    """Handle an incoming message from the owner."""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404

    data = request.json
    user_message = data.get('message', '')
    session = sessions[session_id]

    session['messages'].append({
        'role': 'user',
        'content': user_message,
        'timestamp': datetime.utcnow().isoformat()
    })

    # TODO: Replace with orchestrator pipeline
    # from orchestrator import Orchestrator
    # orchestrator = Orchestrator(session)
    # response = orchestrator.process(user_message)

    response = {
        'message': f"[POC STUB] Received: '{user_message}'. The orchestrator pipeline is not yet implemented. This is a placeholder response.",
        'state': session['state'],
        'session_id': session_id
    }

    session['messages'].append({
        'role': 'assistant',
        'content': response['message'],
        'timestamp': datetime.utcnow().isoformat()
    })

    return jsonify(response)


@app.route('/api/session/<session_id>/summary', methods=['GET'])
def get_summary(session_id):
    """Get the clinic-facing summary for a completed session."""
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


if __name__ == '__main__':
    os.makedirs(os.path.join(os.path.dirname(__file__), 'logs'), exist_ok=True)
    port = int(os.getenv('PORT', 5002))
    debug = os.getenv('APP_ENV', 'development') == 'development'
    logger.info(f"Starting PetCare API server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
