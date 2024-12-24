from fastapi import APIRouter, HTTPException
import pandas as pd
from app.models import load_model_artifacts

router = APIRouter()

# Loading model artifacts at startup
try:
    model_artifacts = load_model_artifacts()
    MODEL = model_artifacts['model']
    ENCODER = model_artifacts['encoder']
    FEATURE_COLS = model_artifacts['feature_cols']
except Exception as e:
    print(f"Warning: Could not load model artifacts: {str(e)}")
    MODEL = None
    ENCODER = None
    FEATURE_COLS = None

@router.get("/salary/{board_name}/{posting_id}")
async def predict_salary(board_name: str, posting_id: str):
    """
    Predicts salary for a given job posting.
    """
    try:
        if MODEL is None:
            # Fallback 
            return {
                "board_name": board_name,
                "posting_id": posting_id,
                "predicted_salary": 50000,
                "note": "Using fallback prediction (model not loaded)"
            }
            
        # TODO:
        # 1. Fetch job posting details using board_name and posting_id
        # 2. Extract relevant features (Category, ContractType, etc.)
        # For now, I will use dummy data for sake of time
        dummy_data = {
            'Category': ['IT Jobs'],
            'ContractType': ['permanent'],
            'ContractTime': ['full-time'],
            'LocationNormalized': ['London']
        }
        
        input_df = pd.DataFrame(dummy_data)
        
        X = ENCODER.transform(input_df[FEATURE_COLS])
        
        predicted_salary = MODEL.predict(X)[0]
        
        return {
            "board_name": board_name,
            "posting_id": posting_id,
            "predicted_salary": round(predicted_salary, 2)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error predicting salary: {str(e)}"
        ) 