---
doc_id: KB-F6G7H8I9J0-vpn_reset
title: "Connectivity — Endpoints — VPN Connection Reset"
service: Endpoint Connectivity
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- vpn
- remote
- network
- access
- connection
urls: []
---

# VPN Connection Reset

# Endpoints (Remote Access)

Use this guide to troubleshoot situations where the corporate VPN client is hung, failing to authenticate, or connected but not routing traffic correctly.

### VPN Reset

## Severity:
`S2` — High impact; remote users are entirely cut off from internal corporate resources.

## Symptoms
- The VPN client is stuck on "Connecting..." or "Securing connection..." for several minutes.
- The user is prompted for MFA (Multi-Factor Authentication), but the push notification never arrives.
- The VPN indicates it is connected, but the user cannot access intranet sites or network drives.

## Quick checks
- Open a web browser to confirm the user has a working local internet connection.
- Check the IT status page to ensure there are no global VPN server outages.

## Fix steps
1. Open the VPN client application and click Disconnect or Cancel.
2. Locate the VPN icon in the system tray (bottom right, near the clock), right-click it, and select Quit or Exit.
3. Open the Start menu, search for Services, and open the app.
4. Scroll down to find your VPN service (e.g., Cisco AnyConnect Secure Mobility Agent).
5. Right-click the service and select Restart.
6. Reopen the VPN client from the Start menu and attempt to connect again.

## Escalate if
- The VPN client immediately crashes upon opening.
- The user receives an explicit "Account locked" or "Certificate invalid" error.
- The fix steps resolve the issue temporarily, but the connection drops every few minutes.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- ISP / Local Network: (e.g., Comcast home network, or Public Hotel Wi-Fi)
- VPN Client Version: (Found in the app's About section)
- Error Code: (Any specific numerical error provided by the client)