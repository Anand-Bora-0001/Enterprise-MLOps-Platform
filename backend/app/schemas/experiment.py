from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class ExperimentBase(BaseModel):
    name: str
    model_type: str
    dataset_id: int
    project_id: int

class ExperimentCreate(ExperimentBase):
    pass

class ExperimentUpdate(BaseModel):
    status: Optional[str] = None
    mlflow_run_id: Optional[str] = None
    hyperparameters: Optional[str] = None
    metrics: Optional[str] = None
    completed_at: Optional[datetime] = None

class ExperimentInDBBase(ExperimentBase):
    id: int
    owner_id: int
    status: str
    mlflow_run_id: Optional[str] = None
    hyperparameters: Optional[str] = None
    metrics: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Experiment(ExperimentInDBBase):
    pass
