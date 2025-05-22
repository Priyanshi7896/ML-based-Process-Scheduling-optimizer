import json
import numpy as np  # Added import
import pandas as pd  # Added import
from predict_algo import SchedulerPredictor
from pathlib import Path
import subprocess

class SchedulerSystem:
    def __init__(self):
        self.predictor = SchedulerPredictor()
        self.binaries = {
            "fcfs": Path("../cpp/fcfs.exe"),  # Fixed path
            "sjf": Path("../cpp/sjf.exe"),
            "rr": Path("../cpp/rr.exe"),
            "priority": Path("../cpp/priority.exe")
        }
    
    def get_user_input(self):
        """Simulating user input """
        num_processes = int(input("Number of processes: "))
        processes = []
        for i in range(num_processes):
            print(f"\nProcess {i}:")
            at = int(input("Arrival time: "))
            bt = int(input("Burst time: "))
            priority = int(input("Priority: "))
            processes.append({"pid": i, "arrival_time": at, "burst_time": bt, "priority": priority})
        
        time_quantum = int(input("\nTime quantum (for RR): "))
        return {
            "num_processes": num_processes,
            "processes": processes,  
            "time_quantum": time_quantum,
            "stats": self.calculate_stats(processes)
        }
    
    def calculate_stats(self, processes):
        bursts = [p['burst_time'] for p in processes]
        arrivals = [p['arrival_time'] for p in processes]
        return {
            "avg_burst": np.mean(bursts),
            "arrival_std": np.std(arrivals) if len(arrivals) > 1 else 0,
            "burst_skew": pd.Series(bursts).skew()
        }
    
    def run_algorithm(self, algo, input_data):
        """Execute the scheduling algorithm binary"""
        try:
            result = subprocess.run(
                [str(self.binaries[algo])],
                input=json.dumps(input_data).encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return json.loads(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Error running {algo}: {e.stderr.decode()}")
            return None
    
    def execute(self):
        print("=== Process Scheduling Optimizer ===")
        user_input = self.get_user_input()
        best_algo = self.predictor.predict(user_input)
        print(f"\nRecommended algorithm: {best_algo.upper()}")
        
        results = self.run_algorithm(best_algo, user_input)
        if results:
            print("\n=== Scheduling Results ===")
            print(json.dumps(results, indent=2))
        else:
            print("Failed to get results.")

if __name__ == "__main__":
    system = SchedulerSystem()
    system.execute()