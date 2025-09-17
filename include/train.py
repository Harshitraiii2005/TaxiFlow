import pandas as pd
import joblib
import os
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def train_all_models(X_path, y_path, save_dir):
    """Train KNN, Linear Regression, RandomForest and save models."""
    os.makedirs(save_dir, exist_ok=True)
    X_train = pd.read_csv(X_path)
    y_train = pd.read_csv(y_path).values.ravel()

    models_to_train = {
        "knn": KNeighborsRegressor(),
        "linear": LinearRegression(),
        "rf": RandomForestRegressor(n_estimators=100, random_state=42)
    }

    for name, model in models_to_train.items():
        model.fit(X_train, y_train)
        joblib.dump(model, os.path.join(save_dir, f"{name}.joblib"))
        print(f"Model {name} saved at {save_dir}")
