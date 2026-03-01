"""
Sub-Agent C: Confidence Gate Agent

Author: Syed Ali Turab
Date:   March 1, 2026

Validates required intake fields, assesses overall data confidence,
detects conflicting signals, and determines the next action.
"""

import logging

logger = logging.getLogger('petcare.agents.confidence_gate')

REQUIRED_FIELDS = ['species', 'chief_complaint']
IMPORTANT_FIELDS = ['timeline', 'eating_drinking', 'energy_level']


class ConfidenceGateAgent:
    """Field validation and confidence assessment agent."""

    def __init__(self):
        self.agent_name = 'confidence_gate'

    def process(self, intake_data: dict) -> dict:
        """
        Validate intake data completeness and confidence.

        Returns:
            dict with keys: agent_name, status, output, confidence, warnings
        """
        missing_required = []
        missing_important = []
        conflicts = []

        for field in REQUIRED_FIELDS:
            if not intake_data.get(field):
                missing_required.append(field)

        for field in IMPORTANT_FIELDS:
            if not intake_data.get(field):
                missing_important.append(field)

        # TODO: Add conflict detection logic
        # e.g., "not breathing" + "acting normal" → conflict

        completeness = 1.0 - (
            len(missing_required) * 0.3 +
            len(missing_important) * 0.1
        )
        completeness = max(0.0, min(1.0, completeness))

        if missing_required:
            action = 'clarify'
            status = 'needs_review'
        elif completeness < 0.6:
            action = 'clarify'
            status = 'needs_review'
        elif conflicts:
            action = 'human_review'
            status = 'needs_review'
        else:
            action = 'proceed'
            status = 'success'

        return {
            'agent_name': self.agent_name,
            'status': status,
            'output': {
                'confidence_score': completeness,
                'missing_required': missing_required,
                'missing_important': missing_important,
                'conflicts': conflicts,
                'action': action
            },
            'confidence': completeness,
            'warnings': [f"Missing required field: {f}" for f in missing_required]
        }
