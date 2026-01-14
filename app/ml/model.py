import joblib

MODEL_PATH = "app/ml/model.joblib"
_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model
