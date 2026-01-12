async function analyze() {
    const textarea = document.getElementById("text");
    const resultBox = document.getElementById("result");

    const text = textarea.value.trim();

    // === Frontend validation (consistent with backend) ===
    const wordCount = text.split(/\s+/).filter(Boolean).length;
    const MIN_WORDS = 20;

    if (wordCount < MIN_WORDS) {
        showError(`Text is too short (minimum ${MIN_WORDS} words).`);
        return;
    }

    resultBox.textContent = "Analyzing...";
    resultBox.className = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        // === Backend validation error ===
        if (!response.ok) {
            showError(data.error || "Validation error from API.");
            return;
        }

        displayResult(data);

    } catch (error) {
        console.error(error);
        showError("Cannot connect to backend.");
    }
}

function displayResult(data) {
    const resultBox = document.getElementById("result");

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
    const resultBox = document.getElementById("result");
    resultBox.textContent = message;
    resultBox.className = "error";
}
