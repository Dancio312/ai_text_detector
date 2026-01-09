async function analyze() {
    const text = document.getElementById("text").value;

    const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await response.json();
    document.getElementById("result").textContent =
        JSON.stringify(data, null, 2);
}
