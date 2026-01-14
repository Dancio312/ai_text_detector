import csv
from pathlib import Path
from datetime import datetime


CSV_PATH = Path("data/analysis_results.csv")


def log_analysis(
    text: str,
    lr_result: dict,
    transformer_result: dict,
    final_decision: dict
):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = CSV_PATH.exists()

    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "text_length_words",
                "lr_label",
                "lr_probability",
                "transformer_label",
                "transformer_probability",
                "final_label",
                "confidence",
                "weighted_score"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            len(text.split()),
            lr_result["label"],
            lr_result["ai_probability"],
            transformer_result["label"],
            transformer_result["ai_probability"],
            final_decision["final_label"],
            final_decision["confidence"],
            final_decision["weighted_score"]
        ])
