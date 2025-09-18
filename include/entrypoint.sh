#!/bin/bash
set -e

# Start StatsD exporter for Prometheus
statsd_exporter --statsd.listen-udp=:8125 --web.listen-address=:9102 &

# Start Flask app in background
python3 /include/include/app.py &

# Finally, run the default Astro Airflow entrypoint
exec /entrypoint "$@"
