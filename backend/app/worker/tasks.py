import os
import json
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import mlflow
import mlflow.sklearn

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.experiment import Experiment
from app.models.dataset import Dataset

@celery_app.task
def train_model_task(experiment_id: int):
    db = SessionLocal()
    try:
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if not experiment:
            return
        
        experiment.status = "running"
        db.commit()

        dataset = db.query(Dataset).filter(Dataset.id == experiment.dataset_id).first()
        
        # Load dataset
        if dataset.format == "csv":
            df = pd.read_csv(dataset.file_path)
        else:
            df = pd.read_parquet(dataset.file_path)

        # Basic dummy setup: assume last column is target
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        
        # Ensure numeric
        X = pd.get_dummies(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(f"project_{experiment.project_id}")

        with mlflow.start_run() as run:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            mlflow.log_param("model_type", experiment.model_type)
            mlflow.log_param("n_estimators", 100)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.sklearn.log_model(model, "model")

            # Update DB
            experiment.status = "completed"
            experiment.mlflow_run_id = run.info.run_id
            experiment.metrics = json.dumps({"accuracy": accuracy})
            experiment.hyperparameters = json.dumps({"n_estimators": 100})
            experiment.completed_at = datetime.utcnow()
            db.commit()

    except Exception as e:
        if experiment:
            experiment.status = "failed"
            experiment.metrics = json.dumps({"error": str(e)})
            db.commit()
    finally:
        db.close()
