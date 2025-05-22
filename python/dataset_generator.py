import os
import random
import json
import math
import statistics
from pathlib import Path
from scipy.stats import skew

# Configuring
NUM_SAMPLES = 1000
MIN_PROCESSES = 3
MAX_PROCESSES = 20
MAX_ARRIVAL_TIME = 100
MAX_BURST_TIME = 50
MAX_PRIORITY = 10
MIN_QUANTUM = 1
MAX_QUANTUM = 20
EDGE_CASE_RATIO = 0.05
BURST_ARRIVAL_CHANCE = 0.3


SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"

def generate_process(pid, is_edge_case=False):
    burst = min(math.ceil(random.expovariate(0.1)), MAX_BURST_TIME)
    if is_edge_case and pid == 0:
        burst = MAX_BURST_TIME * 3
    return {
        "pid": pid,
        "arrival_time": random.randint(0, MAX_ARRIVAL_TIME),
        "burst_time": burst,
        "priority": min(max(int(random.gauss(5, 2)), 1), MAX_PRIORITY)
    }

def generate_scenario(index):
    num_processes = random.randint(MIN_PROCESSES, MAX_PROCESSES)
    is_edge_case = index < EDGE_CASE_RATIO * NUM_SAMPLES
    
    processes = [generate_process(i, is_edge_case) for i in range(num_processes)]
    
    if random.random() < BURST_ARRIVAL_CHANCE:
        arrival_time = random.randint(0, MAX_ARRIVAL_TIME // 2)
        for p in processes[-random.randint(2, 4):]:
            p["arrival_time"] = arrival_time
    
    if is_edge_case and index % 2 == 0:
        for p in processes:
            p["arrival_time"] = 0
    
    processes.sort(key=lambda x: x["arrival_time"])
    
    scenario = {
        "num_processes": num_processes,
        "processes": processes,
        "time_quantum": random.randint(MIN_QUANTUM, MAX_QUANTUM),
        "stats": {
            "avg_burst": statistics.mean(p["burst_time"] for p in processes),
            "arrival_std": statistics.stdev(p["arrival_time"] for p in processes) if num_processes > 1 else 0,
            "burst_skew": skew([p["burst_time"] for p in processes])
        }
    }
    return scenario

def save_scenario(scenario, index):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_file = DATA_DIR / f"scenario_{index:04d}.json"
    with open(output_file, 'w') as f:
        json.dump(scenario, f, indent=2)

def generate_datasets():
    print(f"Generating {NUM_SAMPLES} scenarios (including {int(EDGE_CASE_RATIO*NUM_SAMPLES)} edge cases)...")
    for i in range(NUM_SAMPLES):
        scenario = generate_scenario(i)
        save_scenario(scenario, i)
    print(f"Saved to {DATA_DIR}")

if __name__ == "__main__":
    generate_datasets()