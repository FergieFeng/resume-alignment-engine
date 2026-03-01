"""
Sub-Agent A: Intake Agent

Author: Syed Ali Turab
Date:   March 1, 2026

Collects pet profile, chief complaint, and symptom details through
adaptive, multi-turn follow-up questions tailored to species and symptom area.
"""

import logging

logger = logging.getLogger('petcare.agents.intake')

REQUIRED_FIELDS = ['species', 'chief_complaint']

OPTIONAL_FIELDS = ['pet_name', 'breed', 'age', 'weight', 'timeline',
                   'eating_drinking', 'energy_level']

SYMPTOM_AREA_FOLLOWUPS = {
    'gastrointestinal': [
        'How many times has your pet vomited in the last 24 hours?',
        'Is there any diarrhea?',
        'Is there any blood in the vomit or stool?',
        'Could your pet have eaten something unusual (garbage, toys, plants)?'
    ],
    'respiratory': [
        'Is your pet having difficulty breathing or breathing rapidly?',
        'Is there coughing? If so, is it dry or productive?',
        'Any nasal discharge?',
        'Is the cough worse at night or after exercise?'
    ],
    'dermatological': [
        'Where on the body is the skin issue?',
        'Is there itching, redness, or hair loss?',
        'How long has this been going on?',
        'Any new foods, products, or environmental changes recently?'
    ],
    'injury': [
        'Where is the injury located?',
        'Is your pet able to walk/move normally?',
        'Is there swelling or bleeding?',
        'Do you know what caused the injury?'
    ],
    'urinary': [
        'Is your pet straining to urinate?',
        'Is there blood in the urine?',
        'How frequently is your pet trying to urinate?',
        'Is your pet able to produce any urine?'
    ]
}


class IntakeAgent:
    """Adaptive symptom intake agent."""

    def __init__(self):
        self.agent_name = 'intake'

    def process(self, session: dict, user_message: str) -> dict:
        """
        Process user input and return structured intake data or follow-up questions.

        Returns:
            dict with keys: agent_name, status, output, confidence, warnings
        """
        # TODO: Implement LLM-powered adaptive intake
        # 1. Parse user message for pet profile fields
        # 2. Identify symptom area
        # 3. Generate relevant follow-up questions
        # 4. Build structured output

        return {
            'agent_name': self.agent_name,
            'status': 'success',
            'output': {
                'pet_profile': {},
                'chief_complaint': user_message,
                'symptom_details': {},
                'follow_up_questions': [],
                'intake_complete': False
            },
            'confidence': 0.0,
            'warnings': ['Intake agent not yet implemented']
        }
