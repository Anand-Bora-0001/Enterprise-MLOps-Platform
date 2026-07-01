from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.worker.tasks import train_model_task

router = APIRouter()

@router.get("/", response_model=List[schemas.Experiment])
def read_experiments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve experiments.
    """
    experiments = db.query(models.Experiment).filter(models.Experiment.owner_id == current_user.id).offset(skip).limit(limit).all()
    return experiments

@router.post("/", response_model=schemas.Experiment)
def create_experiment(
    *,
    db: Session = Depends(deps.get_db),
    experiment_in: schemas.ExperimentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create and start a new experiment (training job).
    """
    project = db.query(models.Project).filter(models.Project.id == experiment_in.project_id).first()
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")

    dataset = db.query(models.Dataset).filter(models.Dataset.id == experiment_in.dataset_id).first()
    if not dataset or dataset.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Dataset not found")

    experiment = models.Experiment(
        name=experiment_in.name,
        model_type=experiment_in.model_type,
        dataset_id=experiment_in.dataset_id,
        project_id=experiment_in.project_id,
        owner_id=current_user.id
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    # Trigger Celery Background Task
    train_model_task.delay(experiment.id)

    return experiment
