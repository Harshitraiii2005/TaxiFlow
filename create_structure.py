import os

# Define project structure as a dictionary
project_structure = {
    "nyc-taxi-mlops-pipeline": {
        "airflow": {
            "dags": {
                "ingestion_dag.py": "",
                "preprocessing_dag.py": "",
                "training_dag.py": "",
                "deployment_dag.py": ""
            },
            "plugins": {
                "custom_operators.py": ""
            },
            "docker-compose.yml": "",
            "requirements.txt": ""
        },
        "data": {
            "raw": {},
            "processed": {},
            "models": {}
        },
        "ml": {
            "preprocessing.py": "",
            "train.py": "",
            "evaluate.py": "",
            "utils.py": ""
        },
        "flask_app": {
            "app.py": "",
            "Dockerfile": "",
            "requirements.txt": ""
        },
        "k8s": {
            "deployment.yaml": "",
            "service.yaml": "",
            "ingress.yaml": ""
        },
        "monitoring": {
            "prometheus.yml": "",
            "grafana-dashboard.json": "",
            "alerts.yml": ""
        },
        "cicd": {
            "github-actions.yml": "",
            "docker-build.sh": ""
        },
        "docker": {
            "airflow.Dockerfile": "",
            "ml.Dockerfile": "",
            "base.Dockerfile": ""
        },
        "scripts": {
            "upload_to_s3.sh": "",
            "run_local.sh": ""
        },
        ".gitignore": "",
        "README.md": "# NYC Taxi MLOps Pipeline\n\nEnd-to-end MLOps project with Airflow, Flask, Docker, K8s, and Monitoring.",
        "LICENSE": ""
    }
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)


if __name__ == "__main__":
    base_dir = os.getcwd()
    create_structure(base_dir, project_structure)
    print("✅ NYC Taxi MLOps pipeline project structure created successfully!")
