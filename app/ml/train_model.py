import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from app.ml.preprocessing import extract_features

DATA_PATH = "data/dataset.csv"
MODEL_PATH = "app/ml/model.joblib"


def prepare_dataset():
    df = pd.read_csv(DATA_PATH)

    X = []
    y = []

    for _, row in df.iterrows():
        features = extract_features(row["text"])
        X.append(list(features.values()))
        y.append(1 if row["label"] == "ai" else 0)

    return X, y


def train():
    X, y = prepare_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1:", f1_score(y_test, y_pred))

    joblib.dump(model, MODEL_PATH)
    print("Model saved to", MODEL_PATH)


if __name__ == "__main__":
    train()
