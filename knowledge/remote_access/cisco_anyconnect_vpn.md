---
doc_id: KB-C37206B5FE
title: Remote Access — Cisco Secure Client (AnyConnect) VPN
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
dns:
  - vpn.acme.com
---

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

## Common issues

### VPN won't connect

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Connection fails
- Timeout errors
- Stuck at 'Connecting'

**Quick checks**
- Confirm your internet works by opening a few websites
- Restart your computer

**Fix steps**
1. Confirm you entered **vpn.acme.com** exactly.
2. Restart your computer.
3. Try again from a different network if possible (mobile hotspot) to rule out home ISP blocking.

**Escalate if**
- The error repeats after restart
- You are blocked from all work because VPN is required

**Ticket fields to capture (when escalating)**
- **Error text:** Copy/paste or screenshot
- **Network type:** Home Wi‑Fi / hotspot / other

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
