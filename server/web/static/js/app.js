document.addEventListener("DOMContentLoaded", () => {
  const form             = document.getElementById("parse-form");
  const metaGroup        = document.getElementById("meta-group");
  const regenerateGroup  = document.getElementById("regenerate-group");
  const textOut          = document.getElementById("textResult");
  const jsonOut          = document.getElementById("jsonResult");

  // Переключение видимости полей через CSS-класс .hidden
  function updateVisibility() {
    const mode = form.elements["mode"].value;
    if (mode === "structuring") {
      metaGroup.classList.remove("hidden");
      regenerateGroup.classList.add("hidden");
    } else if (mode === "codegen") {
      metaGroup.classList.add("hidden");
      regenerateGroup.classList.remove("hidden");
    }
  }

  // Инициализировать при загрузке страницы
  updateVisibility();

  // Слушатель на смену режима
  form.addEventListener("change", (e) => {
    if (e.target.name === "mode") {
      updateVisibility();
    }
  });

  // Отправка формы через AJAX
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    textOut.textContent = "Parsing…";
    jsonOut.textContent = "Parsing…";

    const url        = document.getElementById("url-input").value;
    const query      = document.getElementById("query-input").value;
    const mode       = form.elements["mode"].value;
    const meta       = document.getElementById("meta-input").value;
    const regenerate = document.getElementById("regenerate-checkbox")?.checked ?? false;

    const payload = { url, query, mode };
    if (mode === "structuring") {
      payload.meta = meta;
    }
    if (mode === "codegen") {
      payload.regenerate = regenerate;
    }

    try {
      const resp = await fetch("/parse/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await resp.json();

      if (data.error) {
        textOut.textContent = "";
        jsonOut.textContent = "Error: " + data.error;
      } else {
        textOut.textContent = data.text ?? data.cleaned_text ?? "";
        const j = data.json ?? data;
        jsonOut.textContent = JSON.stringify(j, null, 2);
      }
    } catch (err) {
      textOut.textContent = "";
      jsonOut.textContent = "Fetch error: " + err.message;
    }
  });
});
