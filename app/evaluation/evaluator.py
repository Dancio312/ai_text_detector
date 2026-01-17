import csv
from pathlib import Path
from collections import Counter

from app.core.config import EVALUATION_COLUMNS, MODEL_NAMES


def evaluate(csv_path: str):
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    required_columns = set(EVALUATION_COLUMNS)

    results = {
        "logistic_regression": [],
        "transformer": []
    }

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # === CSV Schema Validation ===
        missing = required_columns - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns in CSV: {missing}")

        for row in reader:
            results["logistic_regression"].append(row["lr_label"])
            results["transformer"].append(row["transformer_label"])

    report = {}

    for model_key, labels in results.items():
        counter = Counter(labels)
        total = sum(counter.values())

        report[model_key] = {
            "model_name": MODEL_NAMES[model_key],
            "total_samples": total,
            "ai_predictions": counter.get("AI", 0),
            "human_predictions": counter.get("human", 0)
        }

    return report


def save_report(report: dict, output_path: str):
    output_path = Path(output_path)

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "model",
            "total_samples",
            "ai_predictions",
            "human_predictions"
        ])

        for model in report.values():
            writer.writerow([
                model["model_name"],
                model["total_samples"],
                model["ai_predictions"],
                model["human_predictions"]
            ])

    print(f"Evaluation report saved to {output_path.resolve()}")
