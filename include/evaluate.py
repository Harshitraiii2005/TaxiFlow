import pandas as pd
import joblib
import os
from sklearn.metrics import r2_score

def evaluate_all_models(model_dir, X_test_path, y_test_path):
    """Evaluate all saved models and print R2 scores."""
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path)
    results = {}

    for file in os.listdir(model_dir):
        if file.endswith(".joblib"):
            model_path = os.path.join(model_dir, file)
            model = joblib.load(model_path)
            y_pred = model.predict(X_test)
            score = r2_score(y_test, y_pred)
            results[file.split(".")[0]] = score
            print(f"Model {file} R2: {score:.4f}")

    return results
