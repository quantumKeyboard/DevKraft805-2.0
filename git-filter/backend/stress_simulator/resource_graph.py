"""
stress_simulator/resource_graph.py
Pre-defined resource allocation data per section per stress level.
All values are hardcoded as per spec Section 8.9.
"""

# Format:
# RESOURCE_DATA[section][level] = {cpu_pct, memory_mb, response_time_ms, failure_probability_pct}

RESOURCE_DATA: dict[str, dict[int, dict]] = {
    "Backend": {
        1: {"cpu_pct": 15,  "memory_mb": 512,   "response_time_ms": 120,  "failure_probability_pct": 1},
        2: {"cpu_pct": 45,  "memory_mb": 1200,  "response_time_ms": 350,  "failure_probability_pct": 5},
        3: {"cpu_pct": 78,  "memory_mb": 2800,  "response_time_ms": 1200, "failure_probability_pct": 22},
        4: {"cpu_pct": 95,  "memory_mb": 4500,  "response_time_ms": 4500, "failure_probability_pct": 60},
    },
    "UI": {
        1: {"cpu_pct": 5,   "memory_mb": 128,   "response_time_ms": 50,   "failure_probability_pct": 0},
        2: {"cpu_pct": 12,  "memory_mb": 256,   "response_time_ms": 100,  "failure_probability_pct": 1},
        3: {"cpu_pct": 22,  "memory_mb": 512,   "response_time_ms": 300,  "failure_probability_pct": 8},
        4: {"cpu_pct": 35,  "memory_mb": 900,   "response_time_ms": 900,  "failure_probability_pct": 22},
    },
    "External": {
        1: {"cpu_pct": 8,   "memory_mb": 256,   "response_time_ms": 200,  "failure_probability_pct": 2},
        2: {"cpu_pct": 20,  "memory_mb": 512,   "response_time_ms": 500,  "failure_probability_pct": 8},
        3: {"cpu_pct": 40,  "memory_mb": 1000,  "response_time_ms": 1500, "failure_probability_pct": 35},
        4: {"cpu_pct": 65,  "memory_mb": 2000,  "response_time_ms": 5000, "failure_probability_pct": 75},
    },
    "Utils": {
        1: {"cpu_pct": 3,   "memory_mb": 64,    "response_time_ms": 20,   "failure_probability_pct": 0},
        2: {"cpu_pct": 8,   "memory_mb": 128,   "response_time_ms": 40,   "failure_probability_pct": 1},
        3: {"cpu_pct": 15,  "memory_mb": 256,   "response_time_ms": 100,  "failure_probability_pct": 5},
        4: {"cpu_pct": 25,  "memory_mb": 512,   "response_time_ms": 300,  "failure_probability_pct": 15},
    },
    "Config": {
        1: {"cpu_pct": 1,   "memory_mb": 32,    "response_time_ms": 5,    "failure_probability_pct": 0},
        2: {"cpu_pct": 2,   "memory_mb": 32,    "response_time_ms": 5,    "failure_probability_pct": 1},
        3: {"cpu_pct": 3,   "memory_mb": 64,    "response_time_ms": 10,   "failure_probability_pct": 1},
        4: {"cpu_pct": 5,   "memory_mb": 64,    "response_time_ms": 20,   "failure_probability_pct": 3},
    },
    "Tests": {
        1: {"cpu_pct": 0,   "memory_mb": 0,     "response_time_ms": 0,    "failure_probability_pct": 0},
        2: {"cpu_pct": 0,   "memory_mb": 0,     "response_time_ms": 0,    "failure_probability_pct": 0},
        3: {"cpu_pct": 0,   "memory_mb": 0,     "response_time_ms": 0,    "failure_probability_pct": 0},
        4: {"cpu_pct": 0,   "memory_mb": 0,     "response_time_ms": 0,    "failure_probability_pct": 0},
    },
}
