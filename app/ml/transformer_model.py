from transformers import pipeline

_transformer = None


def load_transformer():
    global _transformer
    if _transformer is None:
        _transformer = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1
        )
    return _transformer
