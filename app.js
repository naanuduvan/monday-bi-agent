async function sendPrompt(promptText) {
  const prompt = promptText || document.getElementById("prompt").value;
  const response = await fetch("/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt })
  });
  const data = await response.json();

  // Show fallback message if present
  document.getElementById("answer").textContent =
    data.message || JSON.stringify(data, null, 2);
}
