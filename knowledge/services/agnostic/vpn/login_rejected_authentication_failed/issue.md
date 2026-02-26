---
doc_id: KB-C37206B5FE-login_reje
title: "Remote Access \u2014 Cisco Secure Client (AnyConnect) VPN \u2014 Login rejected\
  \ / authentication failed"
service: Cisco AnyConnect VPN
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- vpn
- cisco
- anyconnect
- remote_access
- login_rejected_authentication_failed
dns:
- vpn.acme.com
---

# Login rejected / authentication failed

# Cisco Secure Client (AnyConnect) VPN

## VPN gateway
- **vpn.acme.com**

## When you need VPN
- When an internal application requires it
- When instructed by IT

## Connect steps
1. Open **Cisco Secure Client**.
2. In the connection box, enter: **vpn.acme.com**
3. Sign in with your ACME email and password.
4. Approve the MFA prompt.

### Login rejected / authentication failed

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Username/password rejected
- MFA prompt never appears
- Account disabled messages

**Quick checks**
- Confirm you can sign in to https://portal.office.com (checks your account)
- Check Caps Lock

**Fix steps**
1. Try signing in to https://portal.office.com. If that fails, fix your account sign-in first.
2. If portal sign-in works, try VPN again and approve MFA promptly.

**Escalate if**
- You cannot sign in to portal.office.com
- Account disabled or suspicious activity suspected

**Ticket fields to capture (when escalating)**
- **Can sign in to portal.office.com:** Yes/No
- **Any error code:** As shown
