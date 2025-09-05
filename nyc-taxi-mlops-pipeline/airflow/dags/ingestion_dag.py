from airflow import DAG
from airflow.providers.amazon.aws.transfers.s3_to_local import S3ToLocalOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="ingestion_dag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["nyc-taxi", "ingestion"],
) as dag:

    download_from_s3 = S3ToLocalOperator(
        task_id="download_raw_data",
        bucket_name="nyc-taxi-bucket",
        prefix="raw/nyc_taxi.csv",
        dest="/opt/airflow/data/raw/nyc_taxi.csv",
        aws_conn_id="aws_default"
    )

    download_from_s3
