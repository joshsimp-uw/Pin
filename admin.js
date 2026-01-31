(() => {
  const session = JSON.parse(localStorage.getItem("pin_session") || "null");
  if (!session?.isAuthenticated) {
    window.location.href = "./login.html";
    return;
  }

  // Admin rule: Any authenticated user may access admin

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  // Footer meta (matches other pages)
  const now = new Date();
  $("#year").textContent = String(now.getFullYear());
  $("#buildDate").textContent = now.toISOString();
  $("#adminBadge").textContent = `${session.email} • admin`;

  // Buttons
  $("#backBtn").addEventListener("click", () => window.location.href = "./app.html");
  $("#logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("pin_session");
    window.location.href = "./login.html";
  });

  // Storage keys
  const CONFIG_KEY = "pin_admin_config_v1";
  const AUDIT_KEY = "pin_admin_audit_v1";

  // Default config (prototype)
  const defaults = {
    llm: { provider: "mock", model: "gpt-4o-mini", apiKeyMasked: "not-set" },
    rag: { topK: 4, minScore: 0.15 },
    flows: { maxTurnsBeforeEscalate: 8 }
  };

  const loadConfig = () => {
    try {
      return { ...defaults, ...(JSON.parse(localStorage.getItem(CONFIG_KEY)) || {}) };
    } catch {
      return { ...defaults };
    }
  };

  const saveConfig = (cfg) => localStorage.setItem(CONFIG_KEY, JSON.stringify(cfg));

  const maskKey = (k) => {
    const s = String(k || "").trim();
    if (!s) return "not-set";
    if (s.length < 8) return "****";
    return `${s.slice(0, 3)}…${s.slice(-4)}`;
  };

  const logAudit = (action, detail) => {
    const log = JSON.parse(localStorage.getItem(AUDIT_KEY) || "[]");
    log.unshift({ ts: new Date().toISOString(), actor: session.email, action, detail });
    localStorage.setItem(AUDIT_KEY, JSON.stringify(log.slice(0, 50)));
  };

  const cfg = loadConfig();

  // Rendering
  const setActive = (view) => {
    $$(".nav button").forEach(b => b.classList.toggle("active", b.dataset.view === view));
  };

  const renderLLM = () => {
    $("#adminPanel").innerHTML = `
      <h2>LLM Settings</h2>
      <p class="small">Prototype storage only (localStorage). Real implementation would send this to FastAPI.</p>
      <div class="hr"></div>

      <label class="small">Provider</label>
      <select id="provider">
        <option value="mock">mock</option>
        <option value="openai_compat">openai_compat</option>
      </select>

      <label class="small" style="margin-top:10px">Model</label>
      <input id="model" class="input" />

      <label class="small" style="margin-top:10px">API Key (won’t store full key)</label>
      <input id="apiKey" class="input" type="password" placeholder="Enter to update" />

      <div class="hr"></div>

      <button class="btn" id="saveLLM">Save</button>
      <span class="small" style="margin-left:10px">Current key: <span class="mono" id="keyLabel"></span></span>
    `;

    $("#provider").value = cfg.llm.provider;
    $("#model").value = cfg.llm.model;
    $("#keyLabel").textContent = cfg.llm.apiKeyMasked;

    $("#saveLLM").addEventListener("click", () => {
      const newKey = $("#apiKey").value.trim();

      cfg.llm.provider = $("#provider").value;
      cfg.llm.model = $("#model").value.trim() || cfg.llm.model;

      if (newKey) cfg.llm.apiKeyMasked = maskKey(newKey);

      saveConfig(cfg);
      logAudit("update_llm", { provider: cfg.llm.provider, model: cfg.llm.model, apiKey: cfg.llm.apiKeyMasked });

      $("#apiKey").value = "";
      $("#keyLabel").textContent = cfg.llm.apiKeyMasked;
      alert("Saved LLM settings.");
    });
  };

  const renderRAG = () => {
    $("#adminPanel").innerHTML = `
      <h2>RAG Settings</h2>
      <div class="hr"></div>

      <label class="small">Top K</label>
      <input id="topK" class="input" type="number" min="1" max="10" />

      <label class="small" style="margin-top:10px">Min Score</label>
      <input id="minScore" class="input" type="number" step="0.05" min="0" max="1" />

      <div class="hr"></div>
      <button class="btn" id="saveRAG">Save</button>
    `;

    $("#topK").value = String(cfg.rag.topK);
    $("#minScore").value = String(cfg.rag.minScore);

    $("#saveRAG").addEventListener("click", () => {
      cfg.rag.topK = Number($("#topK").value || cfg.rag.topK);
      cfg.rag.minScore = Number($("#minScore").value || cfg.rag.minScore);

      saveConfig(cfg);
      logAudit("update_rag", { ...cfg.rag });
      alert("Saved RAG settings.");
    });
  };

  const renderFlows = () => {
    $("#adminPanel").innerHTML = `
      <h2>Flow Rules</h2>
      <div class="hr"></div>

      <label class="small">Max turns before escalate</label>
      <input id="maxTurns" class="input" type="number" min="3" max="30" />

      <div class="hr"></div>
      <button class="btn" id="saveFlows">Save</button>
    `;

    $("#maxTurns").value = String(cfg.flows.maxTurnsBeforeEscalate);

    $("#saveFlows").addEventListener("click", () => {
      cfg.flows.maxTurnsBeforeEscalate = Number($("#maxTurns").value || cfg.flows.maxTurnsBeforeEscalate);
      saveConfig(cfg);
      logAudit("update_flows", { ...cfg.flows });
      alert("Saved flow rules.");
    });
  };

  const renderAudit = () => {
    const log = JSON.parse(localStorage.getItem(AUDIT_KEY) || "[]");
    $("#adminPanel").innerHTML = `
      <h2>Audit Log</h2>
      <p class="small">Last 50 changes.</p>
      <div class="hr"></div>
      ${log.length ? log.map(e => `
        <div class="card" style="padding:12px;margin:10px 0;border-radius:12px">
          <div style="font-weight:900">${e.action}</div>
          <div class="small">By: <span class="mono">${e.actor}</span> • ${new Date(e.ts).toLocaleString()}</div>
          <pre class="small" style="margin:10px 0 0;white-space:pre-wrap">${JSON.stringify(e.detail, null, 2)}</pre>
        </div>
      `).join("") : `<div class="small">No changes yet.</div>`}
    `;
  };

  const route = (view) => {
    setActive(view);
    if (view === "llm") return renderLLM();
    if (view === "rag") return renderRAG();
    if (view === "flows") return renderFlows();
    if (view === "audit") return renderAudit();
    renderLLM();
  };

  // Sidebar clicks
  $$("aside .nav button[data-view]").forEach(btn => {
    btn.addEventListener("click", () => route(btn.dataset.view));
  });

  // Start on LLM page
  route("llm");
})();
