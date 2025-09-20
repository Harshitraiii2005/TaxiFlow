
 # 🚖 TaxiFlow

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Airflow](https://img.shields.io/badge/airflow-2.10-blue?logo=apache-airflow\&logoColor=white)](https://airflow.apache.org/)
[![Docker](https://img.shields.io/badge/docker-24.0-blue?logo=docker\&logoColor=white)](https://www.docker.com/)
[![S3](https://img.shields.io/badge/AWS%20S3-ff9900?logo=amazon-aws\&logoColor=white)](https://aws.amazon.com/s3/)
[![Prometheus](https://img.shields.io/badge/prometheus-ff0000?logo=prometheus\&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/grafana-f46800?logo=grafana\&logoColor=white)](https://grafana.com/)
[![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-blue?logo=github\&logoColor=white)](https://github.com/features/actions)

---

## Overview

**TaxiFlow** is an **end-to-end ML pipeline** for taxi trip predictions. It automates:

* Data fetching from **S3** using **Astro Airflow**
* Data ingestion & preprocessing
* Model training and evaluation
* Best model selection for production
* Triggering **Flask app (`app.py`)** for serving predictions
* Dockerized deployment on port **5055**
* Monitoring via **Prometheus & Grafana**
* CI/CD automation using **GitHub Actions**

---

## 🏗 Architecture Diagram

```mermaid
flowchart TD
    subgraph Data Layer
        S3[(AWS S3 Bucket)]
    end

    subgraph Orchestration
        Airflow[Astro Airflow DAGs]
        Ingest[Data Ingestion]
        Preprocess[Preprocessing]
        Train[Model Training]
        Evaluate[Evaluation & Best Model Selection]
    end

    subgraph Application Layer
        App[Flask App - app.py]
        Docker[Docker Container :5055]
    end

    subgraph Monitoring
        Prometheus[Prometheus Metrics]
        Grafana[Grafana Dashboard]
    end

    S3 --> Ingest
    Ingest --> Preprocess
    Preprocess --> Train
    Train --> Evaluate
    Evaluate --> App
    App --> Docker
    Docker --> Prometheus
    Prometheus --> Grafana
```

---

## 🔹 DAG Structure

* **`ingest_task`** – Fetches data from **S3**
* **`preprocess_task`** – Cleans, scales, encodes data
* **`train_task`** – Trains multiple ML models
* **`evaluate_task`** – Picks best model based on metrics
* **`trigger_app_task`** – Deploys the best model via **Flask app**

Each task is modular, so adding new preprocessing steps or models is easy.

---

## 🐳 Docker Setup for Flask App

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dags /app/dags
COPY include /app/include
COPY app.py /app/app.py
COPY assets /app/assets

EXPOSE 5055

CMD ["python", "app.py"]
```

**Run the container:**

```bash
docker build -t taxiflow-app .
docker run -d -p 5055:5055 taxiflow-app
```

---

## 🛠 Docker Setup for Astro Airflow

If you want to **run Astro Airflow in Docker**, use this base image:

```dockerfile
FROM astrocrpublic.azurecr.io/runtime:3.0-10

```

**Run Astro Airflow container:**

```bash
astro dev init
astro dev start
```

This allows you to **orchestrate DAGs** while keeping Flask app separate.

---

## 📊 Prometheus & Grafana Integration

1. Expose metrics in **`app.py`** using Prometheus client:

```python
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
```

2. Add a **`/metrics` endpoint** to Flask app.
3. Connect **Grafana** to Prometheus to visualize:

* Number of predictions
* Model inference time
* Errors

---

## ⚙️ CI/CD with GitHub Actions

```yaml
name: CI/CD for Astro Airflow

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-run:
    runs-on: ubuntu-latest

    steps:
      # 1️⃣ Checkout repository
      - name: Checkout repo
        uses: actions/checkout@v3

      # 2️⃣ Install Docker (official way, avoids containerd conflicts)
      - name: Install Docker
        run: |
          curl -fsSL https://get.docker.com -o get-docker.sh
          sudo sh get-docker.sh
          sudo usermod -aG docker $USER
          docker --version

      # 3️⃣ Install Astro CLI
      - name: Install Astro CLI
        run: |
          curl -sSL https://install.astronomer.io | sudo bash
          astro version

      # 4️⃣ Initialize Astro project (if Dockerfile not present)
      - name: Initialize Astro project
        run: |
          if [ ! -f "Dockerfile" ]; then
            astro dev init
          fi

      # 5️⃣ Start Astro Airflow in background
      - name: Start Astro Airflow
        run: |
          nohup astro dev start > airflow.log 2>&1 &
          echo "Waiting for Airflow webserver on port 8080..."
          for i in {1..30}; do
            if curl -s http://localhost:8080/health | grep "healthy"; then
              echo "✅ Airflow started"
              break
            else
              sleep 5
            fi
          done

      # 6️⃣ Build Docker image
      - name: Build Docker image
        run: |
          astro dev build
          # Tag the built image
          docker tag $(docker images --format "{{.Repository}}:{{.Tag}}" | grep airflow) my-astro-airflow:latest

      # 7️⃣ Run Docker container
      - name: Run Docker container
        run: |
          docker run -d --name astro-container -p 8080:8080 my-astro-airflow:latest
          echo "Container started"
          sleep 20

      # 8️⃣ Optional cleanup
      - name: Cleanup Docker container
        if: always()
        run: |
          docker stop astro-container || true
          docker rm astro-container || true
```

---

## 📸 Screenshots / Demo

1️⃣ **Airflow DAGs** <img width="1045" height="863" alt="Airflow DAGs" src="https://github.com/user-attachments/assets/c00d2c87-e8da-45e4-84d6-bbd6f94ae955" />

2️⃣ **Successful run Airflow** <img width="1600" height="1000" alt="Airflow Run" src="https://github.com/user-attachments/assets/de7f9acd-b4ca-49c0-bb28-669c8d360b96" />

3️⃣ **DAGs detail** <img width="1600" height="928" alt="DAGs Detail" src="https://github.com/user-attachments/assets/954abd82-3a97-4ee4-a332-bb87d374ac5a" />

4️⃣ **Prometheus Metrics** <img width="1592" height="924" alt="Prometheus Metrics" src="https://github.com/user-attachments/assets/4ff6fcf7-2216-4cf6-a78c-ecad61f4687a" />

5️⃣ **Grafana Dashboard** <img width="1600" height="928" alt="Grafana Dashboard" src="https://github.com/user-attachments/assets/2d4d63c5-b77e-426e-a407-e32af99d8d02" />

6️⃣ **Running App** <img width="1600" height="920" alt="Running App" src="https://github.com/user-attachments/assets/ee5e4424-9c38-4d2e-b9be-0e4fc1a11a97" />

7️⃣ **Docker Container** <img width="1600" height="1000" alt="image" src="https://github.com/user-attachments/assets/c66e1f09-1ddc-46a8-adad-52276e20a1cc" />


---

## 🛠 Tech Stack

| Layer            | Technology                                       |
| ---------------- | ------------------------------------------------ |
| Orchestration    | Astro Airflow                                    |
| Data Storage     | AWS S3                                           |
| Programming      | Python 3.11                                      |
| Containerization | Docker                                           |
| Monitoring       | Prometheus, Grafana                              |
| CI/CD            | GitHub Actions                                   |
| ML Framework     | scikit-learn / XGBoost / LightGBM (customizable) |

📄 License

This project is licensed under the Apache License 2.0
.

© 2025 Harshit Rai
