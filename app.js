(() => {
  const session = JSON.parse(localStorage.getItem("pin_session") || "null");
  if (!session?.isAuthenticated) {
    window.location.href = "./login.html";
    return;
  }

  const stateKey = "pin_state_v1";
  const now = new Date();

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));
  const escapeHtml = (s) => String(s).replace(/[&<>\"']/g, (c) => ({
    "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"
  })[c]);

  const loadState = () => {
    const raw = localStorage.getItem(stateKey);
    if (raw) return JSON.parse(raw);

    return {
      chats: [],         // {id, name, createdAt, messages:[{role, text, ts}], status:'open'|'closed', ticketId?}
      tickets: [],       // {id, chatId, title, createdAt, payload}
      selectedChatId: null,
      view: "newIssue",
      version: 1
    };
  };

  const saveState = () => localStorage.setItem(stateKey, JSON.stringify(state));

  const state = loadState();

  // Header + footer meta
  $("#year").textContent = String(now.getFullYear());
  $("#buildDate").textContent = now.toISOString();
  $("#companyMeta").textContent = session.company;
  $("#userMeta").textContent = session.email;
  $("#userBadge").textContent = `${session.email} • ${session.dept}`;

  const logout = () => {
    localStorage.removeItem("pin_session");
    window.location.href = "./login.html";
  };
  $("#logoutBtn").addEventListener("click", logout);

  // Counts
  const counts = () => {
    const openChats = state.chats.filter(c => c.status === "open").length;
    const tickets = state.tickets.length;
    const closed = state.chats.filter(c => c.status === "closed").length;
    $("#countOpenChats").textContent = String(openChats);
    $("#countOpenChats2").textContent = String(openChats);
    $("#countTickets").textContent = String(tickets);
    $("#countClosed").textContent = String(closed);
  };

  // Render KPI context panel
  const renderKpis = () => {
    const open = state.chats.filter(c => c.status === "open").length;
    const closed = state.chats.filter(c => c.status === "closed").length;
    const selected = state.selectedChatId ? state.chats.find(c => c.id === state.selectedChatId) : null;

    const kpis = [
      { label: "Company", value: session.company },
      { label: "User", value: session.email },
      { label: "Department", value: session.dept },
      { label: "Open chats", value: String(open) },
      { label: "Closed chats", value: String(closed) },
      { label: "Selected", value: selected ? selected.name : "—" },
    ];

    $("#kpiPanel").innerHTML = kpis.map(k => `
      <div class="item">
        <div class="label">${escapeHtml(k.label)}</div>
        <div class="value">${escapeHtml(k.value)}</div>
      </div>
    `).join("");
  };

  const setActiveNav = (view) => {
    $$(".nav button").forEach(b => b.classList.toggle("active", b.dataset.view === view));
  };

  const uid = () => Math.random().toString(36).slice(2, 10);

  // Views
  const view_newIssue = () => {
    setActiveNav("newIssue");
    state.view = "newIssue";
    saveState();

    $("#primaryPanel").innerHTML = `
      <h2>New Issue</h2>
      <p class="small">Start a new chat session. The first meaningful message becomes the issue summary (chat name).</p>
      <div class="hr"></div>

      <div class="chat">
        <div class="chat-log" id="chatLog">
          <div class="msg bot">
            <div><strong>Pin</strong>: Hi! Describe what's going on, and I’ll ask the questions needed to resolve it — or build a ticket if we can’t.</div>
            <div class="meta">${escapeHtml(new Date().toLocaleString())}</div>
          </div>
        </div>

        <div class="chat-input">
          <textarea id="chatText" placeholder="Describe your issue..."></textarea>
          <button id="sendBtn" class="btn">Send</button>
        </div>

        <div style="display:flex; gap:10px; flex-wrap:wrap">
          <button id="createTicketBtn" class="btn secondary" type="button">Generate Ticket (demo)</button>
          <button id="closeChatBtn" class="btn secondary" type="button">Close Chat</button>
          <span class="small">Tip: Use “Generate Ticket” after you’ve provided enough detail.</span>
        </div>
      </div>
    `;

    // Create a new chat instance immediately per your spec
    const newChat = {
      id: uid(),
      name: "New Issue",
      createdAt: new Date().toISOString(),
      status: "open",
      messages: [
        { role: "bot", text: "Hi! Describe what's going on, and I’ll ask the questions needed to resolve it — or build a ticket if we can’t.", ts: new Date().toISOString() }
      ]
    };
    state.chats.unshift(newChat);
    state.selectedChatId = newChat.id;
    saveState();
    counts();
    renderKpis();

    const renderChat = () => {
      const chat = state.chats.find(c => c.id === state.selectedChatId);
      if (!chat) return;

      const log = $("#chatLog");
      log.innerHTML = chat.messages.map(m => `
        <div class="msg ${m.role === "user" ? "user" : "bot"}">
          <div>${m.role === "user" ? "<strong>You</strong>" : "<strong>Pin</strong>"}: ${escapeHtml(m.text)}</div>
          <div class="meta">${escapeHtml(new Date(m.ts).toLocaleString())}</div>
        </div>
      `).join("");
      log.scrollTop = log.scrollHeight;
    };

    const setChatNameFromFirstUserMessage = (text) => {
      const chat = state.chats.find(c => c.id === state.selectedChatId);
      if (!chat) return;

      if (chat.name === "New Issue") {
        // crude summary heuristic: first sentence up to 60 chars
        const summary = text.split(/[.\n]/)[0].trim().slice(0, 60) || "Issue";
        chat.name = summary;
      }
    };

    const addBotFollowUp = () => {
      const chat = state.chats.find(c => c.id === state.selectedChatId);
      if (!chat) return;

      // Demo follow-up: a small decision tree stub
      const last = chat.messages.filter(m => m.role === "user").at(-1)?.text?.toLowerCase() || "";
      let prompt = "Got it. What device are you on, and what error message (exact text) do you see?";
      if (last.includes("vpn")) prompt = "VPN issue — which client (AnyConnect, GlobalProtect, Windows built-in) and are you offsite? Any error code?";
      if (last.includes("email")) prompt = "Email issue — is this Outlook, OWA, or mobile? Are you seeing a password prompt, or messages stuck sending?";
      if (last.includes("printer")) prompt = "Printer issue — what’s the printer name/IP and what exactly fails (release, print, or connection)?";

      chat.messages.push({ role: "bot", text: prompt, ts: new Date().toISOString() });
      saveState();
      renderChat();
    };

    const send = () => {
      const textArea = $("#chatText");
      const text = textArea.value.trim();
      if (!text) return;

      const chat = state.chats.find(c => c.id === state.selectedChatId);
      if (!chat) return;

      chat.messages.push({ role: "user", text, ts: new Date().toISOString() });
      setChatNameFromFirstUserMessage(text);
      saveState();
      counts();
      renderKpis();
      renderChat();
      textArea.value = "";
      addBotFollowUp();
    };

    $("#sendBtn").addEventListener("click", send);
    $("#chatText").addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
    });

    $("#createTicketBtn").addEventListener("click", () => {
      const chat = state.chats.find(c => c.id === state.selectedChatId);
      if (!chat) return;

      const title = chat.name === "New Issue" ? "Issue" : chat.name;
      const payload = {
        company: session.company,
        requester: { email: session.email, department: session.dept },
        title,
        createdAt: new Date().toISOString(),
        transcript: chat.messages,
        // Integration note: this maps cleanly to tier1-bot schemas later
        integration: { status: "stub", target: "ticketing-system" }
      };

      const ticket = { id: `TCK-${Math.floor(Math.random()*90000+10000)}`, chatId: chat.id, title, createdAt: new Date().toISOString(), payload };
      state.tickets.unshift(ticket);
      chat.ticketId = ticket.id;
      saveState();
      counts();
      renderKpis();

      // Switch to created tickets view to show the result
      route("createdTickets");
    });

    $("#closeChatBtn").addEventListener("click", () => {
      const chat = state.chats.find(c => c.id === state.selectedChatId);
      if (!chat) return;
      chat.status = "closed";
      saveState();
      counts();
      renderKpis();
      route("closedTickets");
    });

    renderChat();
  };

  const view_openChats = () => {
    setActiveNav("openChats");
    state.view = "openChats";
    saveState();

    const openChats = state.chats.filter(c => c.status === "open");
    $("#primaryPanel").innerHTML = `
      <h2>Open Chats</h2>
      <p class="small">Re-open a chat in the main window. (Prototype list)</p>
      <div class="hr"></div>
      ${openChats.length ? `
        <div>
          ${openChats.map(c => `
            <div class="card" style="padding:12px;margin:10px 0;border-radius:12px">
              <div style="display:flex;justify-content:space-between;gap:12px;align-items:center">
                <div>
                  <div style="font-weight:800">${escapeHtml(c.name)}</div>
                  <div class="small">Created: ${escapeHtml(new Date(c.createdAt).toLocaleString())}</div>
                </div>
                <div style="display:flex;gap:10px">
                  <button class="btn secondary" data-open="${c.id}">Open</button>
                  <button class="btn danger" data-close="${c.id}">Close</button>
                </div>
              </div>
            </div>
          `).join("")}
        </div>
      ` : `<div class="small">No open chats. Start with <strong>New Issue</strong>.</div>`}
    `;

    $$("[data-open]").forEach(btn => btn.addEventListener("click", () => {
      state.selectedChatId = btn.dataset.open;
      saveState();
      // show selected chat in New Issue view (chat UI is there)
      route("newIssue", { reuseSelected: true });
    }));

    $$("[data-close]").forEach(btn => btn.addEventListener("click", () => {
      const chat = state.chats.find(c => c.id === btn.dataset.close);
      if (chat) chat.status = "closed";
      saveState();
      counts();
      renderKpis();
      route("openChats");
    }));
  };

  const view_createdTickets = () => {
    setActiveNav("createdTickets");
    state.view = "createdTickets";
    saveState();

    const tickets = state.tickets;
    $("#primaryPanel").innerHTML = `
      <h2>Created Tickets</h2>
      <p class="small">Not connected to a ticketing system yet — showing the payload Pin would send.</p>
      <div class="hr"></div>

      ${tickets.length ? tickets.map(t => `
        <div class="card" style="padding:12px;margin:10px 0;border-radius:12px">
          <div style="display:flex;justify-content:space-between;gap:12px;align-items:flex-start">
            <div>
              <div style="font-weight:900">${escapeHtml(t.id)} — ${escapeHtml(t.title)}</div>
              <div class="small">Created: ${escapeHtml(new Date(t.createdAt).toLocaleString())}</div>
            </div>
            <button class="btn secondary" data-viewticket="${t.id}">View</button>
          </div>
          <div class="small" style="margin-top:10px">Chat: <span class="mono">${escapeHtml(t.chatId)}</span></div>
        </div>
      `).join("") : `<div class="small">No tickets yet. Generate one from <strong>New Issue</strong>.</div>`}

      <div class="hr"></div>
      <div class="small">Integration note: later this maps to the backend flow engine output (ticket schema) and posts to your help desk connector.</div>
    `;

    $$("[data-viewticket]").forEach(btn => btn.addEventListener("click", () => {
      const ticket = state.tickets.find(t => t.id === btn.dataset.viewticket);
      if (!ticket) return;
      $("#primaryPanel").innerHTML = `
        <h2>Ticket ${escapeHtml(ticket.id)}</h2>
        <p class="small"><strong>${escapeHtml(ticket.title)}</strong></p>
        <div class="hr"></div>
        <pre class="card" style="padding:12px;border-radius:12px;overflow:auto;max-height:520px">${escapeHtml(JSON.stringify(ticket.payload, null, 2))}</pre>
        <div style="margin-top:12px;display:flex;gap:10px">
          <button class="btn secondary" id="backTickets">Back</button>
          <button class="btn" id="openChatFromTicket">Open Chat</button>
        </div>
      `;
      $("#backTickets").addEventListener("click", () => route("createdTickets"));
      $("#openChatFromTicket").addEventListener("click", () => {
        state.selectedChatId = ticket.chatId;
        saveState();
        route("newIssue", { reuseSelected: true });
      });
    }));
  };

  const view_closedTickets = () => {
    setActiveNav("closedTickets");
    state.view = "closedTickets";
    saveState();

    const closedChats = state.chats.filter(c => c.status === "closed");
    $("#primaryPanel").innerHTML = `
      <h2>Closed Tickets</h2>
      <p class="small">Placeholder view. Shows closed chats for later reference.</p>
      <div class="hr"></div>

      ${closedChats.length ? closedChats.map(c => `
        <div class="card" style="padding:12px;margin:10px 0;border-radius:12px">
          <div style="display:flex;justify-content:space-between;gap:12px;align-items:center">
            <div>
              <div style="font-weight:800">${escapeHtml(c.name)}</div>
              <div class="small">Closed • Created: ${escapeHtml(new Date(c.createdAt).toLocaleString())}</div>
            </div>
            <button class="btn secondary" data-reopen="${c.id}">Re-open</button>
          </div>
        </div>
      `).join("") : `<div class="small">Nothing closed yet.</div>`}
    `;

    $$("[data-reopen]").forEach(btn => btn.addEventListener("click", () => {
      const chat = state.chats.find(c => c.id === btn.dataset.reopen);
      if (chat) chat.status = "open";
      state.selectedChatId = btn.dataset.reopen;
      saveState();
      counts();
      renderKpis();
      route("newIssue", { reuseSelected: true });
    }));
  };

  // Router
  const route = (view, opts = {}) => {
    counts();
    renderKpis();

    if (view === "logout") return logout();
    if (view === "newIssue" && opts.reuseSelected) {
      // re-render newIssue but keep selected chat
      setActiveNav("newIssue");
      state.view = "newIssue";
      saveState();
      // render base UI then bind selected chat
      $("#primaryPanel").innerHTML = `
        <h2>Chat</h2>
        <p class="small">Resumed chat. (Prototype)</p>
        <div class="hr"></div>
        <div class="chat">
          <div class="chat-log" id="chatLog"></div>
          <div class="chat-input">
            <textarea id="chatText" placeholder="Continue the conversation..."></textarea>
            <button id="sendBtn" class="btn">Send</button>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap">
            <button id="createTicketBtn" class="btn secondary" type="button">Generate Ticket (demo)</button>
            <button id="closeChatBtn" class="btn secondary" type="button">Close Chat</button>
          </div>
        </div>
      `;

      const renderChat = () => {
        const chat = state.chats.find(c => c.id === state.selectedChatId);
        if (!chat) return;
        $("#primaryPanel h2").textContent = chat.name;
        const log = $("#chatLog");
        log.innerHTML = chat.messages.map(m => `
          <div class="msg ${m.role === "user" ? "user" : "bot"}">
            <div>${m.role === "user" ? "<strong>You</strong>" : "<strong>Pin</strong>"}: ${escapeHtml(m.text)}</div>
            <div class="meta">${escapeHtml(new Date(m.ts).toLocaleString())}</div>
          </div>
        `).join("");
        log.scrollTop = log.scrollHeight;
      };

      const addBotFollowUp = () => {
        const chat = state.chats.find(c => c.id === state.selectedChatId);
        if (!chat) return;
        chat.messages.push({ role: "bot", text: "Thanks — what changed right before this started happening?", ts: new Date().toISOString() });
        saveState();
        renderChat();
      };

      const send = () => {
        const textArea = $("#chatText");
        const text = textArea.value.trim();
        if (!text) return;
        const chat = state.chats.find(c => c.id === state.selectedChatId);
        if (!chat) return;
        chat.messages.push({ role: "user", text, ts: new Date().toISOString() });
        saveState();
        counts();
        renderKpis();
        renderChat();
        textArea.value = "";
        addBotFollowUp();
      };

      $("#sendBtn").addEventListener("click", send);
      $("#chatText").addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
      });

      $("#createTicketBtn").addEventListener("click", () => {
        const chat = state.chats.find(c => c.id === state.selectedChatId);
        if (!chat) return;

        const title = chat.name || "Issue";
        const payload = {
          company: session.company,
          requester: { email: session.email, department: session.dept },
          title,
          createdAt: new Date().toISOString(),
          transcript: chat.messages,
          integration: { status: "stub", target: "ticketing-system" }
        };

        const ticket = { id: `TCK-${Math.floor(Math.random()*90000+10000)}`, chatId: chat.id, title, createdAt: new Date().toISOString(), payload };
        state.tickets.unshift(ticket);
        chat.ticketId = ticket.id;
        saveState();
        counts();
        renderKpis();
        route("createdTickets");
      });

      $("#closeChatBtn").addEventListener("click", () => {
        const chat = state.chats.find(c => c.id === state.selectedChatId);
        if (!chat) return;
        chat.status = "closed";
        saveState();
        counts();
        renderKpis();
        route("closedTickets");
      });

      renderChat();
      return;
    }

    // Standard view switch
    const views = {
      newIssue: view_newIssue,
      openChats: view_openChats,
      createdTickets: view_createdTickets,
      closedTickets: view_closedTickets,
    };

    (views[view] || view_newIssue)();
  };

  // Nav click handlers
  $$("aside .nav button[data-view]").forEach(btn => {
    btn.addEventListener("click", () => route(btn.dataset.view));
  });

  // Initial route
  counts();
  renderKpis();
  route(state.view || "newIssue");
})();