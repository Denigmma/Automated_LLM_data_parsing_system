document.addEventListener("DOMContentLoaded", () => {
  const form      = document.getElementById("parse-form");
  const metaGroup = document.getElementById("meta-group");
  const textOut   = document.getElementById("textResult");
  const jsonOut   = document.getElementById("jsonResult");

  // Show or hide metadata field based on selected mode
  function updateMetaVisibility() {
    const mode = form.elements["mode"].value;
    metaGroup.style.display = mode === "structuring" ? "block" : "none";
  }

  // initial
  updateMetaVisibility();

  // on radio change
  form.addEventListener("change", (e) => {
    if (e.target.name === "mode") {
      updateMetaVisibility();
    }
  });

  // on submit, fire AJAX
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    textOut.textContent = "Parsing…";
    jsonOut.textContent = "Parsing…";

    const url  = document.getElementById("url-input").value;
    const mode = form.elements["mode"].value;
    const meta = document.getElementById("meta-input").value;

    const payload = { url, mode };
    if (mode === "structuring") {
      payload.meta = meta;
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
        // если у вас в API ключ «json» — то data.json
        const j = data.json ?? data;
        jsonOut.textContent = JSON.stringify(j, null, 2);
      }
    } catch (err) {
      textOut.textContent = "";
      jsonOut.textContent = "Fetch error: " + err.message;
    }
  });
});
