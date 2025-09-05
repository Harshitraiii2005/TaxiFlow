from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier

def get_model():
    # You can tune n_neighbors as needed
    return KNeighborsClassifier(n_neighbors=5)

def train_model(preprocessor, model, X_train, y_train):
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    pipeline.fit(X_train, y_train)
    return pipeline
