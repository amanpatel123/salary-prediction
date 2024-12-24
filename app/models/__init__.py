import os
import joblib
import json
from pathlib import Path

MODELS_DIR = Path(__file__).parent

def load_model_artifacts():
    print(f"Loading model artifacts from {MODELS_DIR}")
    try:
        model = joblib.load(MODELS_DIR / 'linear_regression_model.joblib')
        encoder = joblib.load(MODELS_DIR / 'encoder.joblib')
        
        with open(MODELS_DIR / 'feature_cols.json', 'r') as f:
            feature_cols = json.load(f)
            
        return {
            'model': model,
            'encoder': encoder,
            'feature_cols': feature_cols
        }
    except Exception as e:
        raise RuntimeError(f"Error loading model artifacts: {str(e)}") 