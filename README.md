<div align="center">
  
# 🚀 Enterprise MLOps Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.0+-0194E2.svg)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

An open-source, production-ready, full-stack Machine Learning Operations platform designed for enterprise scale. This monorepo bridges the gap between experimentation and production, offering a complete end-to-end lifecycle for machine learning models.

<img src="docs/portal.png" alt="Enterprise MLOps Portal Dashboard" width="100%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-top: 20px; margin-bottom: 20px;"/>

</div>

---


## 🏗️ Architecture Diagram

Below is the high-level architecture diagram representing the interactions between different microservices and infrastructure components in this MLOps platform:

```mermaid
graph TD
    %% Users
    DataScientist[Data Scientist / Admin]
    ExternalApp[Client Application]

    %% Ingress & UI
    Ingress[NGINX Ingress]
    ReactUI[React Frontend UI]

    %% APIs
    FastAPI[FastAPI Backend]

    %% Background Workers & Broker
    Redis[Redis Message Broker]
    CeleryWorker[Celery ML Worker]

    %% Storage & MLflow
    PostgreSQL[(PostgreSQL DB)]
    LocalStorage[(Local Dataset Storage)]
    MLflowServer[MLflow Tracking Server]
    MLflowStorage[(MLflow Artifacts)]

    %% Connections
    DataScientist -->|Manages Models & Datasets| Ingress
    ExternalApp -->|Real-time Inference| Ingress

    Ingress -->|/api/*| FastAPI
    Ingress -->|/*| ReactUI

    FastAPI -->|Reads/Writes Metadata| PostgreSQL
    FastAPI -->|Saves/Loads CSV| LocalStorage
    FastAPI -->|Queues Training Tasks| Redis
    FastAPI -->|Real-time Inference Loads Model| MLflowServer

    CeleryWorker -->|Polls Queue| Redis
    CeleryWorker -->|Loads CSV| LocalStorage
    CeleryWorker -->|Updates Status| PostgreSQL
    CeleryWorker -->|Logs Metrics & Artifacts| MLflowServer

    MLflowServer -->|Persists Models| MLflowStorage

    classDef db fill:#f9f,stroke:#333,stroke-width:2px;
    classDef worker fill:#ff9,stroke:#333,stroke-width:2px;
    classDef api fill:#bbf,stroke:#333,stroke-width:2px;
    
    class PostgreSQL,LocalStorage,MLflowStorage db;
    class CeleryWorker,Redis worker;
    class FastAPI,MLflowServer api;
```

---

## ✨ Core Features

### 🔐 1. Identity & Access Management (IAM)
- Secure **JWT-based authentication** and Role-Based Access Control (RBAC).
- Isolated multi-tenant architecture tracking metadata ownership by user and project.

### 📁 2. Dataset Management
- High-performance, scalable local file storage.
- Support for ingestion of large tabular datasets (CSV/Parquet).

### ⚙️ 3. Distributed Experiment Tracking
- Integrated **MLflow Tracking Server** for hyperparameter and metric logging.
- **Celery + Redis** worker pools for distributed, non-blocking asynchronous model training (e.g., Scikit-learn, XGBoost pipelines).

### 🚀 4. Model Registry & Real-Time Inference
- Version control and stage gating (Staged, Approved, Rejected, Archived) via a centralized **Model Registry**.
- High-throughput **Real-time Inference Engine** that dynamically loads models from the MLflow artifact store into memory for sub-millisecond scoring.

### 🧠 5. Explainable AI (XAI)
- Live local feature importance scoring for real-time predictions.
- Utilizes **SHAP (SHapley Additive exPlanations)** `TreeExplainer` unwrapping MLflow models dynamically.

### 📊 6. System Observability
- Deep API monitoring using `prometheus-fastapi-instrumentator`.
- Out-of-the-box system latency and traffic throughput visualization using **Grafana**.

