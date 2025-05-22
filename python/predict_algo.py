import json
import joblib
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "data" / "model" / "scheduler_model.pkl"

class SchedulerPredictor:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
    
    def predict(self, input_data):
        # Converting input to feature vector
        features = np.array([
            input_data['num_processes'],
            input_data['stats']['avg_burst'],
            input_data['stats']['arrival_std'],
            input_data['stats']['burst_skew'],
            input_data['time_quantum']
        ]).reshape(1, -1)
        
        return self.model.predict(features)[0]

if __name__ == "__main__":
    # Example 
    predictor = SchedulerPredictor()
    test_input = {
        "num_processes": 5,
        "processes": [...],  
        "time_quantum": 4,
        "stats": {
            "avg_burst": 12.4,
            "arrival_std": 3.2,
            "burst_skew": 0.8
        }
    }
    print(f"Recommended algorithm: {predictor.predict(test_input)}")