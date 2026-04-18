const state = {
  anthropicConfigured: document.body.dataset.anthropic === "true",
};

function decodeBase64ToBlob(base64, mimeType = "text/csv;charset=utf-8;") {
  const binary = window.atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }
  return new Blob([bytes], { type: mimeType });
}

function createDownloadLink(filename, base64) {
  const template = document.getElementById("download-template");
  const link = template.content.firstElementChild.cloneNode(true);
  const blob = decodeBase64ToBlob(base64);
  const url = URL.createObjectURL(blob);
  link.href = url;
  link.download = filename;
  return link;
}

function safeCellValue(value) {
  if (value === null || value === undefined || value === "") {
    return "—";
  }
  return String(value);
}

function buildPreviewTable(rows) {
  if (!rows || rows.length === 0) {
    return "<p class=\"result-meta\">No preview rows available.</p>";
  }

  const columns = Object.keys(rows[0]).slice(0, 8);
  const head = columns.map((column) => `<th>${column}</th>`).join("");
  const body = rows
    .map((row) => {
      const cells = columns
        .map((column) => `<td>${safeCellValue(row[column])}</td>`)
        .join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");

  return `
    <div class="table-shell">
      <table>
        <thead><tr>${head}</tr></thead>
        <tbody>${body}</tbody>
      </table>
    </div>
  `;
}

function setLoading(button, loadingText) {
  button.dataset.originalText = button.textContent;
  button.textContent = loadingText;
  button.disabled = true;
}

function clearLoading(button) {
  button.textContent = button.dataset.originalText || "Submit";
  button.disabled = false;
}

function renderResult(container, html) {
  container.classList.remove("hidden");
  container.innerHTML = html;
}

function renderError(container, message) {
  renderResult(container, `<div class="notice warning">${message}</div>`);
}

async function handleJsonRequest({ url, options, button, loadingText, container, renderer }) {
  try {
    setLoading(button, loadingText);
    const response = await fetch(url, options);
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Request failed.");
    }

    renderer(payload);
  } catch (error) {
    renderError(container, error.message);
  } finally {
    clearLoading(button);
  }
}

document.getElementById("mock-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  const container = document.getElementById("mock-result");
  const formData = new FormData(form);

  await handleJsonRequest({
    url: "/api/mock-leads",
    options: { method: "POST", body: formData },
    button,
    loadingText: "Generating...",
    container,
    renderer: (payload) => {
      const download = createDownloadLink(payload.filename, payload.csv_base64);
      renderResult(
        container,
        `
          <p class="result-meta">Generated <strong>${payload.row_count}</strong> mock leads.</p>
          <div class="result-actions"></div>
          ${buildPreviewTable(payload.preview_rows)}
        `,
      );
      container.querySelector(".result-actions").appendChild(download);
    },
  });
});

document.getElementById("score-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  const container = document.getElementById("score-result");
  const formData = new FormData(form);

  await handleJsonRequest({
    url: "/api/score",
    options: { method: "POST", body: formData },
    button,
    loadingText: "Scoring...",
    container,
    renderer: (payload) => {
      const { summary } = payload;
      const download = createDownloadLink(payload.filename, payload.csv_base64);
      renderResult(
        container,
        `
          <p class="result-meta">
            Scored <strong>${summary.total_leads}</strong> leads. Average score:
            <strong>${summary.average_score}</strong>
          </p>
          <div class="metric-grid">
            <div class="metric-box"><span>Hot</span><strong>${summary.tier_counts.Hot}</strong></div>
            <div class="metric-box"><span>Warm</span><strong>${summary.tier_counts.Warm}</strong></div>
            <div class="metric-box"><span>Cold</span><strong>${summary.tier_counts.Cold}</strong></div>
            <div class="metric-box"><span>Max Score</span><strong>${summary.max_score}</strong></div>
          </div>
          <div class="result-actions"></div>
          ${buildPreviewTable(payload.preview_rows)}
        `,
      );
      container.querySelector(".result-actions").appendChild(download);
    },
  });
});

document.getElementById("outreach-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  const container = document.getElementById("outreach-result");

  if (!state.anthropicConfigured) {
    renderError(container, "ANTHROPIC_API_KEY is missing. Add it before generating outreach.");
    return;
  }

  const formData = new FormData(form);
  const generateAll = formData.get("generate_all") === "on";
  formData.set("generate_all", generateAll ? "true" : "false");

  await handleJsonRequest({
    url: "/api/outreach",
    options: { method: "POST", body: formData },
    button,
    loadingText: "Generating...",
    container,
    renderer: (payload) => {
      const download = createDownloadLink(payload.filename, payload.csv_base64);
      renderResult(
        container,
        `
          <p class="result-meta">
            Generated outreach for <strong>${payload.generated_count}</strong> leads.
            Failures: <strong>${payload.failed_count}</strong>
          </p>
          <div class="result-actions"></div>
          ${buildPreviewTable(payload.preview_rows)}
        `,
      );
      container.querySelector(".result-actions").appendChild(download);
    },
  });
});
