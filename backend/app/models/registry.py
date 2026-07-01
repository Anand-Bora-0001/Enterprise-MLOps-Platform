from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class RegisteredModel(Base):
    __tablename__ = "registered_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    version = Column(String, nullable=False)
    status = Column(String, default="staged") # staged, approved, rejected, archived
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    experiment = relationship("Experiment")
    project = relationship("Project")
    owner = relationship("User")

class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    registered_model_id = Column(Integer, ForeignKey("registered_models.id"))
    endpoint_name = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    registered_model = relationship("RegisteredModel")
