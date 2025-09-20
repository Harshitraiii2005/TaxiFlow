from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'include'))

from include.ingestion import ingest_from_s3
from include.preprocessing import preprocess
from include.train import train_all_models
from include.evaluate import evaluate_and_save_best_model


DATA_DIR = "/tmp/airflow_data"
MODEL_DIR = os.path.join(DATA_DIR, "models")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
APP_PATH = os.path.join(os.path.dirname(__file__), "..", "include", "app.py")

BUCKET = "your-bucket-name"
FILE_KEY = "nyc_taxi_trip_duration.csv"
AWS_KEY = "your-aws-access-key"
AWS_SECRET = "your-aws-secret-key"


with DAG(
    "ml_pipeline_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_from_s3,
        op_args=[BUCKET, FILE_KEY, AWS_KEY, AWS_SECRET, DATA_DIR]
    )

    preprocess_task = PythonOperator(
        task_id="preprocess_data",
        python_callable=preprocess,
        op_args=[os.path.join(DATA_DIR, "raw_data.csv"), DATA_DIR]
    )

    train_task = PythonOperator(
        task_id="train_models",
        python_callable=train_all_models,
        op_args=[
            os.path.join(DATA_DIR, "X_train.csv"),
            os.path.join(DATA_DIR, "y_train.csv"),
            MODEL_DIR
        ]
    )

    evaluate_task = PythonOperator(
        task_id="evaluate_models",
        python_callable=evaluate_and_save_best_model,
        op_args=[
            MODEL_DIR,
            os.path.join(DATA_DIR, "X_test.csv"),
            os.path.join(DATA_DIR, "y_test.csv")
        ]
    )

    
    trigger_app = BashOperator(
        task_id="trigger_app",
        bash_command=f"""
        if [ -f /tmp/flask.pid ] && kill -0 $(cat /tmp/flask.pid) 2>/dev/null; then
            echo "Flask app already running with PID $(cat /tmp/flask.pid)";
        else
            setsid python3 {APP_PATH} > /tmp/flask.log 2>&1 < /dev/null &
            echo $! > /tmp/flask.pid
            echo "Flask app started with PID $(cat /tmp/flask.pid)"
        fi
        """,
    )

   
    ingest_task >> preprocess_task >> train_task >> evaluate_task >> trigger_app
