from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys

# Add 'include' folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'include'))

# Import modular functions
from include.ingestion import ingest_from_s3
from include.preprocessing import preprocess
from include.train import train_all_models
from include.evaluate import evaluate_all_models

# -----------------------------
# Persistent folders
# -----------------------------
DATA_DIR = "/tmp/airflow_data"
MODEL_DIR = os.path.join(DATA_DIR, "models")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# S3 Config
# -----------------------------
BUCKET = "your-bucket"
FILE_KEY = "file-name"
AWS_KEY = "access-key"
AWS_SECRET = "secret-key"

# -----------------------------
# Define DAG
# -----------------------------
with DAG(
    "ml_pipeline_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    # Task 1: Ingest data from S3
    ingest_task = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_from_s3,
        op_args=[BUCKET, FILE_KEY, AWS_KEY, AWS_SECRET, DATA_DIR]
    )

    # Task 2: Preprocess data
    preprocess_task = PythonOperator(
        task_id="preprocess_data",
        python_callable=preprocess,
        op_args=[os.path.join(DATA_DIR, "raw_data.csv"), DATA_DIR]
    )

    # Task 3: Train multiple models
    train_task = PythonOperator(
        task_id="train_models",
        python_callable=train_all_models,
        op_args=[os.path.join(DATA_DIR, "X_train.csv"),
                 os.path.join(DATA_DIR, "y_train.csv"),
                 MODEL_DIR]
    )

    # Task 4: Evaluate all models
    evaluate_task = PythonOperator(
        task_id="evaluate_models",
        python_callable=evaluate_all_models,
        op_args=[MODEL_DIR,
                 os.path.join(DATA_DIR, "X_test.csv"),
                 os.path.join(DATA_DIR, "y_test.csv")]
    )

    # -----------------------------
    # Task dependencies
    # -----------------------------
    ingest_task >> preprocess_task >> train_task >> evaluate_task
