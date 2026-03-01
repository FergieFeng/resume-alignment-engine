"""
Sub-Agent F: Scheduling Agent

Author: Syed Ali Turab
Date:   March 1, 2026

Proposes available appointment slots based on urgency tier,
appointment type, and provider pool. Uses mock schedule data for POC.
"""

import json
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger('petcare.agents.scheduling')


class SchedulingAgent:
    """Appointment slot proposal agent."""

    def __init__(self, slots_path: str = None):
        self.agent_name = 'scheduling'
        self.available_slots = self._load_slots(slots_path)

    def _load_slots(self, path: str = None) -> list:
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f).get('slots', [])
        return self._generate_mock_slots()

    def _generate_mock_slots(self) -> list:
        """Generate mock available slots for the next 7 days."""
        slots = []
        base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        providers = ['Dr. Chen', 'Dr. Patel', 'Dr. Kim', 'Dr. Wilson']

        for day_offset in range(7):
            day = base + timedelta(days=day_offset)
            if day.weekday() >= 5:
                continue
            for hour in [9, 10, 11, 13, 14, 15, 16]:
                slot_time = day.replace(hour=hour, minute=0)
                for provider in providers:
                    slots.append({
                        'datetime': slot_time.isoformat(),
                        'provider': provider,
                        'type': 'general',
                        'available': True
                    })
        return slots

    def process(self, routing_result: dict, triage_result: dict) -> dict:
        """
        Find matching available slots based on routing and urgency.

        Returns:
            dict with keys: agent_name, status, output, confidence, warnings
        """
        urgency = triage_result.get('output', {}).get('urgency_tier', 'Routine')
        providers = routing_result.get('output', {}).get('provider_pool', [])

        matching_slots = [
            s for s in self.available_slots
            if s.get('available') and s.get('provider') in providers
        ]

        if urgency == 'Emergency':
            return {
                'agent_name': self.agent_name,
                'status': 'success',
                'output': {
                    'proposed_slots': [],
                    'booking_status': 'not_applicable',
                    'booking_request': None,
                    'note': 'Emergency — direct to emergency clinic.'
                },
                'confidence': 1.0,
                'warnings': []
            }

        proposed = matching_slots[:3]

        return {
            'agent_name': self.agent_name,
            'status': 'success',
            'output': {
                'proposed_slots': [
                    {'datetime': s['datetime'], 'provider': s['provider']}
                    for s in proposed
                ],
                'booking_status': 'proposed' if proposed else 'manual_request',
                'booking_request': None if proposed else {
                    'urgency': urgency,
                    'appointment_type': routing_result.get('output', {}).get('appointment_type'),
                    'note': 'No matching slots found. Please review manually.'
                }
            },
            'confidence': 0.9 if proposed else 0.5,
            'warnings': [] if proposed else ['No matching slots found for criteria']
        }
