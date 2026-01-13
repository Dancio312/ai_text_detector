const textarea = document.getElementById("text");
const counter = document.getElementById("wordCounter");
const status = document.getElementById("status");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultBox = document.getElementById("result");

const MIN_WORDS = 20;

textarea.addEventListener("input", updateCounter);

function updateCounter() {
    const words = textarea.value.trim().split(/\s+/).filter(Boolean).length;
    counter.textContent = `Words: ${words} / ${MIN_WORDS}`;

    if (words >= MIN_WORDS) {
        status.textContent = "Ready";
        status.className = "valid";
        analyzeBtn.disabled = false;
    } else {
        status.textContent = "Too short";
        status.className = "invalid";
        analyzeBtn.disabled = true;
    }
}

async function analyze() {
    const text = textarea.value.trim();
    resultBox.textContent = "Analyzing...";
    resultBox.className = "result-box";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        if (!response.ok) {
            showError(data.error || "API error");
            return;
        }

        displayResult(data);
    } catch {
        showError("Cannot connect to backend.");
    }
}

function displayResult(data) {
    const t = data.transformer;
    const l = data.logistic_regression;

    const tConf = Math.round(t.ai_probability * 100);
    const lConf = Math.round(l.ai_probability * 100);

    resultBox.innerHTML = `
        <h3 style="margin-bottom:10px;">Model comparison</h3>

        <div class="model-grid">
            <div class="model-card">
                <div class="model-title">Transformer (DistilBERT)</div>
                <div class="progress-container">
                    <div class="progress-label">
                        ${t.label} – ${tConf}%
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill ${t.label === "AI" ? "progress-ai" : "progress-human"}"
                             style="--value:${tConf}%"></div>
                    </div>
                </div>
            </div>

            <div class="model-card">
                <div class="model-title">Logistic Regression</div>
                <div class="progress-container">
                    <div class="progress-label">
                        ${l.label} – ${lConf}%
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill ${l.label === "AI" ? "progress-ai" : "progress-human"}"
                             style="--value:${lConf}%"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function showError(msg) {
    resultBox.textContent = msg;
}

function clearAll() {
    textarea.value = "";
    resultBox.textContent = "Ready to analyze. Enter text and click Analyze.";
    updateCounter();
}

function generateSample() {
    textarea.value =
        "Artificial intelligence systems are increasingly used to generate text that closely resembles human writing. These systems are trained on large datasets and learn complex language patterns.";
    updateCounter();
}
