const textarea = document.getElementById("text");
const counter = document.getElementById("wordCounter");
const analyzeBtn = document.getElementById("analyzeBtn");

const resultContainer = document.getElementById("result");
const verdictSection = document.getElementById("verdictSection");
const detailsSection = document.getElementById("detailsSection");
const systemSection = document.getElementById("systemSection");

const infoMessage = document.getElementById("infoMessage");

const MIN_WORDS = 20;
let hasResult = false;

textarea.addEventListener("input", updateCounter);

function updateCounter() {
    const words = textarea.value.trim().split(/\s+/).filter(Boolean).length;

    if (hasResult) {
        verdictSection.innerHTML = "";
        detailsSection.innerHTML = "";
        systemSection.innerHTML = "";
        infoMessage.textContent = "Text changed — previous result has been cleared.";
        infoMessage.style.display = "block";
        hasResult = false;
    }

    counter.innerHTML = `Words: ${words} / ${MIN_WORDS}`;
    analyzeBtn.disabled = words < MIN_WORDS;
}

function clearAll() {
    textarea.value = "";
    verdictSection.innerHTML = "";
    detailsSection.innerHTML = "";
    systemSection.innerHTML = "";
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

    verdictSection.innerHTML = "<div class='result-card'>Analyzing...</div>";
    detailsSection.innerHTML = "";
    systemSection.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        renderResult(data);

    } catch {
        verdictSection.innerHTML =
            "<div class='result-card'>Cannot connect to backend.</div>";
    }
}

function animateProgress(bar, targetPercent, duration = 1200) {
    let start = null;

    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        bar.style.width = (progress * targetPercent) + "%";

        if (progress < 1) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
}

function renderResult(data) {
    const transformer = data.transformer;
    const logistic = data.logistic_regression;
    const verdict = data.verdict;

    hasResult = true;

    // === VERDICT ===
    let verdictTitle;
    if (verdict.label === "AI") {
        verdictTitle = "🤖 AI Generated Text";
    } else if (verdict.label === "human" || verdict.label === "HUMAN") {
        verdictTitle = "🧑 Human Written Text";
    } else {
        verdictTitle = "⚖️ Inconclusive Result";
    }

    verdictSection.innerHTML = `
        <div class="result-card final">
            <strong style="font-size: 18px;">${verdictTitle}</strong>
            <p style="margin-top: 8px; font-size: 14px; color: #cbd5f5;">
                ${verdict.explanation || "The system could not confidently classify the text."}
            </p>
        </div>
    `;

    // === DETAILS ===
    detailsSection.innerHTML = `
        <div class="result-card">

            <div class="model">
                <strong>Transformer model</strong>
                <div class="progress">
                    <div class="progress-fill" id="bar-transformer"></div>
                </div>
                ${(transformer.ai_probability * 100).toFixed(1)}%
            </div>

            <div class="model">
                <strong>Logistic Regression</strong>
                <div class="progress">
                    <div class="progress-fill" id="bar-logistic"></div>
                </div>
                ${(logistic.ai_probability * 100).toFixed(1)}%
            </div>

        </div>
    `;

    // === SYSTEM INFO ===
    systemSection.innerHTML = `
        <p style="margin-top: 14px; font-size: 12px; color: #94a3b8; text-align: center;">
            Final decision based on ensemble analysis of multiple models.
        </p>
    `;

    animateProgress(
        document.getElementById("bar-transformer"),
        transformer.ai_probability * 100
    );
    animateProgress(
        document.getElementById("bar-logistic"),
        logistic.ai_probability * 100
    );
}
