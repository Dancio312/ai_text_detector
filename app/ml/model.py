import joblib

MODEL_PATH = "app/ml/model.joblib"

_model = None


def load_model():
    print("Loading trained Logistic Regression model")
    return joblib.load("app/ml/model.joblib")

