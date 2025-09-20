from flask import Flask, render_template_string, request
import pandas as pd
from datetime import datetime
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# -----------------------------
# Data storage
# -----------------------------
history = pd.DataFrame(columns=[
    "passenger_count", "pickup_longitude", "pickup_latitude",
    "dropoff_longitude", "dropoff_latitude", "pickup_hour",
    "pickup_day", "pickup_weekday", "prediction"
])

# -----------------------------
# Prometheus metrics
# -----------------------------
prediction_counter = Counter('prediction_requests_total', 'Total number of predictions')

# -----------------------------
# HTML Template with Bootstrap
# -----------------------------
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>NYC Taxi Duration Predictor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="text-center mb-4">
            <h1 class="display-5">🚖 NYC Taxi Trip Duration Predictor</h1>
            <p class="lead">Enter trip details to predict duration</p>
        </div>

        <div class="card shadow-sm p-4 mb-4">
            <form method="post">
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label class="form-label">Passenger Count</label>
                        <input type="number" class="form-control" name="passenger_count" value="{{ passenger_count }}" min="1">
                    </div>
                    <div class="col-md-8">
                        <label class="form-label">Pickup Datetime</label>
                        <input type="datetime-local" class="form-control" name="pickup_datetime" value="{{ pickup_datetime }}">
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="form-label">Pickup Longitude</label>
                        <input type="text" class="form-control" name="pickup_longitude" value="{{ pickup_longitude }}">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Pickup Latitude</label>
                        <input type="text" class="form-control" name="pickup_latitude" value="{{ pickup_latitude }}">
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="form-label">Dropoff Longitude</label>
                        <input type="text" class="form-control" name="dropoff_longitude" value="{{ dropoff_longitude }}">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Dropoff Latitude</label>
                        <input type="text" class="form-control" name="dropoff_latitude" value="{{ dropoff_latitude }}">
                    </div>
                </div>
                <div class="text-center">
                    <button type="submit" class="btn btn-primary btn-lg">Predict</button>
                </div>
            </form>
        </div>

        {% if prediction %}
        <div class="alert alert-success text-center" role="alert">
            <h4 class="alert-heading">Predicted Duration: {{ prediction }} minutes ⏱️</h4>
        </div>
        {% endif %}

        <h2 class="mb-3">Prediction History</h2>
        <div class="table-responsive">
            <table class="table table-striped table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th>Passenger</th><th>Pickup Lon</th><th>Pickup Lat</th>
                        <th>Dropoff Lon</th><th>Dropoff Lat</th><th>Hour</th>
                        <th>Day</th><th>Weekday</th><th>Prediction</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in history.itertuples() %}
                    <tr>
                        <td>{{ row.passenger_count }}</td>
                        <td>{{ row.pickup_longitude }}</td>
                        <td>{{ row.pickup_latitude }}</td>
                        <td>{{ row.dropoff_longitude }}</td>
                        <td>{{ row.dropoff_latitude }}</td>
                        <td>{{ row.pickup_hour }}</td>
                        <td>{{ row.pickup_day }}</td>
                        <td>{{ row.pickup_weekday }}</td>
                        <td>{{ row.prediction }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    global history
    prediction = None

    # Default input values
    passenger_count = 1
    pickup_datetime = "2025-09-17T10:00"
    pickup_longitude = -73.985
    pickup_latitude = 40.758
    dropoff_longitude = -73.985
    dropoff_latitude = 40.768

    if request.method == "POST":
        prediction_counter.inc()

        passenger_count = int(request.form["passenger_count"])
        pickup_datetime = request.form["pickup_datetime"]
        pickup_longitude = float(request.form["pickup_longitude"])
        pickup_latitude = float(request.form["pickup_latitude"])
        dropoff_longitude = float(request.form["dropoff_longitude"])
        dropoff_latitude = float(request.form["dropoff_latitude"])

        dt = datetime.strptime(pickup_datetime, "%Y-%m-%dT%H:%M")
        pickup_hour = dt.hour
        pickup_day = dt.day
        pickup_weekday = dt.weekday()

        distance = abs(dropoff_latitude - pickup_latitude) + abs(dropoff_longitude - pickup_longitude)
        prediction = round(distance * 400, 2)

        new_row = pd.DataFrame([{
            "passenger_count": passenger_count,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "pickup_hour": pickup_hour,
            "pickup_day": pickup_day,
            "pickup_weekday": pickup_weekday,
            "prediction": prediction
        }])

        history = pd.concat([history, new_row], ignore_index=True)

    return render_template_string(
        HTML,
        passenger_count=passenger_count,
        pickup_datetime=pickup_datetime,
        pickup_longitude=pickup_longitude,
        pickup_latitude=pickup_latitude,
        dropoff_longitude=dropoff_longitude,
        dropoff_latitude=dropoff_latitude,
        prediction=prediction,
        history=history
    )

# -----------------------------
# Metrics endpoint
# -----------------------------
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=True)
