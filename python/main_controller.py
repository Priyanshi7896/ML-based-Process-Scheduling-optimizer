import numpy as np
import pandas as pd
from pathlib import Path
import json
import subprocess
from predict_algo import SchedulerPredictor

class SchedulerSystem:
    def __init__(self):
        self.predictor = SchedulerPredictor()
        self.binaries = {
            "fcfs": Path("../cpp/fcfs.exe"),
            "sjf": Path("../cpp/sjf.exe"),
            "rr": Path("../cpp/rr.exe"),
            "priority": Path("../cpp/priority.exe")
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
            raise Exception(f"Algorithm error: {e.stderr.decode()}")

