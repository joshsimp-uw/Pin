(() => {
  const $ = (id) => document.getElementById(id);

  const now = new Date();
  $("year").textContent = String(now.getFullYear());
  $("buildDate").textContent = now.toISOString();

  const defaults = {
    company: "ACME",
    email: "jane.doe@acme.com",
    // dept: "IT",
  };

  // Load remembered values if present
  const stored = JSON.parse(localStorage.getItem("pin_demo_login") || "null");
  if (stored) {
    $("company").value = stored.company || defaults.company;
    $("email").value = stored.email || defaults.email;
    // $("dept").value = stored.dept || defaults.dept;
  } else {
    $("company").value = defaults.company;
    $("email").value = defaults.email;
  }

  $("resetBtn").addEventListener("click", () => {
    localStorage.removeItem("pin_demo_login");
    $("company").value = defaults.company;
    $("email").value = defaults.email;
    // $("dept").value = defaults.dept;
    $("password").value = "";
  });

  $("loginBtn").addEventListener("click", () => {
    const company = $("company").value.trim() || defaults.company;
    const email = $("email").value.trim() || defaults.email;
    const password = $("password").value;

    (async () => {
      try {
        const r = await fetch("/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ org_id: company, email, password })
        });
        if (!r.ok) {
          const t = await r.text().catch(() => "");
          throw new Error(t || `Login failed (${r.status})`);
        }
        const data = await r.json();
        const user = data.user || {};

        const session = {
          company,
          org_id: user.org_id || company,
          email: user.email || email,
          role: user.role || "end_user",
          token: data.token,
          isAuthenticated: true,
          issuedAt: new Date().toISOString(),
        };

        localStorage.setItem("pin_demo_login", JSON.stringify({ company, email }));
        localStorage.setItem("pin_session", JSON.stringify(session));

        window.location.href = "./app.html";
      } catch (e) {
        alert(String(e?.message || e));
      }
    })();
  });
})();
