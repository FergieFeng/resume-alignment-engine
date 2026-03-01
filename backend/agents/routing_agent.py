"""
Sub-Agent E: Routing Agent

Maps symptom category to appointment type and provider pool
using the clinic's routing rules.
"""

import json
import os
import logging

logger = logging.getLogger('petcare.agents.routing')

DEFAULT_ROUTING_MAP = {
    'gastrointestinal': {'appointment_type': 'sick_visit_urgent', 'providers': ['Dr. Chen', 'Dr. Patel']},
    'respiratory': {'appointment_type': 'sick_visit_urgent', 'providers': ['Dr. Chen', 'Dr. Kim']},
    'dermatological': {'appointment_type': 'sick_visit_routine', 'providers': ['Dr. Patel', 'Dr. Wilson']},
    'injury': {'appointment_type': 'sick_visit_urgent', 'providers': ['Dr. Chen', 'Dr. Kim']},
    'urinary': {'appointment_type': 'sick_visit_urgent', 'providers': ['Dr. Patel', 'Dr. Chen']},
    'dental': {'appointment_type': 'sick_visit_routine', 'providers': ['Dr. Wilson']},
    'behavioral': {'appointment_type': 'sick_visit_routine', 'providers': ['Dr. Kim']},
    'wellness': {'appointment_type': 'wellness', 'providers': ['Dr. Patel', 'Dr. Wilson', 'Dr. Kim']},
    'other': {'appointment_type': 'sick_visit_routine', 'providers': ['Dr. Chen', 'Dr. Patel']}
}


class RoutingAgent:
    """Symptom-to-appointment routing agent."""

    def __init__(self, clinic_rules_path: str = None):
        self.agent_name = 'routing'
        self.routing_map = self._load_routing_map(clinic_rules_path)

    def _load_routing_map(self, path: str = None) -> dict:
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                return data.get('routing_map', DEFAULT_ROUTING_MAP)
        return DEFAULT_ROUTING_MAP

    def process(self, intake_data: dict, triage_result: dict) -> dict:
        """
        Map symptom category to appointment type and provider pool.

        Returns:
            dict with keys: agent_name, status, output, confidence, warnings
        """
        symptom_area = intake_data.get('symptom_details', {}).get('area', 'other')
        route = self.routing_map.get(symptom_area, self.routing_map['other'])

        urgency = triage_result.get('output', {}).get('urgency_tier', 'Routine')
        if urgency == 'Emergency':
            appointment_type = 'emergency'
        else:
            appointment_type = route['appointment_type']

        return {
            'agent_name': self.agent_name,
            'status': 'success',
            'output': {
                'symptom_category': symptom_area,
                'appointment_type': appointment_type,
                'provider_pool': route['providers'],
                'special_requirements': None
            },
            'confidence': 0.85,
            'warnings': []
        }
