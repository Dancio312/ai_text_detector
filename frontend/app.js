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
        infoMessage.innerHTML = `<i class="fa-solid fa-circle-info"></i> Text changed — previous analysis result has been cleared.`;
        infoMessage.classList.remove("hidden");
        hasResult = false;
    }

    if (words >= MIN_WORDS) {
        counter.innerHTML = `Words counter: <strong>${words}</strong> / ${MIN_WORDS} <span class="ok">✔</span>`;
        analyzeBtn.disabled = false;
    } else {
        counter.innerHTML = `Words counter: <strong>${words}</strong> / ${MIN_WORDS} <span class="bad">❌</span>`;
        analyzeBtn.disabled = true;
    }
}

function clearAll() {
    textarea.value = "";
    resultBox.innerHTML = "";
    infoMessage.classList.add("hidden");
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

    infoMessage.classList.add("hidden");
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

function renderResult(data) {
    const t = data.transformer;
    const l = data.logistic_regression;

    const finalAI = (t.ai_probability + l.ai_probability) / 2 >= 0.5;
    hasResult = true;

    resultBox.innerHTML = `
        <div class="result-card">

            <div class="model">
                <strong>Transformer</strong>
                <div class="progress">
                    <div class="progress-fill" style="width:${t.ai_probability * 100}%"></div>
                </div>
                ${(t.ai_probability * 100).toFixed(1)}%
            </div>

            <div class="model">
                <strong>Logistic Regression</strong>
                <div class="progress">
                    <div class="progress-fill" style="width:${l.ai_probability * 100}%"></div>
                </div>
                ${(l.ai_probability * 100).toFixed(1)}%
            </div>

            <div class="final">
                Final verdict: ${finalAI ? "🤖 AI Generated" : "🧑 Human Written"}
            </div>

        </div>
    `;
}
