async function analyze() {
    const text = document.getElementById("text").value.trim();
    const resultBox = document.getElementById("result");

    if (text.length < 50) {
        showError("Text is too short (minimum 50 characters).");
        return;
    }

    resultBox.textContent = "Analyzing...";
    resultBox.className = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            showError("Validation error from API.");
            return;
        }

        displayResult(data);

    } catch (err) {
        showError("Cannot connect to backend.");
    }
}

function displayResult(data) {
    const transformer = data.transformer;
    const logistic = data.logistic_regression;
    const resultBox = document.getElementById("result");

    const labelText = transformer.label === "AI"
        ? "AI GENERATED TEXT"
        : "HUMAN WRITTEN TEXT";

    resultBox.className = transformer.label === "AI" ? "ai" : "human";

    resultBox.innerHTML = `
        <h3>${labelText}</h3>
        <p><strong>Transformer confidence:</strong>
           ${(transformer.ai_probability * 100).toFixed(2)}%
        </p>
        <hr>
        <p><strong>Logistic Regression:</strong>
           ${logistic.label}
           (${(logistic.ai_probability * 100).toFixed(2)}%)
        </p>
    `;
}

function showError(message) {
    const resultBox = document.getElementById("result");
    resultBox.textContent = message;
    resultBox.className = "error";
}
