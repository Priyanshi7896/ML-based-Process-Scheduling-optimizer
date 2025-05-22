import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from pathlib import Path

# Telling Paths
SCRIPT_DIR = Path(__file__).parent
LABELED_DATA = SCRIPT_DIR.parent / "data" / "labeled" / "labeled_data.json"
MODEL_DIR = SCRIPT_DIR.parent / "data" / "model"
MODEL_DIR.mkdir(exist_ok=True)

def load_data():
    with open(LABELED_DATA, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def preprocess(df):
    # Feature engineering
    features = []
    for _, row in df.iterrows():
        stats = row['stats']
        features.append({
            'num_processes': row['num_processes'],
            'avg_burst': stats['avg_burst'],
            'arrival_std': stats['arrival_std'],
            'burst_skew': stats['burst_skew'],
            'time_quantum': row['time_quantum'],
            'best_algo': row['best_algorithm']
        })
    return pd.DataFrame(features)

def train():
    df = load_data()
    processed = preprocess(df)
    
    X = processed.drop('best_algo', axis=1)
    y = processed['best_algo']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Evaluating
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Saving model
    joblib.dump(model, MODEL_DIR / "scheduler_model.pkl")
    print(f"Model saved to {MODEL_DIR}")

if __name__ == "__main__":
    train()