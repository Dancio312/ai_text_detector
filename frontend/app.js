const textarea = document.getElementById("text");
const resultBox = document.getElementById("result");
const loader = document.getElementById("loader");
const counter = document.getElementById("counter");
const button = document.getElementById("analyzeBtn");

const MIN_WORDS = 20;

/* === live word counter === */
textarea.addEventListener("input", () => {
    const words = textarea.value.trim().split(/\s+/).filter(Boolean).length;
    counter.textContent = `${words} words`;
});

async function analyze() {
    const text = textarea.value.trim();
    const wordCount = text.split(/\s+/).filter(Boolean).length;

    resultBox.className = "";
    resultBox.textContent = "";

    if (wordCount < MIN_WORDS) {
        showError(`Text is too short (minimum ${MIN_WORDS} words).`);
        return;
    }

    loader.classList.remove("hidden");
    button.disabled = true;
    resultBox.textContent = "Analyzing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || "Validation error from API.");
            return;
        }

        displayResult(data);

    } catch (error) {
        console.error(error);
        showError("Cannot connect to backend.");
    } finally {
        loader.classList.add("hidden");
        button.disabled = false;
    }
}

function displayResult(data) {
    const transformer = data.transformer;
    const logistic = data.logistic_regression;

    const isAI = transformer.label === "AI";

    resultBox.className = isAI ? "ai" : "human";

    resultBox.innerHTML = `
        <h3>${isAI ? "AI GENERATED TEXT" : "HUMAN WRITTEN TEXT"}</h3>

        <p>
            <strong>Transformer model:</strong><br>
            Confidence: ${(transformer.ai_probability * 100).toFixed(2)}%
        </p>

        <hr>

        <p>
            <strong>Logistic Regression:</strong><br>
            Label: ${logistic.label}<br>
            Confidence: ${(logistic.ai_probability * 100).toFixed(2)}%
        </p>
    `;
}

function showError(message) {
    resultBox.textContent = message;
    resultBox.className = "error";
}
