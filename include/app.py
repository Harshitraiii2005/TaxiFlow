import pandas as pd
from taipy import Gui
from datetime import datetime

# -----------------------------
# Data storage
# -----------------------------
history = pd.DataFrame(columns=[
    "passenger_count", "pickup_longitude", "pickup_latitude",
    "dropoff_longitude", "dropoff_latitude", "pickup_hour",
    "pickup_day", "pickup_weekday", "prediction"
])

# -----------------------------
# Input fields
# -----------------------------
passenger_count = 1
pickup_datetime = "2025-09-17 10:00"
pickup_longitude = -73.985
pickup_latitude = 40.758
dropoff_longitude = -73.985
dropoff_latitude = 40.768
prediction = None


# -----------------------------
# Prediction function (Dummy)
# Replace this with ML model predict()
# -----------------------------
def predict_trip():
    global prediction, history

    dt = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M")
    pickup_hour = dt.hour
    pickup_day = dt.day
    pickup_weekday = dt.weekday()

    # Dummy formula: Manhattan distance * 4 minutes
    distance = abs(dropoff_latitude - pickup_latitude) + abs(dropoff_longitude - pickup_longitude)
    prediction = round(distance * 400, 2)  # ~ minutes

    # Add to history
    new_row = {
        "passenger_count": passenger_count,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "pickup_hour": pickup_hour,
        "pickup_day": pickup_day,
        "pickup_weekday": pickup_weekday,
        "prediction": f"{prediction} min"
    }
    history = pd.concat([history, pd.DataFrame([new_row])], ignore_index=True)


# -----------------------------
# UI Layout
# -----------------------------
page = """
# 🚕 NYC Taxi Trip Duration Predictor

### Enter Trip Details
Passenger Count: <|{passenger_count}|input|number|min=1|max=6|>
Pickup Datetime: <|{pickup_datetime}|input|datetime|>

Pickup Longitude: <|{pickup_longitude}|input|number|>
Pickup Latitude: <|{pickup_latitude}|input|number|>

Dropoff Longitude: <|{dropoff_longitude}|input|number|>
Dropoff Latitude: <|{dropoff_latitude}|input|number|>

<|Predict|button|on_action=predict_trip|>

---

### 📊 Prediction History
<|{history}|table|page_size=5|filter=True|sort=True|>
"""

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    Gui(page).run(title="NYC Taxi Predictor", port=5000)
