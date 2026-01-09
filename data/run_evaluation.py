from app.evaluation.evaluator import evaluate, save_report

INPUT_CSV = "data/paraphrase_results.csv"
OUTPUT_CSV = "data/evaluation_report.csv"

if __name__ == "__main__":
    report = evaluate(INPUT_CSV)
    save_report(report, OUTPUT_CSV)
