from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from ml.preprocessing import preprocess_data

default_args = {"owner": "airflow", "retries": 1}

def run_preprocessing():
    preprocess_data(
        input_path="/opt/airflow/data/raw/nyc_taxi.csv",
        output_path="/opt/airflow/data/processed/nyc_taxi_processed.csv"
    )

with DAG(
    dag_id="preprocessing_dag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["nyc-taxi", "preprocessing"],
) as dag:

    preprocess = PythonOperator(
        task_id="preprocess_task",
        python_callable=run_preprocessing
    )

    preprocess
