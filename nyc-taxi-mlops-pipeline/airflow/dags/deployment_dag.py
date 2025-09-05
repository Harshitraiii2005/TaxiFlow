from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"owner": "airflow", "retries": 1}

with DAG(
    dag_id="deployment_dag",
    default_args=default_args,
    schedule_interval=None,  # manual trigger
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["nyc-taxi", "deployment"],
) as dag:

    build_flask_docker = BashOperator(
        task_id="build_flask_docker",
        bash_command="docker build -t nyc-taxi-flask ./flask_app"
    )

    push_flask_docker = BashOperator(
        task_id="push_flask_docker",
        bash_command="docker tag nyc-taxi-flask your-dockerhub/nyc-taxi-flask:latest && docker push your-dockerhub/nyc-taxi-flask:latest"
    )

    build_flask_docker >> push_flask_docker
