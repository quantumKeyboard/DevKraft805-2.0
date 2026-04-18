"""
stress_simulator/simulator.py
Returns pre-defined stress simulation results for a given stress level.
No computation is performed — all data is hardcoded (per spec Section 8.9).
"""

from stress_simulator.stress_levels import StressLevel, STRESS_LEVEL_META
from stress_simulator.resource_graph import RESOURCE_DATA


def get_stress_simulation(level: int) -> dict:
    """
    Return the hardcoded stress simulation result for the given level (1–4).

    Returns:
    {
        "level": int,
        "name": str,
        "label": str,
        "description": str,
        "multiplier": str,
        "sections": [
            {
                "section": str,
                "cpu_pct": int,
                "memory_mb": int,
                "response_time_ms": int,
                "failure_probability_pct": int,
                "is_critical": bool,  # failure_probability_pct >= 50
                "is_warning": bool,   # failure_probability_pct >= 20
            }
        ]
    }
    """
    if level not in (1, 2, 3, 4):
        raise ValueError(f"Invalid stress level: {level}. Must be 1–4.")

    stress_enum = StressLevel(level)
    meta = STRESS_LEVEL_META[stress_enum]

    sections = []
    for section_name, level_data in RESOURCE_DATA.items():
        data = level_data[level]
        fp = data["failure_probability_pct"]
        sections.append({
            "section": section_name,
            "cpu_pct": data["cpu_pct"],
            "memory_mb": data["memory_mb"],
            "response_time_ms": data["response_time_ms"],
            "failure_probability_pct": fp,
            "is_critical": fp >= 50,
            "is_warning": fp >= 20,
        })

    # Sort: critical first, then warning, then normal
    sections.sort(key=lambda x: x["failure_probability_pct"], reverse=True)

    return {
        "level": level,
        "name": meta["name"],
        "label": meta["label"],
        "description": meta["description"],
        "multiplier": meta["multiplier"],
        "sections": sections,
    }
