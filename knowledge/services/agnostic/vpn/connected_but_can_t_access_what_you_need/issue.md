---
doc_id: KB-C37206B5FE-connected_
title: "Remote Access \u2014 Cisco Secure Client (AnyConnect) VPN \u2014 Connected\
  \ but can't access what you need"
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
- connected_but_can_t_access_what_you_need
dns:
- vpn.acme.com
---

# Connected but can't access what you need

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

### Connected but can't access what you need

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- VPN shows connected
- Internal site/app still fails
- Only one app affected

**Quick checks**
- Disconnect and reconnect VPN
- Confirm the resource actually requires VPN

**Fix steps**
1. Disconnect VPN and reconnect.
2. Try the resource again.
3. If only one internal app is failing, report it with the name/URL of the app.

**Escalate if**
- Multiple internal resources fail while connected
- VPN disconnects repeatedly

**Ticket fields to capture (when escalating)**
- **Resource name/URL:** What you are trying to reach
- **Does VPN stay connected?:** Yes/No


## Escalation logic (for chatbot / help desk)
- VPN required for work and cannot connect → **S2**
- Suspicious authentication behavior (unexpected prompts / compromise) → **S1**
- Single app issue while VPN connected → **S3** (route to application owner)
