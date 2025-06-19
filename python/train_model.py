import json
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
LABELED_DATA = SCRIPT_DIR.parent / "data" / "labeled" / "labeled_data.json"
MODEL_DIR = SCRIPT_DIR.parent / "data" / "model"
MODEL_DIR.mkdir(exist_ok=True)

def load_data():
    with open(LABELED_DATA, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def preprocess(df):
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

def train_with_hyperparameter_tuning():
    df = load_data()
    processed = preprocess(df)
    
    X = processed.drop('best_algo', axis=1)
    y = processed['best_algo']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define parameter grid
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    
    # Initialize GridSearchCV
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        verbose=2
    )
    
    print("Starting hyperparameter tuning...")
    grid_search.fit(X_train, y_train)
    
    # Get best model
    best_model = grid_search.best_estimator_
    
    # Evaluate
    y_pred = best_model.predict(X_test)
    print("\n=== Best Model Performance ===")
    print(classification_report(y_test, y_pred))
    
    # Save best model
    joblib.dump(best_model, MODEL_DIR / "tuned_scheduler_model.pkl")
    print(f"\nBest parameters: {grid_search.best_params_}")
    print(f"Model saved to {MODEL_DIR / 'tuned_scheduler_model.pkl'}")

if __name__ == "__main__":
    train_with_hyperparameter_tuning()