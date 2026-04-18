"""
api/routers/stress.py
GET /stress/{level} — returns hardcoded stress simulation for level 1–4.
"""

from fastapi import APIRouter, HTTPException
from stress_simulator.simulator import get_stress_simulation

router = APIRouter(prefix="/stress", tags=["stress"])


@router.get("/{level}")
async def get_stress_result(level: int):
    if level not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=400,
            detail="Invalid stress level. Must be 1 (LOW), 2 (MEDIUM), 3 (HIGH), or 4 (PEAK).",
        )
    return get_stress_simulation(level)
