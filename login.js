(() => {
  const $ = (id) => document.getElementById(id);

  const now = new Date();
  $("year").textContent = String(now.getFullYear());
  $("buildDate").textContent = now.toISOString();

  const defaults = {
    company: "ACME",
    email: "jane.doe@acme.com",
    dept: "IT",
  };

  // Load remembered values if present
  const stored = JSON.parse(localStorage.getItem("pin_demo_login") || "null");
  if (stored) {
    $("company").value = stored.company || defaults.company;
    $("email").value = stored.email || defaults.email;
    $("dept").value = stored.dept || defaults.dept;
  } else {
    $("company").value = defaults.company;
    $("email").value = defaults.email;
  }

  $("resetBtn").addEventListener("click", () => {
    localStorage.removeItem("pin_demo_login");
    $("company").value = defaults.company;
    $("email").value = defaults.email;
    $("dept").value = defaults.dept;
    $("password").value = "";
  });

  $("loginBtn").addEventListener("click", () => {
    const company = $("company").value.trim() || defaults.company;
    const email = $("email").value.trim() || defaults.email;
    const dept = $("dept").value;

    const session = {
      company,
      email,
      dept,
      // stub auth: mark logged in
      isAuthenticated: true,
      issuedAt: new Date().toISOString(),
    };

    localStorage.setItem("pin_demo_login", JSON.stringify({ company, email, dept }));
    localStorage.setItem("pin_session", JSON.stringify(session));

    window.location.href = "./app.html";
  });
})();