// ======= CONFIG =======
const API_BASE = "https://unthinkable-68r5.onrender.com"; // FastAPI base URL

// ======= ELEMENTS =======
const fileInput   = document.getElementById("fileInput");
const urlInput    = document.getElementById("urlInput"); // ✅ NEW
const btnProcess  = document.getElementById("btnProcess");
const previewImg  = document.getElementById("previewImg");
const statusEl    = document.getElementById("status");
const resultsEl   = document.getElementById("results");
const filterEl    = document.getElementById("scoreFilter");
const scoreValue  = document.getElementById("scoreValue");

// ======= STATE =======
let uploadedFileName = null;
let uploadedUrl = null; // ✅ NEW
let results = [];

// ======= HELPERS =======
const setStatus = (msg, isError = false) => {
  statusEl.textContent = msg || "";
  statusEl.style.color = isError ? "#ffb3b3" : "#9aa4b2";
};

const toPct = (score) => (score * 100).toFixed(0);

// Build an image URL for a dataset product (served from /static)
const productImageUrl = (fileName) => `${API_BASE}/static/${encodeURIComponent(fileName)}`;

// ======= UI EVENTS =======
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    btnProcess.disabled = false;
    const blobUrl = URL.createObjectURL(file);
    previewImg.src = blobUrl;
    setStatus(`Selected: ${file.name}`);
    uploadedUrl = null; // reset
  }
});

urlInput.addEventListener("input", () => {
  const url = urlInput.value.trim();
  if (url) {
    btnProcess.disabled = false;
    previewImg.src = url;
    setStatus(`URL selected`);
    uploadedFileName = null; // reset
    uploadedUrl = url;
  }
});

// ======= PROCESS BUTTON =======
btnProcess.addEventListener("click", async () => {
  try {
    btnProcess.disabled = false;
    setStatus("Uploading & processing… please wait");

    if (uploadedUrl) {
      // Case 1: URL Input
      const res = await fetch(`${API_BASE}/api/upload`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: uploadedUrl }),
      });

      if (!res.ok) throw new Error(`Upload URL failed: ${res.status}`);
      const data = await res.json();
      uploadedFileName = data?.data?.fileName;
    } else {
      // Case 2: File Input
      const file = fileInput.files[0];
      if (!file) return;

      const form = new FormData();
      form.append("image", file);
      form.append("fileName", file.name);

      const res = await fetch(`${API_BASE}/api/upload`, {
        method: "POST",
        body: form,
      });

      if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
      const data = await res.json();
      uploadedFileName = data?.data?.fileName || file.name;
    }

    // Ask for similar products
    setStatus("Finding similar products…");
    const simRes = await fetch(`${API_BASE}/api/similar?fileName=${encodeURIComponent(uploadedFileName)}`);
    if (!simRes.ok) throw new Error(`Similar failed: ${simRes.status}`);
    const simData = await simRes.json();
    results = Array.isArray(simData.similar) ? simData.similar : [];

    // Render
    renderResults();
    setStatus(`Done. Found ${results.length} matches.`);
  } catch (err) {
    console.error(err);
    setStatus(err.message || "Something went wrong.", true);
  } finally {
    btnProcess.disabled = false;
  }
});

// ======= FILTER SLIDER =======
filterEl.addEventListener("input", () => {
  const minPct = Number(filterEl.value);
  scoreValue.textContent = (minPct / 100).toFixed(2);
  renderResults();
});

// ======= RENDER =======
function renderResults() {
  const minScore = Number(filterEl.value) / 100; // 0..1
  scoreValue.textContent = (minScore).toFixed(2);

  const filtered = results.filter(r => (typeof r.score === "number" ? r.score : 0) >= minScore);

  if (!filtered.length) {
    resultsEl.innerHTML = `<div class="status">No results ≥ ${minScore.toFixed(2)}</div>`;
    return;
  }

  resultsEl.innerHTML = filtered.map(item => {
    const imgSrc = item.url ? item.url : productImageUrl(item.fileName);
    const pct = toPct(item.score ?? 0);
    return `
      <article class="card">
        <img src="${imgSrc}" alt="${item.fileName}" />
        <div class="meta">
          <div class="name">${item.fileName}</div>
          <div class="score">Similarity: ${pct}%</div>
        </div>
      </article>
    `;
  }).join("");
}
