from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.api import deps
import mlflow
import numpy as np
import shap

router = APIRouter()

@router.post("/{endpoint_name}")
def explain_prediction(
    endpoint_name: str,
    payload: dict,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Generate SHAP values for a given prediction payload.
    """
    deployment = db.query(models.Deployment).filter(models.Deployment.endpoint_name == endpoint_name, models.Deployment.is_active == True).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    reg_model = db.query(models.RegisteredModel).filter(models.RegisteredModel.id == deployment.registered_model_id).first()
    experiment = db.query(models.Experiment).filter(models.Experiment.id == reg_model.experiment_id).first()

    try:
        # Fetch the model
        model_uri = f"runs:/{experiment.mlflow_run_id}/model"
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        
        import pandas as pd
        input_data = pd.DataFrame([payload])
        
        # NOTE: In a real system, you'd need the training data or a background distribution to initialize SHAP.
        # Here we use a dummy TreeExplainer assuming a tree model.
        underlying_model = loaded_model.unwrap_python_model().model
        
        explainer = shap.TreeExplainer(underlying_model)
        shap_values = explainer.shap_values(input_data)
        
        return {
            "prediction": loaded_model.predict(input_data).tolist(),
            "shap_values": np.array(shap_values).tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
