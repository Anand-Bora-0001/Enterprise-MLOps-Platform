from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RegisteredModelBase(BaseModel):
    name: str
    version: str
    experiment_id: int
    project_id: int

class RegisteredModelCreate(RegisteredModelBase):
    pass

class RegisteredModelUpdate(BaseModel):
    status: Optional[str] = None

class RegisteredModelInDBBase(RegisteredModelBase):
    id: int
    owner_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class RegisteredModel(RegisteredModelInDBBase):
    pass

class DeploymentBase(BaseModel):
    registered_model_id: int
    endpoint_name: str

class DeploymentCreate(DeploymentBase):
    pass

class DeploymentInDBBase(DeploymentBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Deployment(DeploymentInDBBase):
    pass
