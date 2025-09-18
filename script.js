const promptInput = document.getElementById("promptInput");
const actionSelect = document.getElementById("actionSelect");
const runBtn = document.getElementById("runWorkflowBtn");
const output = document.getElementById("output");
const historyList = document.getElementById("historyList");

// Fetch history
async function fetchHistory() {
  try {
    const res = await fetch("/history");
    const data = await res.json();
    historyList.innerHTML = "";
    data.forEach(item => {
      const li = document.createElement("li");
      li.className = "history-item";
      li.textContent = item.final_result;
      historyList.appendChild(li);
    });
  } catch (err) {
    console.error("Error fetching history:", err);
  }
}

// Run workflow
runBtn.addEventListener("click", async () => {
  const prompt = promptInput.value;
  const action = actionSelect.value;
  if (!prompt) return alert("Please enter a prompt!");

  try {
    const res = await fetch("/run-workflow", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, action })
    });
    const data = await res.json();
    output.textContent = data.final_result;
    fetchHistory();
  } catch (err) {
    console.error("Fetch error:", err);
    output.textContent = "Error running workflow.";
  }
});

// Load history on page load
document.addEventListener("DOMContentLoaded", fetchHistory);
