import pandas as pd
from sklearn.model_selection import train_test_split
import os

def preprocess(raw_path: str, save_dir: str) -> str:
    """Preprocess data and save train/test CSVs."""
    os.makedirs(save_dir, exist_ok=True)
    df = pd.read_csv(raw_path)

    # Drop missing values
    df = df.dropna()

    # Convert datetime
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])

    # Feature engineering
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_day'] = df['pickup_datetime'].dt.day
    df['pickup_weekday'] = df['pickup_datetime'].dt.weekday
    df['trip_time_diff'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds()

    # Drop unnecessary columns
    drop_cols = ['id', 'pickup_datetime', 'dropoff_datetime', 'store_and_fwd_flag']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    # Split features and target
    X = df.drop('trip_duration', axis=1)
    y = df['trip_duration']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Save CSVs
    X_train.to_csv(os.path.join(save_dir, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(save_dir, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(save_dir, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(save_dir, "y_test.csv"), index=False)

    print(f"Preprocessed data saved in {save_dir}")
    return save_dir
