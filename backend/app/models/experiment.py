from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    mlflow_run_id = Column(String, unique=True, index=True, nullable=True)
    status = Column(String, default="pending") # pending, running, completed, failed
    model_type = Column(String, nullable=False)
    hyperparameters = Column(String, nullable=True) # JSON string
    metrics = Column(String, nullable=True) # JSON string
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    dataset = relationship("Dataset")
    project = relationship("Project")
    owner = relationship("User")
