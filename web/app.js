(() => {
  const session = JSON.parse(localStorage.getItem("pin_session") || "null");
  if (!session?.isAuthenticated) {
    window.location.href = "./login.html";
    return;
  }

  const BACKEND_BASE = ""; // same-origin

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));
  const escapeHtml = (s) => String(s ?? "").replace(/[&<>\"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
  })[c]);

  const api = async (path, opts = {}) => {
    const r = await fetch(`${BACKEND_BASE}${path}`,
      {
        ...opts,
        headers: {
          ...(opts.headers || {}),
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.token}`,
        },
      }
    );
    if (!r.ok) {
      const t = await r.text().catch(() => "");
      throw new Error(t || `${path} failed (${r.status})`);
    }
    const ct = r.headers.get("content-type") || "";
    if (ct.includes("application/json")) return r.json();
    return r.text();
  };

  // Header
  const now = new Date();
  $("#year").textContent = String(now.getFullYear());
  $("#buildDate").textContent = now.toISOString();
  $("#companyMeta").textContent = session.company;
  $("#userMeta").textContent = session.email;
  $("#userBadge").textContent = session.email;

  const logout = () => {
    localStorage.removeItem("pin_session");
    window.location.href = "./login.html";
  };
  $("#logoutBtn").addEventListener("click", logout);

  // Admin button
  const adminBtn = document.getElementById("adminBtn");
  if (adminBtn) {
    if (session.role === "admin") {
      adminBtn.style.display = "inline-flex";
      adminBtn.addEventListener("click", () => (window.location.href = "./admin.html"));
    } else {
      adminBtn.style.display = "none";
    }
  }

  // Local UI state (per user)
  const stateKey = `pin_ui_state_v2:${session.email}`;
  const uiState = (() => {
    try {
      return JSON.parse(localStorage.getItem(stateKey) || "{}") || {};
    } catch {
      return {};
    }
  })();
  const saveUi = () => localStorage.setItem(stateKey, JSON.stringify(uiState));

  let currentSessionId = uiState.currentSessionId || null;

  const setActiveNav = (view) => {
    $$("aside .nav button[data-view]").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  };

  const renderKpis = async () => {
    const data = await api("/api/home", { method: "GET" });
    const c = data.counts || {};

    const kpis = [
      { label: "Company", value: session.company },
      { label: "User", value: session.email },
      { label: "Open chats", value: String(c.open_chats ?? 0) },
      { label: "Closed chats", value: String(c.closed_chats ?? 0) },
      { label: "Open tickets", value: String(c.open_tickets ?? 0) },
      { label: "Closed tickets", value: String(c.closed_tickets ?? 0) },
    ];

    $("#kpiPanel").innerHTML = kpis.map(k => `
      <div class="item">
        <div class="label">${escapeHtml(k.label)}</div>
        <div class="value">${escapeHtml(k.value)}</div>
      </div>
    `).join("");

    // Sidebar counts
    const openChats = c.open_chats ?? 0;
    const openTickets = c.open_tickets ?? 0;
    const closedChats = c.closed_chats ?? 0;
    const closedTickets = c.closed_tickets ?? 0;

    const oc2 = document.getElementById("countOpenChats2");
    const tk = document.getElementById("countTickets");
    const cl = document.getElementById("countClosed");
    const ct = document.getElementById("countClosedTickets");

    if (oc2) oc2.textContent = String(openChats);
    if (tk) tk.textContent = String(openTickets);
    if (cl) cl.textContent = String(closedChats);
    if (ct) ct.textContent = String(closedTickets);
  };

  async function sendChatMessage({ message, session_id, context = {} }) {
    const res = await fetch(`${BACKEND_BASE}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.token}`,
      },
      body: JSON.stringify({ message, session_id, context })
    });

    if (!res.ok) {
      const errText = await res.text().catch(() => "");
      throw new Error(`/chat failed ${res.status}: ${errText}`);
    }

    return res.json();
  }

  const fmtDate = (iso) => {
    try { return new Date(iso).toLocaleString(); } catch { return String(iso || ""); }
  };

  const renderHome = async () => {
    setActiveNav("home");
    uiState.view = "home";
    saveUi();

    const data = await api("/api/home", { method: "GET" });
    const c = data.counts || {};
    const recentChats = (data.recent?.open_chats || []).slice(0, 5);
    const recentTickets = (data.recent?.open_tickets || []).slice(0, 5);

    $("#primaryPanel").innerHTML = `
      <h2>Welcome</h2>
      <p class="small">Here’s a quick snapshot of your help desk activity.</p>
      <div class="hr"></div>

      <div class="kpi" style="grid-template-columns: repeat(2, minmax(0, 1fr));">
        <div class="item"><div class="label">Open chats</div><div class="value">${escapeHtml(c.open_chats ?? 0)}</div></div>
        <div class="item"><div class="label">Closed chats</div><div class="value">${escapeHtml(c.closed_chats ?? 0)}</div></div>
        <div class="item"><div class="label">Open tickets</div><div class="value">${escapeHtml(c.open_tickets ?? 0)}</div></div>
        <div class="item"><div class="label">Closed tickets</div><div class="value">${escapeHtml(c.closed_tickets ?? 0)}</div></div>
      </div>

      <div class="hr"></div>

      <h3 style="margin:0 0 8px">Recent open chats</h3>
      <div class="list" id="recentChats"></div>

      <div class="hr"></div>

      <h3 style="margin:0 0 8px">Recent open tickets</h3>
      <div class="list" id="recentTickets"></div>
    `;

    const chatHtml = recentChats.length ? recentChats.map(s => `
      <button class="row" data-open-chat="${escapeHtml(s.session_id)}">
        <div>
          <div><strong>${escapeHtml(s.title || "Chat")}</strong></div>
          <div class="small">Updated ${escapeHtml(fmtDate(s.updated_at))}${s.ticket_id ? ` • Ticket linked` : ""}</div>
        </div>
        <div class="small">→</div>
      </button>
    `).join("") : `<div class="small">No open chats.</div>`;

    const ticketHtml = recentTickets.length ? recentTickets.map(t => `
      <button class="row" data-open-ticket="${escapeHtml(t.ticket_id)}">
        <div>
          <div><strong>${escapeHtml(t.summary || "Ticket")}</strong></div>
          <div class="small">Created ${escapeHtml(fmtDate(t.created_at))}</div>
        </div>
        <div class="small">→</div>
      </button>
    `).join("") : `<div class="small">No open tickets.</div>`;

    $("#recentChats").innerHTML = chatHtml;
    $("#recentTickets").innerHTML = ticketHtml;

    $$("[data-open-chat]").forEach(btn => btn.addEventListener("click", () => openChat(btn.dataset.openChat)));
    $$("[data-open-ticket]").forEach(btn => btn.addEventListener("click", () => openTicket(btn.dataset.openTicket)));

    await renderKpis();
  };

  const renderProfile = async () => {
    setActiveNav("profile");
    uiState.view = "profile";
    saveUi();

    $("#primaryPanel").innerHTML = `
      <h2>Profile</h2>
      <p class="small">Reset your password.</p>
      <div class="hr"></div>

      <div class="form-grid">
        <div class="field">
          <label>Current Password</label>
          <input id="pwCurrent" type="password" class="input" />
        </div>
        <div class="field">
          <label>New Password</label>
          <input id="pwNew" type="password" class="input" />
        </div>
        <div class="field">
          <label>Confirm New Password</label>
          <input id="pwConfirm" type="password" class="input" />
        </div>
      </div>

      <div style="display:flex; gap:10px; margin-top:12px; flex-wrap:wrap; align-items:center">
        <button class="btn" id="pwSaveBtn" type="button">Update password</button>
        <span id="pwMsg" class="small"></span>
      </div>
    `;

    const msg = $("#pwMsg");
    $("#pwSaveBtn").addEventListener("click", async () => {
      const current_password = $("#pwCurrent").value;
      const new_password = $("#pwNew").value;
      const confirm = $("#pwConfirm").value;
      msg.textContent = "";
      if (!current_password || !new_password) {
        msg.textContent = "Enter your current password and a new password.";
        return;
      }
      if (new_password !== confirm) {
        msg.textContent = "New password and confirmation do not match.";
        return;
      }

      try {
        await api("/auth/change_password", {
          method: "POST",
          body: JSON.stringify({ current_password, new_password }),
        });
        $("#pwCurrent").value = "";
        $("#pwNew").value = "";
        $("#pwConfirm").value = "";
        msg.textContent = "Password updated.";
      } catch (e) {
        msg.textContent = String(e?.message || e);
      }
    });

    await renderKpis();
  };

  const renderChatList = async (status) => {
    setActiveNav(status === "closed" ? "closedChats" : "openChats");
    uiState.view = status === "closed" ? "closedChats" : "openChats";
    saveUi();

    const rows = await api(`/api/chats?status=${encodeURIComponent(status)}`, { method: "GET" });

    $("#primaryPanel").innerHTML = `
      <h2>${status === "closed" ? "Closed Chats" : "Open Chats"}</h2>
      <p class="small">Chats are private to your account.</p>
      <div class="hr"></div>
      <div class="list" id="chatList"></div>
    `;

    const html = (rows || []).length ? rows.map(s => `
      <button class="row" data-open-chat="${escapeHtml(s.session_id)}">
        <div>
          <div><strong>${escapeHtml(s.title || "Chat")}</strong></div>
          <div class="small">Updated ${escapeHtml(fmtDate(s.updated_at))}${s.ticket_id ? ` • Ticket linked` : ""}</div>
        </div>
        <div class="small">→</div>
      </button>
    `).join("") : `<div class="small">No chats.</div>`;

    $("#chatList").innerHTML = html;
    $$("[data-open-chat]").forEach(btn => btn.addEventListener("click", () => openChat(btn.dataset.openChat)));
    await renderKpis();
  };

  const renderTicketList = async (status) => {
    setActiveNav(status === "closed" ? "closedTickets" : "openTickets");
    uiState.view = status === "closed" ? "closedTickets" : "openTickets";
    saveUi();

    const rows = await api(`/api/tickets?status=${encodeURIComponent(status)}`, { method: "GET" });

    $("#primaryPanel").innerHTML = `
      <h2>${status === "closed" ? "Closed Tickets" : "Open Tickets"}</h2>
      <p class="small">Tickets are separate from chats, but linked chats are preserved for reference.</p>
      <div class="hr"></div>
      <div class="list" id="ticketList"></div>
    `;

    const html = (rows || []).length ? rows.map(t => `
      <button class="row" data-open-ticket="${escapeHtml(t.ticket_id)}">
        <div>
          <div><strong>${escapeHtml(t.summary || "Ticket")}</strong></div>
          <div class="small">${escapeHtml(t.status)} • ${escapeHtml(fmtDate(t.created_at))}</div>
        </div>
        <div class="small">→</div>
      </button>
    `).join("") : `<div class="small">No tickets.</div>`;

    $("#ticketList").innerHTML = html;
    $$("[data-open-ticket]").forEach(btn => btn.addEventListener("click", () => openTicket(btn.dataset.openTicket)));
    await renderKpis();
  };

  const openTicket = async (ticketId) => {
    uiState.currentTicketId = ticketId;
    saveUi();

    const t = await api(`/api/tickets/${encodeURIComponent(ticketId)}`, { method: "GET" });
    const chats = t.chats || [];

    $("#primaryPanel").innerHTML = `
      <h2>Ticket</h2>
      <p class="small"><strong>${escapeHtml(t.summary || "")}</strong> • ${escapeHtml(t.status || "")}</p>
      <div class="hr"></div>
      <pre class="mono" style="white-space:pre-wrap; border:1px solid var(--border); padding:12px; border-radius:12px; background:rgba(0,0,0,0.02)">${escapeHtml(t.rendered_text || "")}</pre>

      <div class="hr"></div>
      <h3 style="margin:0 0 8px">Linked chats</h3>
      <div class="list" id="linkedChats"></div>
    `;

    $("#linkedChats").innerHTML = chats.length ? chats.map(s => `
      <button class="row" data-open-chat="${escapeHtml(s.session_id)}">
        <div>
          <div><strong>${escapeHtml(s.title || "Chat")}</strong></div>
          <div class="small">${escapeHtml(s.status)} • Updated ${escapeHtml(fmtDate(s.updated_at))}</div>
        </div>
        <div class="small">→</div>
      </button>
    `).join("") : `<div class="small">No linked chats yet.</div>`;

    $$("[data-open-chat]").forEach(btn => btn.addEventListener("click", () => openChat(btn.dataset.openChat)));
    await renderKpis();
  };

  const openChat = async (sessionId) => {
    currentSessionId = sessionId;
    uiState.currentSessionId = sessionId;
    saveUi();

    const chat = await api(`/api/chats/${encodeURIComponent(sessionId)}`, { method: "GET" });
    const msgs = await api(`/api/chats/${encodeURIComponent(sessionId)}/messages`, { method: "GET" });

    setActiveNav("chat");

    $("#primaryPanel").innerHTML = `
      <h2>${escapeHtml(chat.title || "Chat")}</h2>
      <p class="small">Status: <span class="mono">${escapeHtml(chat.status)}</span>${chat.ticket_id ? ` • Ticket: <span class="mono">${escapeHtml(chat.ticket_id)}</span>` : ""}</p>
      <div class="hr"></div>

      <div class="chat">
        <div class="chat-log" id="chatLog"></div>

        <div class="chat-input">
          <textarea id="chatText" placeholder="Type your message..." ${chat.status !== "open" ? "disabled" : ""}></textarea>
          <button id="sendBtn" class="btn" ${chat.status !== "open" ? "disabled" : ""}>Send</button>
        </div>

        <div style="display:flex; gap:10px; flex-wrap:wrap">
          <button id="escalateBtn" class="btn secondary" type="button" ${chat.ticket_id ? "disabled" : ""}>Escalate to Ticket</button>
          <button id="closeChatBtn" class="btn secondary" type="button" ${chat.status !== "open" ? "disabled" : ""}>Close Chat</button>
          ${chat.ticket_id ? `<button id="openTicketBtn" class="btn secondary" type="button">Open Ticket</button>` : ""}
        </div>
      </div>
    `;

    const log = $("#chatLog");

    const appendMsg = (role, text, ts) => {
      const isUser = role === "user" || role === "human";
      const cls = isUser ? "user" : "bot";
      const name = isUser ? "You" : "Pin";
      const el = document.createElement("div");
      el.className = `msg ${cls}`;
      
      // Use escapeHtml for users, and marked.parse for the LLM
      const contentHtml = isUser 
        ? `<div class="msg-text">${escapeHtml(text)}</div>` 
        : `<div class="msg-text markdown-body">${marked.parse(text)}</div>`;

      el.innerHTML = `
        <div><strong>${escapeHtml(name)}</strong></div>
        ${contentHtml}
        <div class="meta">${escapeHtml(fmtDate(ts || new Date().toISOString()))}</div>
      `;
      
      log.appendChild(el);
      log.scrollTop = log.scrollHeight;
    };

    log.innerHTML = "";
    (msgs || []).forEach(m => appendMsg(m.role, m.content, m.created_at));

    const showActionButtons = (type) => {
      const holder = document.createElement("div");
      holder.style.display = "flex";
      holder.style.gap = "10px";
      holder.style.flexWrap = "wrap";
      holder.style.marginTop = "10px";

      if (type === "escalate_to_ticket") {
        const b1 = document.createElement("button");
        b1.className = "btn";
        b1.textContent = "Escalate to Ticket";
        b1.addEventListener("click", async () => {
          try {
            const r = await api(`/api/chats/${encodeURIComponent(sessionId)}/escalate`, { method: "POST", body: JSON.stringify({}) });
            appendMsg("assistant", r.rendered || "Ticket created.", new Date().toISOString());
            await renderKpis();
            await openChat(sessionId);
          } catch (e) {
            alert(String(e?.message || e));
          }
        });

        const b2 = document.createElement("button");
        b2.className = "btn secondary";
        b2.textContent = "No";
        b2.addEventListener("click", () => sendAndRender("no"));

        holder.appendChild(b1);
        holder.appendChild(b2);
      }

      if (type === "close_chat") {
        const b1 = document.createElement("button");
        b1.className = "btn";
        b1.textContent = "Close chat";
        b1.addEventListener("click", async () => {
          try {
            await api(`/api/chats/${encodeURIComponent(sessionId)}/close`, { method: "POST" });
            await openChat(sessionId);
            await renderKpis();
          } catch (e) {
            alert(String(e?.message || e));
          }
        });

        const b2 = document.createElement("button");
        b2.className = "btn secondary";
        b2.textContent = "Keep open";
        b2.addEventListener("click", () => sendAndRender("no"));

        holder.appendChild(b1);
        holder.appendChild(b2);
      }

      log.appendChild(holder);
      log.scrollTop = log.scrollHeight;
    };

    const sendAndRender = async (text) => {
      const msg = String(text || "").trim();
      if (!msg) return;
      appendMsg("user", msg, new Date().toISOString());

      try {
        const data = await sendChatMessage({ message: msg, session_id: sessionId, context: {} });

        if (data.type === "answer") {
          appendMsg("assistant", data.message || "", new Date().toISOString());
        } else if (data.type === "ticket") {
          appendMsg("assistant", data.rendered || "Ticket created.", new Date().toISOString());
        } else if (data.type === "action") {
          appendMsg("assistant", data.message || "", new Date().toISOString());
          showActionButtons(data.meta?.pending || "");
        } else {
          appendMsg("assistant", JSON.stringify(data), new Date().toISOString());
        }

        await renderKpis();
      } catch (e) {
        appendMsg("assistant", String(e?.message || e), new Date().toISOString());
      }
    };

    const sendBtn = $("#sendBtn");
    const chatText = $("#chatText");
    if (sendBtn && chatText) {
      sendBtn.addEventListener("click", () => {
        const t = chatText.value;
        chatText.value = "";
        sendAndRender(t);
      });
    }

    const closeBtn = $("#closeChatBtn");
    if (closeBtn) {
      closeBtn.addEventListener("click", async () => {
        if (!confirm("Close this chat?")) return;
        try {
          await api(`/api/chats/${encodeURIComponent(sessionId)}/close`, { method: "POST" });
          await openChat(sessionId);
          await renderKpis();
        } catch (e) {
          alert(String(e?.message || e));
        }
      });
    }

    const escBtn = $("#escalateBtn");
    if (escBtn) {
      escBtn.addEventListener("click", async () => {
        if (!confirm("Create a ticket from this chat?")) return;
        try {
          const r = await api(`/api/chats/${encodeURIComponent(sessionId)}/escalate`, { method: "POST", body: JSON.stringify({}) });
          appendMsg("assistant", r.rendered || "Ticket created.", new Date().toISOString());
          await openChat(sessionId);
          await renderKpis();
        } catch (e) {
          alert(String(e?.message || e));
        }
      });
    }

    const otBtn = $("#openTicketBtn");
    if (otBtn) {
      otBtn.addEventListener("click", () => openTicket(chat.ticket_id));
    }

    await renderKpis();
  };

  const createNewChat = async () => {
    setActiveNav("newIssue");
    uiState.view = "newIssue";
    saveUi();

    // Use existing /session/new endpoint
    const r = await fetch(`${BACKEND_BASE}/session/new`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${session.token}` },
    });
    if (!r.ok) {
      const t = await r.text().catch(() => "");
      throw new Error(t || `Failed to create chat (${r.status})`);
    }
    const data = await r.json();
    await openChat(data.session_id);
  };

  // Wire sidebar
  const route = async (view) => {
    try {
      if (view === "logout") return logout();
      if (view === "home") return renderHome();
      if (view === "profile") return renderProfile();
      if (view === "newIssue") return createNewChat();
      if (view === "openChats") return renderChatList("open");
      if (view === "closedChats") return renderChatList("closed");
      if (view === "openTickets") return renderTicketList("created");
      if (view === "closedTickets") return renderTicketList("closed");
      if (view === "chat" && currentSessionId) return openChat(currentSessionId);
      return renderHome();
    } catch (e) {
      $("#primaryPanel").innerHTML = `<h2>Error</h2><pre class="mono" style="white-space:pre-wrap">${escapeHtml(String(e?.message || e))}</pre>`;
    }
  };

  $$("aside .nav button[data-view]").forEach((btn) => {
    btn.addEventListener("click", () => route(btn.dataset.view));
  });

  // Startup: show home (not new chat)
  route(uiState.view || "home");
})();
