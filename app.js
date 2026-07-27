async function sendPrompt(prompt) {
    const response = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    });
    const data = await response.json();
    document.getElementById("answer").innerText = JSON.stringify(data, null, 2);
}

document.getElementById("askButton").addEventListener("click", () => {
    const prompt = document.getElementById("askInput").value;
    sendPrompt(prompt);
});
