import os
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.services.storage import save_upload_file

router = APIRouter()

@router.get("/", response_model=List[schemas.Dataset])
def read_datasets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve datasets.
    """
    datasets = db.query(models.Dataset).filter(models.Dataset.owner_id == current_user.id).offset(skip).limit(limit).all()
    return datasets

@router.post("/upload", response_model=schemas.Dataset)
async def upload_dataset(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload a new dataset.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by user")
    
    file_path = save_upload_file(file, current_user.id, project_id)
    file_size = os.path.getsize(file_path)
    file_format = file.filename.split(".")[-1] if "." in file.filename else "unknown"

    dataset = models.Dataset(
        name=file.filename,
        description=description,
        file_path=file_path,
        file_size_bytes=file_size,
        format=file_format,
        project_id=project_id,
        owner_id=current_user.id
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset
