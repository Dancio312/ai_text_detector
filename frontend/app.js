const textarea = document.getElementById("text");
const counter = document.getElementById("wordCounter");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultBox = document.getElementById("result");
const infoMessage = document.getElementById("infoMessage");

const MIN_WORDS = 20;
let hasResult = false;

textarea.addEventListener("input", updateCounter);

function updateCounter() {
    const words = textarea.value.trim().split(/\s+/).filter(Boolean).length;

    if (hasResult) {
        resultBox.innerHTML = "";
        infoMessage.textContent = "Text changed — previous result has been cleared.";
        infoMessage.style.display = "block";
        hasResult = false;
    }

    counter.innerHTML = `Words: ${words} / ${MIN_WORDS}`;
    analyzeBtn.disabled = words < MIN_WORDS;
}

function clearAll() {
    textarea.value = "";
    resultBox.innerHTML = "";
    infoMessage.style.display = "none";
    analyzeBtn.disabled = true;
    hasResult = false;
    updateCounter();
}

function generateExample() {
    textarea.value =
        "Artificial intelligence has rapidly evolved in recent years, transforming the way people interact with technology. " +
        "Modern AI systems can analyze data, understand language, and generate human-like text with impressive accuracy.";

    textarea.dispatchEvent(new Event("input"));
}

async function analyze() {
    const text = textarea.value.trim();
    if (text.split(/\s+/).length < MIN_WORDS) return;

    infoMessage.style.display = "none";
    resultBox.innerHTML = "<div class='result-card'>Analyzing...</div>";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        renderResult(data);

    } catch {
        resultBox.innerHTML =
            "<div class='result-card'>Cannot connect to backend.</div>";
    }
}

function animateProgress(bar, targetPercent, duration = 1200) {
    let start = null;

    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        bar.style.width = (progress * targetPercent) + "%";

        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}

function renderResult(data) {
    const t = data.transformer;
    const l = data.logistic_regression;
    const v = data.verdict;

    hasResult = true;

    let verdictLabel;
    if (v.label === "AI") {
        verdictLabel = "🤖 AI Generated Text";
    } else if (v.label === "HUMAN") {
        verdictLabel = "🧑 Human Written Text";
    } else {
        verdictLabel = "⚖️ Inconclusive Result";
    }

    resultBox.innerHTML = `
        <div class="result-card">

            <div class="model">
                <strong>Transformer</strong>
                <div class="progress">
                    <div class="progress-fill" id="bar-transformer"></div>
                </div>
                ${(t.ai_probability * 100).toFixed(1)}%
            </div>

            <div class="model">
                <strong>Logistic Regression</strong>
                <div class="progress">
                    <div class="progress-fill" id="bar-logistic"></div>
                </div>
                ${(l.ai_probability * 100).toFixed(1)}%
            </div>

            <div class="final">
                <strong>${verdictLabel}</strong>
                <p style="margin-top: 10px; font-size: 14px; color: #cbd5f5;">
                    ${v.explanation || "The system could not confidently classify the text."}
                </p>
            </div>

        </div>
    `;

    animateProgress(
        document.getElementById("bar-transformer"),
        t.ai_probability * 100
    );
    animateProgress(
        document.getElementById("bar-logistic"),
        l.ai_probability * 100
    );
}
