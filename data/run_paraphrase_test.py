from app.experiments.paraphrase_experiment import run_experiment


texts = [
    {
        "id": 1,
        "variant": "original",
        "text": "This text has been generated to demonstrate the structured nature of language models."
    },
    {
        "id": 1,
        "variant": "paraphrase",
        "text": "The purpose of this text is to show how structured content can be produced automatically."
    },
    {
        "id": 1,
        "variant": "human_style",
        "text": "I just wrote this to show how these texts usually look, nothing special really."
    },
    {
        "id": 2,
        "variant": "original",
        "text": "Artificial intelligence systems are capable of producing coherent and well structured texts."
    },
    {
        "id": 2,
        "variant": "paraphrase",
        "text": "Modern AI tools can generate texts that are consistent and logically organized."
    }
]

if __name__ == "__main__":
    run_experiment(texts)
