def explain_lr(features: dict, model, top_k: int = 3) -> dict:
    """
    Returns top contributing features for Logistic Regression.
    """
    coef = model.coef_[0]
    feature_names = list(features.keys())
    feature_values = list(features.values())

    contributions = []
    for name, value, weight in zip(feature_names, feature_values, coef):
        contributions.append({
            "feature": name,
            "value": round(float(value), 3),
            "weight": round(float(weight), 3),
            "impact": round(float(value * weight), 3),
        })

    contributions.sort(key=lambda x: abs(x["impact"]), reverse=True)

    positives = [c for c in contributions if c["impact"] > 0][:top_k]
    negatives = [c for c in contributions if c["impact"] < 0][:top_k]

    return {
        "model_type": "logistic_regression",
        "top_positive_features": positives,
        "top_negative_features": negatives,
        "note": "Explainability based on linear model feature weights"
    }
