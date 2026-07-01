from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    format = Column(String, nullable=False) # e.g. csv, parquet
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project")
    owner = relationship("User")
