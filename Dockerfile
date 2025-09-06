# Base Image: Python
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy full project into container
COPY . .

# Expose ports
EXPOSE 8080  
EXPOSE 5000   

# Default command: run Flask + Airflow webserver
CMD bash -c "airflow db init && \
             airflow webserver -p 8080 & \
             airflow scheduler & \
             python flask_app/app.py"
