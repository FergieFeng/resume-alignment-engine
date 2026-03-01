"""
Sub-Agent B: Safety Gate Agent

Author: Syed Ali Turab
Date:   March 1, 2026

Detects emergency red flags in collected symptom data and triggers
immediate escalation messaging for life-threatening conditions.
"""

import json
import os
import logging

logger = logging.getLogger('petcare.agents.safety_gate')

DEFAULT_RED_FLAGS = [
    'difficulty breathing',
    'not breathing',
    'uncontrolled bleeding',
    'heavy bleeding',
    'seizure',
    'seizures',
    'convulsions',
    'collapse',
    'collapsed',
    'unresponsive',
    'toxin ingestion',
    'poison',
    'poisoning',
    'antifreeze',
    'chocolate toxicity',
    'rat poison',
    'inability to urinate',
    'cannot urinate',
    'straining to urinate with no output',
    'bloat',
    'distended abdomen',
    'gastric dilation',
    'hit by car',
    'trauma',
    'eye injury',
    'eye popping out',
    'proptosis',
    'severe burn',
    'drowning',
    'heat stroke',
    'hypothermia'
]

ESCALATION_MESSAGE = (
    "⚠️ EMERGENCY DETECTED: Based on the symptoms you've described, this may be "
    "a life-threatening emergency. Please take your pet to the nearest emergency "
    "veterinary clinic IMMEDIATELY. Do not wait for a regular appointment.\n\n"
    "If you're unsure where the nearest emergency clinic is, call your regular "
    "vet's office — their voicemail often has emergency clinic information."
)


class SafetyGateAgent:
    """Rule-based emergency red-flag detection agent."""

    def __init__(self, red_flags_path: str = None):
        self.agent_name = 'safety_gate'
        self.red_flags = self._load_red_flags(red_flags_path)

    def _load_red_flags(self, path: str = None) -> list:
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                return data.get('red_flags', DEFAULT_RED_FLAGS)
        return DEFAULT_RED_FLAGS

    def process(self, intake_data: dict) -> dict:
        """
        Check intake data for emergency red flags.

        Returns:
            dict with keys: agent_name, status, output, confidence, warnings
        """
        chief_complaint = intake_data.get('chief_complaint', '').lower()
        symptom_text = json.dumps(intake_data.get('symptom_details', {})).lower()
        combined_text = f"{chief_complaint} {symptom_text}"

        detected_flags = []
        for flag in self.red_flags:
            if flag.lower() in combined_text:
                detected_flags.append(flag)

        red_flag_detected = len(detected_flags) > 0

        return {
            'agent_name': self.agent_name,
            'status': 'escalate' if red_flag_detected else 'success',
            'output': {
                'red_flag_detected': red_flag_detected,
                'red_flags': detected_flags,
                'escalation_message': ESCALATION_MESSAGE if red_flag_detected else None
            },
            'confidence': 1.0 if red_flag_detected else 0.95,
            'warnings': []
        }
