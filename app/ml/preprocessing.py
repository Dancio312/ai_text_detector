import math
import re
from collections import Counter

STOPWORDS = {
    "the", "and", "is", "in", "to", "of", "that", "it", "on", "for", "with",
    "as", "was", "were", "be", "by", "this", "are", "from", "at"
}


def text_entropy(words):
    counts = Counter(words)
    total = len(words)
    entropy = 0.0

    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


def extract_features(text: str) -> dict:
    text_clean = text.strip()
    words = re.findall(r"\b\w+\b", text_clean.lower())
    sentences = re.split(r"[.!?]+", text_clean)

    num_chars = len(text_clean)
    num_words = len(words)
    num_sentences = max(1, len([s for s in sentences if s.strip()]))

    avg_word_length = sum(len(w) for w in words) / num_words
    avg_sentence_length = num_words / num_sentences

    lexical_diversity = len(set(words)) / num_words

    punctuation_count = len(re.findall(r"[.,;:!?]", text_clean))
    punctuation_density = punctuation_count / num_chars

    uppercase_count = sum(1 for c in text_clean if c.isupper())
    uppercase_ratio = uppercase_count / num_chars

    stopword_count = sum(1 for w in words if w in STOPWORDS)
    stopword_ratio = stopword_count / num_words

    entropy = text_entropy(words)

    return {
        "num_chars": num_chars,
        "num_words": num_words,
        "num_sentences": num_sentences,
        "avg_word_length": round(avg_word_length, 3),
        "avg_sentence_length": round(avg_sentence_length, 3),
        "lexical_diversity": round(lexical_diversity, 3),
        "punctuation_density": round(punctuation_density, 4),
        "uppercase_ratio": round(uppercase_ratio, 4),
        "stopword_ratio": round(stopword_ratio, 3),
        "entropy": round(entropy, 3),
    }
