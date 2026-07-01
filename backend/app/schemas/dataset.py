from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: int

class DatasetCreate(DatasetBase):
    file_path: str
    file_size_bytes: int
    format: str

class DatasetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class DatasetInDBBase(DatasetBase):
    id: int
    owner_id: int
    file_path: str
    file_size_bytes: int
    format: str
    created_at: datetime

    class Config:
        orm_mode = True

class Dataset(DatasetInDBBase):
    pass
