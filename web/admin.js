(() => {
  const session = JSON.parse(localStorage.getItem("pin_session") || "null");
  if (!session?.isAuthenticated) {
    window.location.href = "./login.html";
    return;
  }
  if (session.role !== "admin") {
    window.location.href = "./app.html";
    return;
  }

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  const now = new Date();
  $("#year").textContent = String(now.getFullYear());
  $("#buildDate").textContent = now.toISOString();
  $("#adminBadge").textContent = `${session.email} • admin`;

  $("#backBtn").addEventListener("click", () => (window.location.href = "./app.html"));
  $("#logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("pin_session");
    window.location.href = "./login.html";
  });

  const api = async (path, opts = {}) => {
    const r = await fetch(path, {
      ...opts,
      headers: {
        ...(opts.headers || {}),
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.token}`,
      },
    });
    if (!r.ok) {
      const t = await r.text().catch(() => "");
      throw new Error(t || `${path} failed (${r.status})`);
    }
    return r.json();
  };

  const setActive = (view) => {
    $$(".nav button").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  };

  const renderLLM = async () => {
    const data = await api("/api/admin/llm", { method: "GET" });
    const activeProvider = (data.active?.provider || "mock").toLowerCase();
    const providers = data.providers || [];
    const byProv = Object.fromEntries(providers.map((p) => [p.provider, p]));

    const getModel = (prov, fallback) => (byProv[prov]?.model || fallback);
    const hasKey = (prov) => Boolean(byProv[prov]?.has_key);
    const updatedAt = (prov) => (byProv[prov]?.updated_at || "");

    $("#adminPanel").innerHTML = `
      <h2>LLM Settings</h2>
      <p class="small">These settings are stored in SQLite. API keys are encrypted at rest.</p>
      <div class="hr"></div>

      <label class="small">Active Provider</label>
      <select id="activeProvider">
        <option value="mock">mock</option>
        <option value="openai">openai</option>
        <option value="gemini">gemini</option>
      </select>

      <div class="hr"></div>

      <h3 style="margin:0 0 6px">OpenAI</h3>
      <label class="small">Model</label>
      <input id="openaiModel" class="input" />
      <label class="small" style="margin-top:10px">API Key</label>
      <input id="openaiKey" class="input" type="password" placeholder="Enter to update" />
      <div class="small" style="margin-top:6px">Stored key: <span class="mono">${hasKey("openai") ? "set" : "not-set"}</span>${updatedAt("openai") ? ` • updated ${new Date(updatedAt("openai")).toLocaleString()}` : ""}</div>

      <div class="hr"></div>

      <h3 style="margin:0 0 6px">Gemini</h3>
      <label class="small">Model</label>
      <input id="geminiModel" class="input" />
      <label class="small" style="margin-top:10px">API Key</label>
      <input id="geminiKey" class="input" type="password" placeholder="Enter to update" />
      <div class="small" style="margin-top:6px">Stored key: <span class="mono">${hasKey("gemini") ? "set" : "not-set"}</span>${updatedAt("gemini") ? ` • updated ${new Date(updatedAt("gemini")).toLocaleString()}` : ""}</div>

      <div class="hr"></div>

      <h3 style="margin:0 0 6px">Mock</h3>
      <label class="small">Model</label>
      <input id="mockModel" class="input" />

      <div class="hr"></div>
      <button class="btn" id="saveLLM">Save</button>
    `;

    $("#activeProvider").value = activeProvider;
    $("#openaiModel").value = getModel("openai", "gpt-4o-mini");
    $("#geminiModel").value = getModel("gemini", "gemini-1.5-flash");
    $("#mockModel").value = getModel("mock", "mock");

    $("#saveLLM").addEventListener("click", async () => {
      const ap = $("#activeProvider").value;
      const openaiModel = $("#openaiModel").value.trim() || "gpt-4o-mini";
      const geminiModel = $("#geminiModel").value.trim() || "gemini-1.5-flash";
      const mockModel = $("#mockModel").value.trim() || "mock";
      const openaiKey = $("#openaiKey").value.trim();
      const geminiKey = $("#geminiKey").value.trim();

      try {
        // Update each provider's model + optional key
        await api("/api/admin/llm", {
          method: "PUT",
          body: JSON.stringify({ provider: "openai", model: openaiModel, api_key: openaiKey || undefined, set_active: ap === "openai" }),
        });
        await api("/api/admin/llm", {
          method: "PUT",
          body: JSON.stringify({ provider: "gemini", model: geminiModel, api_key: geminiKey || undefined, set_active: ap === "gemini" }),
        });
        await api("/api/admin/llm", {
          method: "PUT",
          body: JSON.stringify({ provider: "mock", model: mockModel, set_active: ap === "mock" }),
        });

        $("#openaiKey").value = "";
        $("#geminiKey").value = "";
        alert("Saved LLM settings.");
        renderLLM();
      } catch (e) {
        alert(String(e?.message || e));
      }
    });
  };

  const renderRAG = async () => {
    const data = await api("/api/admin/rag", { method: "GET" });
    const active = (data.active?.backend || "local").toLowerCase();
    const canGemini = Boolean(data.available?.gemini);

    $("#adminPanel").innerHTML = `
      <h2>RAG Settings</h2>
      <p class="small">Select which vector index to use for retrieval. Local mode works offline; Gemini mode uses your stored <span class="mono">aistudio.google.com</span> key for embeddings.</p>
      <div class="hr"></div>

      <label class="small">Active Vector Backend</label>
      <select id="ragBackend">
        <option value="local">local (offline)</option>
        <option value="gemini">gemini (embeddings)</option>
      </select>
      <div class="small" style="margin-top:6px">
        Gemini availability: <span class="mono">${canGemini ? "available" : "missing key"}</span>
      </div>

      <div class="hr"></div>
      <button class="btn" id="saveRAG">Save</button>
      <div class="small" style="margin-top:10px">
        Note: If you switch backends, you may need to re-ingest the KB so the selected index is populated.
      </div>
    `;

    const sel = $("#ragBackend");
    sel.value = active;
    if (!canGemini) {
      sel.querySelector('option[value="gemini"]').disabled = true;
      if (sel.value === "gemini") sel.value = "local";
    }

    $("#saveRAG").addEventListener("click", async () => {
      const backend = sel.value;
      try {
        await api("/api/admin/rag", { method: "PUT", body: JSON.stringify({ backend }) });
        alert("Saved RAG settings.");
        renderRAG();
      } catch (e) {
        alert(String(e?.message || e));
      }
    });
  };

  // Keep the other tabs as placeholders (still local-only for now)
  const renderUsers = async () => {
    activeView("users");

    const users = await api("/api/admin/users", { method: "GET" });

    panel.innerHTML = `
      <h2>Users</h2>
      <p class="small">Create users and assign admin rights. Email is the login ID. A temporary password is generated on create.</p>
      <div class="hr"></div>

      <h3 style="margin:0 0 10px">Add user</h3>
      <div class="form-grid">
        <div class="field">
          <label>First Name</label>
          <input id="uFirst" placeholder="First name" />
        </div>
        <div class="field">
          <label>Last Name</label>
          <input id="uLast" placeholder="Last name" />
        </div>
        <div class="field">
          <label>Email (login)</label>
          <input id="uEmail" placeholder="name@company.com" />
        </div>
        <div class="field">
          <label>Is Admin</label>
          <label style="display:flex; gap:10px; align-items:center; margin-top:8px">
            <input id="uIsAdmin" type="checkbox" />
            <span class="small">Grant admin access</span>
          </label>
        </div>
      </div>
      <div style="display:flex; gap:10px; margin-top:12px; flex-wrap:wrap">
        <button id="createUserBtn" class="btn" type="button">Create user</button>
        <span id="createUserMsg" class="small"></span>
      </div>

      <div class="hr"></div>

      <h3 style="margin:0 0 10px">Existing users</h3>
      <div class="list" id="userList"></div>
    `;

    const list = document.getElementById("userList");
    const html = (users || []).length ? users.map(u => `
      <div class="row" style="cursor:default">
        <div>
          <div><strong>${escapeHtml((u.first_name || "") + " " + (u.last_name || ""))}</strong></div>
          <div class="small"><span class="mono">${escapeHtml(u.user_id)}</span> • role: <span class="mono">${escapeHtml(u.role)}</span></div>
        </div>
        <div class="small">${escapeHtml((u.created_at || "").split("T")[0] || "")}</div>
      </div>
    `).join("") : `<div class="small">No users found.</div>`;
    list.innerHTML = html;

    document.getElementById("createUserBtn").addEventListener("click", async () => {
      const first_name = document.getElementById("uFirst").value.trim();
      const last_name = document.getElementById("uLast").value.trim();
      const email = document.getElementById("uEmail").value.trim();
      const is_admin = document.getElementById("uIsAdmin").checked;
      const msg = document.getElementById("createUserMsg");
      msg.textContent = "";

      try {
        const r = await api("/api/admin/users", {
          method: "POST",
          body: JSON.stringify({ first_name, last_name, email, is_admin }),
        });
        msg.innerHTML = `Created <span class="mono">${escapeHtml(r.user_id)}</span>. Temporary password: <span class="mono">${escapeHtml(r.temp_password)}</span>`;
        await renderUsers();
      } catch (e) {
        msg.textContent = String(e?.message || e);
      }
    });
  };

  const renderStub = (title, text) => {
    $("#adminPanel").innerHTML = `
      <h2>${title}</h2>
      <p class="small">${text}</p>
    `;
  };

  const route = (view) => {
    setActive(view);
    if (view === "llm") return renderLLM();
    if (view === "rag") return renderRAG();
    if (view === "users") return renderUsers();
    if (view === "flows") return renderStub("Flow Rules", "Flow rules UI is still a stub in this branch.");
    if (view === "audit") return renderStub("Audit Log", "Audit log UI is still a stub in this branch.");
    return renderLLM();
  };

  $$("aside .nav button[data-view]").forEach((btn) => {
    btn.addEventListener("click", () => route(btn.dataset.view));
  });

  route("llm");
})();
