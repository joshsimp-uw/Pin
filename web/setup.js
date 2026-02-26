(() => {
  const $ = (id) => document.getElementById(id);

  const now = new Date();
  $("year").textContent = String(now.getFullYear());
  $("buildDate").textContent = now.toISOString();

  const presetModel = () => {
    const p = $("llmProvider").value;
    if (p === "openai") $("llmModel").value = $("llmModel").value || "gpt-4o-mini";
    if (p === "gemini") $("llmModel").value = $("llmModel").value || "gemini-1.5-flash";
    if (p === "mock") $("llmModel").value = "mock";
  };

  $("llmProvider").addEventListener("change", presetModel);
  presetModel();

  // If already initialized, bounce to login.
  (async () => {
    try {
      const orgId = $("orgId").value || "ACME";
      const r = await fetch(`/api/bootstrap/status?org_id=${encodeURIComponent(orgId)}`);
      const j = await r.json();
      if (j?.initialized) window.location.href = "./login.html";
    } catch {
      // ignore
    }
  })();

  $("setupBtn").addEventListener("click", async () => {
    const org_id = $("orgId").value.trim() || "ACME";
    const org_name = $("orgName").value.trim() || org_id;
    const admin_email = $("adminEmail").value.trim();
    const admin_first = $("adminFirst").value.trim() || "Admin";
    const admin_last = $("adminLast").value.trim();
    const password = $("adminPassword").value;
    const llm_provider = $("llmProvider").value;
    const llm_model = $("llmModel").value.trim();
    const llm_api_key = $("llmKey").value.trim();

    try {
      const r = await fetch("/api/bootstrap/setup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          org_id,
          org_name,
          admin_email,
          admin_first,
          admin_last,
          password,
          llm_provider,
          llm_model,
          llm_api_key: llm_api_key || undefined,
        }),
      });

      if (!r.ok) {
        const t = await r.text().catch(() => "");
        throw new Error(t || `Setup failed (${r.status})`);
      }

      alert("Setup complete. Redirecting to login…");
      window.location.href = "./login.html";
    } catch (e) {
      alert(String(e?.message || e));
    }
  });
})();
