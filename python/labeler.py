import os
import json
import subprocess
from pathlib import Path
import statistics

# Path Configuration
SCRIPT_DIR = Path(__file__).parent
RAW_DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"
LABELED_DATA_DIR = SCRIPT_DIR.parent / "data" / "labeled"
ALGO_BINARIES = {
    "fcfs": SCRIPT_DIR.parent / "cpp" / "fcfs.exe",
    "sjf": SCRIPT_DIR.parent / "cpp" / "sjf.exe",
    "rr": SCRIPT_DIR.parent / "cpp" / "rr.exe",
    "priority": SCRIPT_DIR.parent / "cpp" / "priority.exe"
}

def run_algorithm(algo_name: str, input_data: dict) -> dict:
    """Execute a scheduling algorithm binary and capture its output."""
    try:
        proc = subprocess.run(
            [str(ALGO_BINARIES[algo_name])],
            input=json.dumps(input_data).encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return json.loads(proc.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error running {algo_name}: {e.stderr.decode()}")
        return None

def evaluate_algorithm(results: dict) -> float:
    """Calculate a combined performance score (lower is better)."""
    avg_waiting = statistics.mean(p["waiting_time"] for p in results["processes"])
    avg_turnaround = statistics.mean(p["turnaround_time"] for p in results["processes"])
    return 0.7 * avg_waiting + 0.3 * avg_turnaround  # Weighted score

def label_scenario(scenario_file: Path) -> dict:
    """Label a single scenario with the best algorithm."""
    with open(scenario_file, 'r') as f:
        scenario = json.load(f)
    
    algo_scores = {}
    for algo_name in ALGO_BINARIES:
        results = run_algorithm(algo_name, scenario)
        if results:
            algo_scores[algo_name] = evaluate_algorithm(results)
    
    best_algo = min(algo_scores, key=algo_scores.get) if algo_scores else None
    
    return {
        **scenario,
        "algorithm_scores": algo_scores,
        "best_algorithm": best_algo
    }

def main():
    LABELED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    labeled_data = []
    
    for scenario_file in RAW_DATA_DIR.glob("*.json"):
        labeled_scenario = label_scenario(scenario_file)
        if labeled_scenario["best_algorithm"]:
            labeled_data.append(labeled_scenario)
        
        # Progress feedback
        if len(labeled_data) % 100 == 0:
            print(f"Processed {len(labeled_data)} scenarios")
    
    # Save all labeled data
    output_file = LABELED_DATA_DIR / "labeled_data.json"
    with open(output_file, 'w') as f:
        json.dump(labeled_data, f, indent=2)
    
    print(f"Labeling complete. Saved to {output_file}")

if __name__ == "__main__":
    main()