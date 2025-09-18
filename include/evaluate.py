import pandas as pd
import joblib
import os
from sklearn.metrics import r2_score

def evaluate_and_save_best_model(model_dir, X_test_path, y_test_path):
    """Evaluate all models, pick the best, and save it as best_model.joblib."""
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path)
    results = {}

    best_score = float("-inf")
    best_model = None
    best_model_name = None

    for file in os.listdir(model_dir):
        if file.endswith(".joblib"):
            model_path = os.path.join(model_dir, file)
            model = joblib.load(model_path)
            y_pred = model.predict(X_test)
            score = r2_score(y_test, y_pred)
            results[file.split(".")[0]] = score
            print(f"Model {file} R2: {score:.4f}")

            # Track best model
            if score > best_score:
                best_score = score
                best_model = model
                best_model_name = file

    # Save best model
    if best_model is not None:
        best_model_path = os.path.join(model_dir, "best_model.joblib")
        joblib.dump(best_model, best_model_path)
        print(f"\nBest model saved as {best_model_path} with R2 = {best_score:.4f}")

    return results, best_model_name, best_score
