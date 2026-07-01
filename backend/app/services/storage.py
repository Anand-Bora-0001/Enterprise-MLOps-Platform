import os
import shutil
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage", "datasets")

def init_storage():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile, user_id: int, project_id: int) -> str:
    init_storage()
    # Create an isolated path per project
    project_dir = os.path.join(UPLOAD_DIR, str(user_id), str(project_id))
    os.makedirs(project_dir, exist_ok=True)
    
    file_path = os.path.join(project_dir, upload_file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return file_path
