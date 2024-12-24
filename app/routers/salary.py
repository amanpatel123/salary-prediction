from fastapi import APIRouter, HTTPException
import pandas as pd
from app.models import load_model_artifacts
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            
        job_posting = fetch_ashby_job_posting(board_name, posting_id)
        # logger.info(f"job posting data: {job_posting}")

        # Map Ashby categories to our training data categories
        category_mapping = {
            'Cohere For AI': 'Engineering Jobs',
            'Go-to-Market': 'Sales Jobs',
            # TODO: Add more categories here. Skipping cause it takes time to figure out
        }

        contract_type_mapping = {
            'FullTime': 'permanent',
            'Contractor': 'contract',
            'PartTime': 'part-time',
            'Internship': 'permanent',
            'Temporary': 'contract'
        }

        data_for_model = {
            'Category': [category_mapping.get(job_posting.get('departmentName'), 'Other/General Jobs')],
            'ContractType': [contract_type_mapping.get(job_posting.get('employmentType'), 'permanent')],
            'ContractTime': [job_posting.get('compensationTierSummary')],
            'LocationNormalized': [job_posting.get('locationName', 'London')]
        }
        
        logger.info(f"Data for model: {data_for_model}")
        input_df = pd.DataFrame(data_for_model)
        
        X = ENCODER.transform(input_df[FEATURE_COLS])
        
        predicted_salary = MODEL.predict(X)[0]
        
        return {
            "board_name": board_name,
            "posting_id": posting_id,
            "predicted_salary": round(predicted_salary, 2),
            "job_details": {
                "category": data_for_model['Category'][0],
                "contract_type": data_for_model['ContractType'][0],
                "location": data_for_model['LocationNormalized'][0]
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error predicting salary: {str(e)}"
        ) 
    

def fetch_ashby_job_posting(board_name: str, job_posting_id: str):
    url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobPosting"
    payload = {
        "operationName": "ApiJobPosting",
        "variables": {
            "organizationHostedJobsPageName": board_name,
            "jobPostingId": job_posting_id
        },
        "query": """
query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {
  jobPosting(
    organizationHostedJobsPageName: $organizationHostedJobsPageName
    jobPostingId: $jobPostingId
  ) {
    id
    title
    departmentName
    locationName
    employmentType
    descriptionHtml
    isListed
    isConfidential
    teamNames
    secondaryLocationNames
    compensationTierSummary
    scrapeableCompensationSalarySummary
    __typename
  }
}
        """.strip()
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    job_posting = data.get("data", {}).get("jobPosting", {})
    return job_posting