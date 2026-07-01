from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
import mlflow
import numpy as np

router = APIRouter()

@router.get("/models", response_model=List[schemas.RegisteredModel])
def read_registered_models(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve registered models.
    """
    models_db = db.query(models.RegisteredModel).filter(models.RegisteredModel.owner_id == current_user.id).offset(skip).limit(limit).all()
    return models_db

@router.post("/models", response_model=schemas.RegisteredModel)
def register_model(
    *,
    db: Session = Depends(deps.get_db),
    model_in: schemas.RegisteredModelCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Register a model from an experiment.
    """
    experiment = db.query(models.Experiment).filter(models.Experiment.id == model_in.experiment_id).first()
    if not experiment or experiment.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Experiment not found")

    if experiment.status != "completed":
        raise HTTPException(status_code=400, detail="Experiment is not completed")

    registered_model = models.RegisteredModel(
        name=model_in.name,
        version=model_in.version,
        experiment_id=model_in.experiment_id,
        project_id=model_in.project_id,
        owner_id=current_user.id
    )
    db.add(registered_model)
    db.commit()
    db.refresh(registered_model)
    return registered_model

@router.post("/deployments", response_model=schemas.Deployment)
def deploy_model(
    *,
    db: Session = Depends(deps.get_db),
    deployment_in: schemas.DeploymentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Deploy a registered model to a real-time endpoint.
    """
    reg_model = db.query(models.RegisteredModel).filter(models.RegisteredModel.id == deployment_in.registered_model_id).first()
    if not reg_model or reg_model.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Registered model not found")
    
    # In a real system, this would trigger Kubernetes API to spin up a pod
    deployment = models.Deployment(
        registered_model_id=reg_model.id,
        endpoint_name=deployment_in.endpoint_name
    )
    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    # Automatically approve the model for simplicity
    reg_model.status = "approved"
    db.commit()

    return deployment

@router.post("/inference/{endpoint_name}")
def predict(
    endpoint_name: str,
    payload: dict,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Real-time inference endpoint.
    """
    deployment = db.query(models.Deployment).filter(models.Deployment.endpoint_name == endpoint_name, models.Deployment.is_active == True).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    reg_model = db.query(models.RegisteredModel).filter(models.RegisteredModel.id == deployment.registered_model_id).first()
    experiment = db.query(models.Experiment).filter(models.Experiment.id == reg_model.experiment_id).first()

    try:
        # Fetch the model from MLflow
        model_uri = f"runs:/{experiment.mlflow_run_id}/model"
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        
        # Parse payload and predict
        import pandas as pd
        input_data = pd.DataFrame([payload])
        prediction = loaded_model.predict(input_data)
        
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
