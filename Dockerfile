FROM astrocrpublic.azurecr.io/runtime:3.0-10

WORKDIR /include

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs and include folder
COPY dags /include/dags
COPY include /include/include

# Copy custom entrypoint
COPY include/entrypoint.sh /entrypoint-custom.sh
RUN chmod +x /entrypoint-custom.sh

# Override entrypoint to run Airflow + Flask + StatsD
ENTRYPOINT ["/entrypoint-custom.sh"]

# Expose Airflow webserver and metrics
EXPOSE 8080 9102
