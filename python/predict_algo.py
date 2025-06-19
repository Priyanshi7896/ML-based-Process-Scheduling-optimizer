import joblib
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "data" / "model" / "tuned_scheduler_model.pkl"

class SchedulerPredictor:
    def __init__(self):
        try:
            self.model = joblib.load(MODEL_PATH)
        except FileNotFoundError:
            raise Exception("Trained model not found. Run train_model.py first.")
    
    def predict(self, input_data):
        features = np.array([
            input_data['num_processes'],
            input_data['stats']['avg_burst'],
            input_data['stats']['arrival_std'],
            input_data['stats']['burst_skew'],
            input_data['time_quantum']
        ]).reshape(1, -1)
        
        return self.model.predict(features)[0]





