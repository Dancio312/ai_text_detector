import re

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s\.\!\?]", "", text)
    return text.strip()


def extract_features(text: str) -> dict:
    cleaned = clean_text(text)

    words = cleaned.split()
    sentences = re.split(r"[.!?]+", cleaned)

    words = [w for w in words if w]
    sentences = [s for s in sentences if s.strip()]

    num_chars = len(cleaned)
    num_words = len(words)
    num_sentences = len(sentences)

    avg_word_length = sum(len(w) for w in words) / num_words if num_words else 0
    avg_sentence_length = num_words / num_sentences if num_sentences else 0
    lexical_diversity = len(set(words)) / num_words if num_words else 0

    return {
        "num_chars": num_chars,
        "num_words": num_words,
        "num_sentences": num_sentences,
        "avg_word_length": round(avg_word_length, 3),
        "avg_sentence_length": round(avg_sentence_length, 3),
        "lexical_diversity": round(lexical_diversity, 3)
    }