### ☁️ 7. Cloud-Native Kubernetes Deployment
- Highly optimized, multi-stage Dockerfiles.
- Full suite of Kubernetes `apps/v1` manifests (Deployments, Services, NGINX Ingress) tailored for production scalability.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Backend Framework** | Python 3.10, FastAPI, Pydantic, SQLAlchemy |
| **Frontend Framework**| React 18, TypeScript, Vite, TailwindCSS |
| **Data Storage** | PostgreSQL, Redis, Local Disk Storage |
| **Machine Learning** | MLflow, Scikit-learn, Pandas, SHAP |
| **Asynchronous Compute**| Celery |
| **Observability** | Prometheus, Grafana |
| **Infrastructure (CI/CD)**| Docker, Kubernetes, NGINX, GitHub Actions |

---

## 📂 Repository Structure

```text
enterprise-mlops-platform/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # FastAPI Route Handlers
│   │   ├── core/           # Configs, DB Sessions, Celery Setup
│   │   ├── models/         # SQLAlchemy ORM Models
│   │   ├── schemas/        # Pydantic Validation Schemas
│   │   ├── services/       # Core Business Logic & Storage
│   │   └── worker/         # Celery Task Definitions
│   ├── tests/              # Pytest Suite
│   ├── requirements.txt    # Python Dependencies
│   └── main.py             # FastAPI App Entrypoint
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI Components
│   │   ├── layouts/        # Dashboard Shell
│   │   ├── pages/          # Feature Pages (Registry, Experiments, Datasets)
│   │   └── services/       # Axios API Client
│   ├── package.json        # Node.js Dependencies
│   └── vite.config.ts      # Vite Build Config
├── deployment/
│   ├── docker/             # Dockerfiles (Backend, Frontend, Worker)
│   └── k8s/                # Kubernetes Manifests
├── docker-compose.yml      # Local Infrastructure (Postgres, Redis, MLflow, Monitoring)
└── README.md               # You are here
```

---

## 🚀 Quick Start (Local Docker Compose)

The easiest way to run the full stack locally is via Docker Compose.

### Prerequisites
- Docker Engine & Docker Compose
- Node.js 18+ (if developing frontend locally)
- Python 3.10+ (if developing backend locally)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/enterprise-mlops-platform.git
   cd enterprise-mlops-platform
   ```

2. **Start the Infrastructure Stack:**
   This command provisions PostgreSQL, Redis, MLflow Tracking Server, Prometheus, and Grafana.
   ```bash
   docker-compose up -d --build
   ```

3. **Access the Application Interfaces:**
   - **Frontend UI (React Dashboard)**: [http://localhost:3001](http://localhost:3001)
   - **Backend API & Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **MLflow Tracking UI**: [http://localhost:5000](http://localhost:5000)
   - **Grafana Observability**: [http://localhost:3000](http://localhost:3000) (User: `admin`, Pass: `admin`)
   - **Prometheus Targets**: [http://localhost:9090](http://localhost:9090)

---

## ☸️ Production Deployment (Kubernetes)

This platform is engineered to be deployed on any Kubernetes cluster (EKS, GKE, AKS, or on-premise).

### 1. Configure Secrets
Before deploying, create the required secrets in your namespace for the PostgreSQL connection string, JWT signing keys, and Redis connection strings.
```bash
kubectl create secret generic mlops-secrets \
  --from-literal=SQLALCHEMY_DATABASE_URI="postgresql://user:pass@host:5432/db" \
  --from-literal=SECRET_KEY="your_super_secret_key"
```

### 2. Apply Manifests
Apply the suite of manifests located in `deployment/k8s/`:
```bash
kubectl apply -f deployment/k8s/
```

### 3. Verify Deployment
Verify all pods are running successfully:
```bash
kubectl get pods -l app=mlops-backend
kubectl get pods -l app=mlops-frontend
kubectl get pods -l app=mlops-worker
```

The NGINX Ingress controller is configured to route traffic based on path (`/api` -> backend, `/` -> frontend).

---

## 🧪 Testing

The platform is heavily tested using Pytest with isolated in-memory SQLite fixtures for the backend APIs.

```bash
cd backend
pytest -v
```

Tests run automatically via the integrated GitHub Actions CI/CD Pipeline upon any Push or Pull Request to the `main` branch.

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
