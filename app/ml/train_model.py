import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

from app.ml.preprocessing import extract_features


def load_dataset(path: str):
    df = pd.read_csv(path)
    texts = df["text"].tolist()
    labels = df["label"].tolist()
    return texts, labels


def prepare_features(texts):
    feature_vectors = []
    for text in texts:
        features = extract_features(text)
        feature_vectors.append(list(features.values()))
    return feature_vectors


def train():
    print("Loading dataset...")
    texts, labels = load_dataset("data/training_data.csv")

    print("Extracting features...")
    X = prepare_features(texts)
    y = labels

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print("Training Logistic Regression...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Accuracy: {accuracy:.2f}")
    print(classification_report(y_test, y_pred))

    print("Saving model...")
    joblib.dump(model, "app/ml/model.joblib")

    print("Training completed.")


if __name__ == "__main__":
    train()
