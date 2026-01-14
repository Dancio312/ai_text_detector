# -*- coding: utf-8 -*-

import csv
import requests

API_URL = "http://127.0.0.1:8000/analyze"
OUTPUT_FILE = "app/experiments/stability_results.csv"

texts = {
    "original": (
        "The question of how to make AI robust and beneficial is the most important "
        "conversation of our century. We need to shift from reactive to proactive mode."
    ),
    "paraphrase": (
        "Ensuring that artificial intelligence remains safe and useful is one of the key "
        "challenges of our time. Society must move from reactive responses to long-term planning."
    ),
    "shortened": (
        "Making artificial intelligence safe and beneficial requires long-term thinking "
        "and carefully designed proactive development strategies."
    ),
    "simplified": (
        "Artificial intelligence should be developed carefully so that it supports people "
        "and provides long-term benefits for society without unnecessary risks."
    ),
}

fieldnames = [
    "variant",
    "lr_probability",
    "transformer_probability",
    "weighted_score",
    "verdict",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for variant, text in texts.items():
        response = requests.post(
            API_URL,
            json={"text": text},
            timeout=30,
        )

        data = response.json()

        # === SAFETY CHECK (VERY IMPORTANT) ===
        if "logistic_regression" not in data:
            print(f"Skipping '{variant}' - validation error from API:")
            print(data)
            continue

        writer.writerow({
            "variant": variant,
            "lr_probability": data["logistic_regression"]["ai_probability"],
            "transformer_probability": data["transformer"]["ai_probability"],
            "weighted_score": data["verdict"].get("weighted_score", ""),
            "verdict": data["verdict"]["label"],
        })

print("Stability experiment completed. Results saved to CSV.")
