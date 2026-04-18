"""
stress_simulator/stress_levels.py
Defines the 4 stress levels for the hardcoded stress simulator.
"""

from enum import IntEnum


class StressLevel(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    PEAK = 4


STRESS_LEVEL_META = {
    StressLevel.LOW: {
        "id": 1,
        "name": "LOW",
        "label": "Normal",
        "description": "Regular daily traffic. Baseline operation.",
        "multiplier": "1× baseline",
    },
    StressLevel.MEDIUM: {
        "id": 2,
        "name": "MEDIUM",
        "label": "Elevated",
        "description": "5× baseline. Typical peak hours.",
        "multiplier": "5× baseline",
    },
    StressLevel.HIGH: {
        "id": 3,
        "name": "HIGH",
        "label": "Stressed",
        "description": "20× baseline. Launch event or viral traffic.",
        "multiplier": "20× baseline",
    },
    StressLevel.PEAK: {
        "id": 4,
        "name": "PEAK",
        "label": "Critical",
        "description": "50× baseline. Worst-case scenario.",
        "multiplier": "50× baseline",
    },
}
