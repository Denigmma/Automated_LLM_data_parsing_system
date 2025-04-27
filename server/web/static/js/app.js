document.addEventListener("DOMContentLoaded", () => {
  const form      = document.getElementById("parse-form");
  const metaGroup = document.getElementById("meta-group");
  const output    = document.getElementById("output");

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
    output.textContent = "Parsing…";

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
      output.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      output.textContent = "Error: " + err.message;
    }
  });
});
