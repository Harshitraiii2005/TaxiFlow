#FROM astrocrpublic.azurecr.io/runtime:3.0-10 -> run this if you want to use astro image with airflow

# Use Python slim image for building the docker image 
FROM python:3.12-slim 

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Flask app
COPY include/app.py /app/

# Expose the port your app runs on
EXPOSE 5055

# Start the app
CMD ["python3", "app.py"]
