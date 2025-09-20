set -e


exec gunicorn -b 0.0.0.0:5055 app:app
