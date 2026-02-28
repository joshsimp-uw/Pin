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
  const escapeHtml = (s) => String(s ?? "").replace(/[&<>\"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
  })[c]);

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

    const ct = (r.headers.get("content-type") || "").toLowerCase();
    const parseBody = async () => {
      if (ct.includes("application/json")) return r.json();
      return r.text();
    };

    if (!r.ok) {
      const body = await parseBody().catch(() => "");
      const msg = typeof body === "string" ? body : JSON.stringify(body);
      const err = new Error(msg || `${path} failed (${r.status})`);
      err.status = r.status;
      err.body = body;
      throw err;
    }

    return parseBody();
  };

  const setActive = (view) => {
    $$('aside .nav button[data-view]').forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  };

  // QoL: collapsible groups
  $$('[data-group-toggle]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const group = btn.dataset.groupToggle;
      const body = document.querySelector(`[data-group-body="${group}"]`);
      if (!body) return;
      const isOpen = body.style.display !== 'none';
      body.style.display = isOpen ? 'none' : 'flex';
    });
  });

  const panel = $("#adminPanel");

  const renderLLM = async () => {
    setActive("llm");
    const data = await api("/api/admin/llm", { method: "GET" });
    const activeProvider = (data.active?.provider || "mock").toLowerCase();
    const providers = data.providers || [];
    const byProv = Object.fromEntries(providers.map((p) => [p.provider, p]));

    const getModel = (prov, fallback) => (byProv[prov]?.model || fallback);
    const hasKey = (prov) => Boolean(byProv[prov]?.has_key);
    const updatedAt = (prov) => (byProv[prov]?.updated_at || "");

    panel.innerHTML = `
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
    setActive("rag");
    const data = await api("/api/admin/rag", { method: "GET" });
    const active = (data.active?.backend || "local").toLowerCase();
    const canGemini = Boolean(data.available?.gemini);

    panel.innerHTML = `
      <h2>RAG Settings</h2>
      <p class="small">Select which vector index to use for retrieval. Local mode works offline; Gemini mode uses your stored key for embeddings.</p>
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

  const fetchUsers = async () => {
    const users = await api("/api/admin/users", { method: "GET" });
    return Array.isArray(users) ? users : [];
  };

  const renderUsersList = async () => {
    setActive("users_list");
    const users = await fetchUsers();

    panel.innerHTML = `
      <h2>Users</h2>
      <p class="small">Email is the login identity. Disabled users are retained for audit/legal history.</p>
      <div class="hr"></div>

      <div class="list" id="userList"></div>
    `;

    const list = $("#userList");
    if (!users.length) {
      list.innerHTML = `<div class="small">No users found.</div>`;
      return;
    }

    list.innerHTML = users.map(u => {
      const disabled = Number(u.is_disabled || 0) === 1;
      return `
        <div class="row" style="cursor:default; align-items:flex-start">
          <div>
            <div><strong>${escapeHtml((u.first_name || "") + " " + (u.last_name || ""))}</strong> ${disabled ? `<span class="badge" style="margin-left:8px">disabled</span>` : ``}</div>
            <div class="small"><span class="mono">${escapeHtml(u.user_id)}</span> • role: <span class="mono">${escapeHtml(u.role)}</span>${disabled && u.disabled_at ? ` • disabled ${escapeHtml(new Date(u.disabled_at).toLocaleString())}` : ""}</div>
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap">
            <button class="btn secondary" data-act="modify" data-user="${escapeHtml(u.user_id)}" type="button">Modify</button>
            ${disabled
              ? `<button class="btn" data-act="enable" data-user="${escapeHtml(u.user_id)}" type="button">Re-enable</button>`
              : `<button class="btn secondary" data-act="disable" data-user="${escapeHtml(u.user_id)}" type="button">Disable</button>`
            }
          </div>
        </div>
      `;
    }).join("");

    $$('[data-act="modify"]').forEach((b) => b.addEventListener('click', () => route("users_modify", b.dataset.user)));
    $$('[data-act="disable"]').forEach((b) => b.addEventListener('click', () => route("users_disable", b.dataset.user)));
    $$('[data-act="enable"]').forEach((b) => b.addEventListener('click', () => doEnableUser(b.dataset.user)));
  };

  const renderUsersNew = async () => {
    setActive("users_new");

    panel.innerHTML = `
      <h2>New User</h2>
      <p class="small">Creates a user and returns a one-time temporary password.</p>
      <div class="hr"></div>

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

      <div style="display:flex; gap:10px; margin-top:12px; flex-wrap:wrap; align-items:center">
        <button id="createUserBtn" class="btn" type="button">Create user</button>
        <span id="createUserMsg" class="small"></span>
      </div>

      <div id="reenableBox" style="display:none; margin-top:12px"></div>
    `;

    const msg = $("#createUserMsg");
    const reenableBox = $("#reenableBox");

    $("#createUserBtn").addEventListener("click", async () => {
      const first_name = $("#uFirst").value.trim();
      const last_name = $("#uLast").value.trim();
      const email = $("#uEmail").value.trim().toLowerCase();
      const is_admin = $("#uIsAdmin").checked;

      msg.textContent = "";
      reenableBox.style.display = "none";
      reenableBox.innerHTML = "";

      try {
        const r = await api("/api/admin/users", {
          method: "POST",
          body: JSON.stringify({ first_name, last_name, email, is_admin }),
        });
        msg.innerHTML = `Created <span class="mono">${escapeHtml(r.user_id)}</span>. Temporary password: <span class="mono">${escapeHtml(r.temp_password)}</span>`;
      } catch (e) {
        const body = e?.body;
        if (e.status === 409 && body && typeof body === 'object' && body.detail?.code === 'user_disabled') {
          const uid = body.detail.user_id || email;
          msg.textContent = body.detail.message || "User is disabled.";
          reenableBox.style.display = "block";
          reenableBox.innerHTML = `
            <div class="card" style="padding:12px">
              <div class="small"><strong>User exists but is disabled.</strong></div>
              <div class="small" style="margin-top:6px">Re-enable <span class="mono">${escapeHtml(uid)}</span>?</div>
              <div style="display:flex; gap:10px; margin-top:10px; flex-wrap:wrap">
                <button class="btn" id="reenableBtn" type="button">Re-enable user</button>
                <button class="btn secondary" id="cancelReenableBtn" type="button">Cancel</button>
              </div>
            </div>
          `;
          $("#reenableBtn").addEventListener("click", async () => {
            try {
              const r2 = await api(`/api/admin/users/${encodeURIComponent(uid)}/enable`, {
                method: "POST",
                body: JSON.stringify({ first_name, last_name, is_admin, reset_password: true })
              });
              msg.innerHTML = `Re-enabled <span class="mono">${escapeHtml(r2.user_id)}</span>. Temporary password: <span class="mono">${escapeHtml(r2.temp_password)}</span>`;
              reenableBox.style.display = "none";
            } catch (e2) {
              msg.textContent = String(e2?.message || e2);
            }
          });
          $("#cancelReenableBtn").addEventListener("click", () => {
            reenableBox.style.display = "none";
          });
          return;
        }

        msg.textContent = String(e?.message || e);
      }
    });
  };

  const doEnableUser = async (userId) => {
    if (!confirm(`Re-enable ${userId}? This will also issue a new temporary password.`)) return;
    try {
      const r = await api(`/api/admin/users/${encodeURIComponent(userId)}/enable`, {
        method: "POST",
        body: JSON.stringify({ reset_password: true }),
      });
      alert(`User re-enabled. Temporary password: ${r.temp_password || "(not reset)"}`);
      renderUsersList();
    } catch (e) {
      alert(String(e?.message || e));
    }
  };

  const renderUsersModify = async (prefillUserId = null) => {
    setActive("users_modify");
    const users = await fetchUsers();

    panel.innerHTML = `
      <h2>Modify User</h2>
      <p class="small">Email (identity) cannot be changed.</p>
      <div class="hr"></div>

      <label class="small">Select user</label>
      <select id="selUser"></select>

      <div class="hr"></div>

      <div class="form-grid">
        <div class="field">
          <label>First Name</label>
          <input id="mFirst" />
        </div>
        <div class="field">
          <label>Last Name</label>
          <input id="mLast" />
        </div>
        <div class="field">
          <label>Is Admin</label>
          <label style="display:flex; gap:10px; align-items:center; margin-top:8px">
            <input id="mIsAdmin" type="checkbox" />
            <span class="small">Grant admin access</span>
          </label>
        </div>
        <div class="field">
          <label>Status</label>
          <div class="small" id="mStatus" style="margin-top:10px"></div>
        </div>
      </div>

      <div style="display:flex; gap:10px; margin-top:12px; flex-wrap:wrap; align-items:center">
        <button class="btn" id="saveUserBtn" type="button">Save changes</button>
        <button class="btn secondary" id="resetPwBtn" type="button">Reset password</button>
        <span id="modifyMsg" class="small"></span>
      </div>
    `;

    const sel = $("#selUser");
    sel.innerHTML = users.map(u => `<option value="${escapeHtml(u.user_id)}">${escapeHtml(u.user_id)}${Number(u.is_disabled||0)===1 ? " (disabled)" : ""}</option>`).join("");

    const loadUser = (uid) => {
      const u = users.find(x => x.user_id === uid);
      if (!u) return;
      $("#mFirst").value = u.first_name || "";
      $("#mLast").value = u.last_name || "";
      $("#mIsAdmin").checked = (u.role || "").toLowerCase() === "admin";
      const disabled = Number(u.is_disabled || 0) === 1;
      $("#mStatus").innerHTML = disabled
        ? `Disabled${u.disabled_at ? ` • ${escapeHtml(new Date(u.disabled_at).toLocaleString())}` : ""}`
        : "Active";
    };

    if (prefillUserId && users.some(u => u.user_id === prefillUserId)) {
      sel.value = prefillUserId;
    }
    loadUser(sel.value);
    sel.addEventListener("change", () => loadUser(sel.value));

    const msg = $("#modifyMsg");

    $("#saveUserBtn").addEventListener("click", async () => {
      const user_id = sel.value;
      const first_name = $("#mFirst").value.trim();
      const last_name = $("#mLast").value.trim();
      const is_admin = $("#mIsAdmin").checked;
      msg.textContent = "";
      try {
        await api(`/api/admin/users/${encodeURIComponent(user_id)}`, {
          method: "PUT",
          body: JSON.stringify({ first_name, last_name, is_admin }),
        });
        msg.textContent = "Saved.";
      } catch (e) {
        msg.textContent = String(e?.message || e);
      }
    });

    $("#resetPwBtn").addEventListener("click", async () => {
      const user_id = sel.value;
      if (!confirm(`Reset password for ${user_id}?`)) return;
      msg.textContent = "";
      try {
        const r = await api(`/api/admin/users/${encodeURIComponent(user_id)}/enable`, {
          method: "POST",
          body: JSON.stringify({ reset_password: true }),
        });
        msg.innerHTML = `Temporary password: <span class="mono">${escapeHtml(r.temp_password)}</span>`;
      } catch (e) {
        msg.textContent = String(e?.message || e);
      }
    });
  };

  const renderUsersDisable = async (prefillUserId = null) => {
    setActive("users_disable");
    const users = await fetchUsers();

    panel.innerHTML = `
      <h2>Remove User (Disable)</h2>
      <p class="small">Users are never deleted. Disabling blocks login but retains historical data.</p>
      <div class="hr"></div>

      <label class="small">Select user</label>
      <select id="selUser"></select>

      <div class="hr"></div>

      <div class="card" style="padding:12px">
        <div class="small" id="disableInfo"></div>
        <div style="display:flex; gap:10px; margin-top:10px; flex-wrap:wrap">
          <button class="btn secondary" id="disableBtn" type="button">Disable user</button>
          <button class="btn" id="enableBtn" type="button">Re-enable user</button>
          <span id="disableMsg" class="small"></span>
        </div>
      </div>
    `;

    const sel = $("#selUser");
    sel.innerHTML = users.map(u => `<option value="${escapeHtml(u.user_id)}">${escapeHtml(u.user_id)}</option>`).join("");

    const info = $("#disableInfo");
    const msg = $("#disableMsg");

    const refreshInfo = () => {
      const u = users.find(x => x.user_id === sel.value);
      if (!u) return;
      const disabled = Number(u.is_disabled || 0) === 1;
      info.innerHTML = `
        <div><strong>${escapeHtml((u.first_name||"") + " " + (u.last_name||""))}</strong></div>
        <div class="small">role: <span class="mono">${escapeHtml(u.role)}</span></div>
        <div class="small">status: <span class="mono">${disabled ? "disabled" : "active"}</span>${disabled && u.disabled_at ? ` • ${escapeHtml(new Date(u.disabled_at).toLocaleString())}` : ""}</div>
      `;
    };

    if (prefillUserId && users.some(u => u.user_id === prefillUserId)) {
      sel.value = prefillUserId;
    }
    refreshInfo();
    sel.addEventListener('change', refreshInfo);

    $("#disableBtn").addEventListener('click', async () => {
      const user_id = sel.value;
      if (!confirm(`Disable ${user_id}?`)) return;
      msg.textContent = "";
      try {
        await api(`/api/admin/users/${encodeURIComponent(user_id)}/disable`, { method: 'POST' });
        msg.textContent = "User disabled.";
        await renderUsersList();
      } catch (e) {
        msg.textContent = String(e?.message || e);
      }
    });

    $("#enableBtn").addEventListener('click', async () => {
      const user_id = sel.value;
      await doEnableUser(user_id);
    });
  };

  const renderStub = (title, text) => {
    panel.innerHTML = `
      <h2>${escapeHtml(title)}</h2>
      <p class="small">${escapeHtml(text)}</p>
    `;
  };

  const route = async (view, arg = null) => {
    try {
      if (view === "llm") return renderLLM();
      if (view === "rag") return renderRAG();

      if (view === "users_list") return renderUsersList();
      if (view === "users_new") return renderUsersNew();
      if (view === "users_modify") return renderUsersModify(arg);
      if (view === "users_disable") return renderUsersDisable(arg);

      if (view === "flows") return renderStub("Flow Rules", "Flow rules UI is still a stub in this branch.");
      if (view === "audit") return renderStub("Audit Log", "Audit log UI is still a stub in this branch.");
      return renderLLM();
    } catch (e) {
      panel.innerHTML = `<h2>Error</h2><pre class="mono" style="white-space:pre-wrap">${escapeHtml(String(e?.message || e))}</pre>`;
    }
  };

  // Bind nav buttons (including submenu)
  $$('aside .nav button[data-view]').forEach((btn) => {
    btn.addEventListener('click', () => route(btn.dataset.view));
  });

  // Default route
  route("llm");
})();
