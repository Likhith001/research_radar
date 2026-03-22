async function runPipeline() {
  const topic = document.getElementById("topic").value || "machine learning";
  const resultsDiv = document.getElementById("results");
  const loading = document.getElementById("loading");

  resultsDiv.innerHTML = "";
  loading.classList.remove("hidden");

  try {
    // Step 1: Run backend pipeline
    await fetch(`http://127.0.0.1:8000/run?topic=${topic}`);

    // Step 2: Fetch all papers
    const response = await fetch(`http://127.0.0.1:8000/papers`);
    const papers = await response.json();

    loading.classList.add("hidden");

    if (papers.length === 0) {
      resultsDiv.innerHTML = "<p>No papers available.</p>";
      return;
    }

    // Step 3: Render cards
    papers.forEach(paper => {
      const div = document.createElement("div");
      div.className = "card";

      div.innerHTML = `
        <h3>${paper.title}</h3>
        <div class="score">⭐ Score: ${paper.score.toFixed(2)}</div>
      `;

      div.style.opacity = 0;
      setTimeout(() => {
        div.style.opacity = 1;
      }, 100);

      resultsDiv.appendChild(div);
    });

    // Step 4: Render graph
    renderChart(papers);

  } catch (error) {
    loading.classList.add("hidden");
    resultsDiv.innerHTML = "<p>Error fetching data</p>";
    console.error(error);
  }
}

/* 🔍 Suggestions */
const suggestions = [
  "Machine Learning",
  "NLP",
  "Computer Vision",
  "Deep Learning",
  "AI Agents"
];

function loadSuggestions() {
  const box = document.getElementById("suggestions");
  box.innerHTML = "";

  suggestions.forEach(s => {
    const span = document.createElement("span");
    span.innerText = s;
    span.onclick = () => {
      document.getElementById("topic").value = s;
    };
    box.appendChild(span);
  });
}

window.onload = loadSuggestions;

/* 📊 Chart */
let chartInstance = null;

function renderChart(papers) {
  const ctx = document.getElementById("chart");

  const labels = papers.map(p => p.title.substring(0, 15));
  const scores = papers.map(p => p.score);

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Paper Scores",
        data: scores
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: { color: "white" }
        }
      },
      scales: {
        x: {
          ticks: { color: "white" }
        },
        y: {
          ticks: { color: "white" }
        }
      }
    }
  });
}

/* 🤖 Chatbot */
async function askAI() {
  const query = document.getElementById("chatInput").value;
  const output = document.getElementById("chatOutput");

  if (!query) return;

  output.innerText = "Thinking...";

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: query })
    });

    const data = await res.json();
    output.innerText = data.response;

  } catch (err) {
    output.innerText = "Error getting response";
  }
}

/* 🌙 Theme Toggle */
function toggleTheme() {
  document.body.classList.toggle("light");
}