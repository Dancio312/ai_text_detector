import csv
from datetime import datetime
from pathlib import Path

from app.services.analysis_service import analyze_text


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
OUTPUT_PATH = DATA_DIR / "paraphrase_results.csv"


def run_experiment(texts: list[dict]):
    DATA_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "text_id",
            "variant",
            "lr_probability",
            "lr_label",
            "transformer_probability",
            "transformer_label",
            "avg_sentence_length",
            "lexical_diversity",
            "timestamp"
        ])

        for item in texts:
            result = analyze_text(item["text"])

            writer.writerow([
                item["id"],
                item["variant"],
                result["logistic_regression"]["ai_probability"],
                result["logistic_regression"]["label"],
                result["transformer"]["ai_probability"],
                result["transformer"]["label"],
                result["features"]["avg_sentence_length"],
                result["features"]["lexical_diversity"],
                datetime.now().isoformat()
            ])

    print(f"Experiment finished. Results saved to {OUTPUT_PATH}")
