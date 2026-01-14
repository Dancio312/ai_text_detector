const textarea = document.getElementById("text");
const counter = document.getElementById("wordCounter");
const analyzeBtn = document.getElementById("analyzeBtn");
const explainabilitySection = document.getElementById("explainabilitySection");

const verdictSection = document.getElementById("verdictSection");
const detailsSection = document.getElementById("detailsSection");
const systemSection = document.getElementById("systemSection");
const infoMessage = document.getElementById("infoMessage");

const MIN_WORDS = 20;
let hasResult = false;

textarea.addEventListener("input", updateCounter);

/* =========================
   INPUT / COUNTER
========================= */

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

    counter.textContent = `Words: ${words} / ${MIN_WORDS}`;
    analyzeBtn.disabled = words < MIN_WORDS;
}

function clearAll() {
    textarea.value = "";
    verdictSection.innerHTML = "";
    detailsSection.innerHTML = "";
    systemSection.innerHTML = "";
    explainabilitySection.innerHTML = "";
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

/* =========================
   ANALYZE
========================= */

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
            "<div class='result-card error'>Cannot connect to backend.</div>";
    }
}

/* =========================
   RENDER
========================= */

function renderResult(data) {
    const { transformer, logistic_regression, verdict } = data;
    hasResult = true;

    /* ===== VERDICT ===== */

    let verdictTitle = "";
    let verdictClass = "";

    if (verdict.label === "AI") {
        verdictTitle = "🤖 AI Generated Text";
        verdictClass = "ai";
    } else if (verdict.label === "HUMAN") {
        verdictTitle = "🧑 Human Written Text";
        verdictClass = "human";
    } else {
        verdictTitle = "⚖️ Inconclusive Result";
        verdictClass = "uncertain";
    }

    verdictSection.innerHTML = `
        <div class="result-card final ${verdictClass}">
            <strong style="font-size: 18px;">
                ${verdictTitle}
                <span class="tooltip"> ⓘ
                    <span class="tooltip-text">
                        Confidence: <b>${verdict.confidence}</b><br>
                        Weighted score: <b>${verdict.weighted_score}</b>
                    </span>
                </span>
            </strong>

            <p style="margin-top: 10px; font-size: 14px; color: #cbd5f5;">
                ${verdict.explanation}
            </p>
        </div>
    `;

    /* ===== MODEL DETAILS ===== */

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
                ${(logistic_regression.ai_probability * 100).toFixed(1)}%
            </div>

            <div class="model">
                <strong>Final weighted score</strong>
                <div class="progress">
                    <div class="progress-fill" id="bar-final"></div>
                </div>
                ${(verdict.weighted_score * 100).toFixed(1)}%
            </div>

        </div>
    `;

    /* ===== SYSTEM INFO ===== */

    systemSection.innerHTML = `
        <p style="margin-top: 14px; font-size: 12px; color: #94a3b8; text-align: center;">
            Final decision based on weighted ensemble analysis.
            Confidence reflects agreement strength between models.
        </p>
    `;

    /* ===== ANIMATE ===== */

    setBar("bar-transformer", transformer.ai_probability * 100);
    setBar("bar-logistic", logistic_regression.ai_probability * 100);
    setBar("bar-final", verdict.weighted_score * 100);
    // ===============================
    // EXPLAINABILITY
    // ===============================
    if (data.explainability) {
        const pos = data.explainability.top_positive_features || [];
        const neg = data.explainability.top_negative_features || [];

        explainabilitySection.innerHTML = `
    <div class="result-card explainability">

        <h3 onclick="this.nextElementSibling.classList.toggle('hidden')">
            🔍 How the statistical model interpreted this text
        </h3>

        <div>

            <p style="font-size:13px; color:#cbd5f5; margin-bottom:10px;">
                The following features had the strongest influence on the Logistic Regression model.
                This explanation reflects <strong>statistical patterns</strong>, not semantic understanding.
            </p>

            <div style="margin-bottom:10px;">
                <strong style="color:#4ade80;">Features increasing AI likelihood:</strong>
                <ul>
                    ${pos.map(f => `
                        <li class="positive">
                            ${f.feature.replaceAll("_", " ")}
                            <span style="opacity:.6;">(impact: ${f.impact.toFixed(2)})</span>
                        </li>
                    `).join("")}
                </ul>
            </div>

            <div>
                <strong style="color:#f87171;">Features decreasing AI likelihood:</strong>
                <ul>
                    ${neg.map(f => `
                        <li class="negative">
                            ${f.feature.replaceAll("_", " ")}
                            <span style="opacity:.6;">(impact: ${f.impact.toFixed(2)})</span>
                        </li>
                    `).join("")}
                </ul>
            </div>

            <div class="explainability-note">
                This explanation is derived from a linear model and should be interpreted as indicative,
                not definitive.
            </div>

        </div>
    </div>
`;

    }

}

/* =========================
   HELPERS
========================= */

function setBar(id, value) {
    const el = document.getElementById(id);
    if (el) el.style.width = value + "%";
}
