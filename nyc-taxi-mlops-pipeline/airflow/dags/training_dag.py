from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from ml.train import train_model

default_args = {"owner": "airflow", "retries": 1}

def run_training():
    train_model(
        data_path="/opt/airflow/data/processed/nyc_taxi_processed.csv",
        model_path="/opt/airflow/data/models/knn_model.pkl"
    )

with DAG(
    dag_id="training_dag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["nyc-taxi", "training"],
) as dag:

    train = PythonOperator(
        task_id="train_model",
        python_callable=run_training
    )

    train
