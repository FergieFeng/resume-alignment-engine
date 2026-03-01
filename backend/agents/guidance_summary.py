"""
Sub-Agent G: Guidance & Summary Agent

Author: Syed Ali Turab
Date:   March 1, 2026

Generates safe, non-diagnostic owner guidance ("do/don't while waiting")
and produces a structured clinic-ready intake summary.
"""

import logging
from datetime import datetime

logger = logging.getLogger('petcare.agents.guidance_summary')

GENERAL_GUIDANCE = {
    'do': [
        'Keep fresh water available for your pet',
        'Monitor your pet closely for any changes',
        'Keep your pet in a calm, comfortable environment',
        'Note any new or worsening symptoms'
    ],
    'dont': [
        'Do not give human medications without veterinary guidance',
        'Do not force-feed your pet if they are refusing food',
        'Do not attempt to induce vomiting unless directed by a veterinarian'
    ],
    'watch_for': [
        'Difficulty breathing or rapid breathing',
        'Extreme lethargy or collapse',
        'Severe or uncontrolled bleeding',
        'Seizures or loss of consciousness'
    ]
}

AREA_SPECIFIC_GUIDANCE = {
    'gastrointestinal': {
        'do': ['Offer small amounts of water frequently', 'Note frequency and appearance of vomiting/diarrhea'],
        'dont': ['Do not give fatty or rich foods', 'Do not give dairy products'],
        'watch_for': ['Blood in vomit or stool', 'Abdominal swelling or distension']
    },
    'respiratory': {
        'do': ['Keep your pet in a well-ventilated area', 'Minimize exercise and excitement'],
        'dont': ['Do not use a tight collar if breathing is labored'],
        'watch_for': ['Blue or pale gums', 'Open-mouth breathing (especially cats)']
    },
    'injury': {
        'do': ['Restrict movement to prevent further injury', 'Apply gentle pressure to bleeding wounds with a clean cloth'],
        'dont': ['Do not apply ice directly to the skin', 'Do not attempt to splint or set broken bones'],
        'watch_for': ['Increasing swelling', 'Loss of use of a limb']
    }
}


class GuidanceSummaryAgent:
    """Owner guidance and clinic summary generation agent."""

    def __init__(self):
        self.agent_name = 'guidance_summary'

    def process(self, session: dict, all_agent_outputs: dict) -> dict:
        """
        Generate owner guidance and clinic-facing summary.

        Returns:
            dict with keys: agent_name, status, output, confidence, warnings
        """
        symptom_area = session.get('symptoms', {}).get('area', '')
        area_guidance = AREA_SPECIFIC_GUIDANCE.get(symptom_area, {})

        guidance = {
            'do': GENERAL_GUIDANCE['do'] + area_guidance.get('do', []),
            'dont': GENERAL_GUIDANCE['dont'] + area_guidance.get('dont', []),
            'watch_for': GENERAL_GUIDANCE['watch_for'] + area_guidance.get('watch_for', [])
        }

        clinic_summary = {
            'version': '1.0.0',
            'session_id': session.get('id', ''),
            'timestamp': datetime.utcnow().isoformat(),
            'pet_profile': session.get('pet_profile', {}),
            'chief_complaint': session.get('symptoms', {}).get('chief_complaint', ''),
            'symptom_details': session.get('symptoms', {}),
            'red_flags': all_agent_outputs.get('safety_gate', {}).get('output', {}),
            'triage': all_agent_outputs.get('triage', {}).get('output', {}),
            'routing': all_agent_outputs.get('routing', {}).get('output', {}),
            'scheduling': all_agent_outputs.get('scheduling', {}).get('output', {}),
            'confidence': {
                'overall': all_agent_outputs.get('confidence_gate', {}).get('confidence', 0),
                'intake_completeness': all_agent_outputs.get('confidence_gate', {}).get('output', {}).get('confidence_score', 0),
                'triage_confidence': all_agent_outputs.get('triage', {}).get('confidence', 0),
                'needs_review': all_agent_outputs.get('confidence_gate', {}).get('output', {}).get('action') == 'human_review'
            },
            'owner_guidance': guidance,
            'metadata': {
                'agents_executed': list(all_agent_outputs.keys())
            }
        }

        return {
            'agent_name': self.agent_name,
            'status': 'success',
            'output': {
                'owner_guidance': guidance,
                'clinic_summary': clinic_summary
            },
            'confidence': 0.85,
            'warnings': []
        }
