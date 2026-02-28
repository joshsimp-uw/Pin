---
doc_id: KB-C37206B5FE-vpn_won_t_
title: "Remote Access \u2014 Cisco Secure Client (AnyConnect) VPN \u2014 VPN won't\
  \ connect"
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
- vpn_won_t_connect
dns:
- vpn.acme.com
---

# VPN won't connect

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

### VPN won't connect

## Severity:
`S2` — Major degradation; user work significantly impacted. Escalate within same business day.

## Symptoms
- Connection fails
- Timeout errors
- Stuck at 'Connecting'

## Quick checks
- Confirm your internet works by opening a few websites
- Restart your computer

## Fix steps
1. Confirm you entered **vpn.acme.com** exactly.
2. Restart your computer.
3. Try again from a different network if possible (mobile hotspot) to rule out home ISP blocking.

## Escalate if
- The error repeats after restart
- You are blocked from all work because VPN is required

## Ticket fields to capture (when escalating)
- Error text: Copy/paste or screenshot
- Network type: Home Wi‑Fi / hotspot / other
