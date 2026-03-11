---
doc_id: KB-C1P2O3R4-captive_portal
title: "Connectivity — Cisco VPN — Captive Portal Detected"
service: Network Access
audience:
- End Users
- Helpdesk
owner: Network Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- cisco
- anyconnect
- vpn
- wifi
- captive-portal
- hotel
- airport
- login
urls: []
---

# Captive Portal Detected

# Cisco AnyConnect (Public Wi-Fi Connectivity)

Use this guide to troubleshoot scenarios where the VPN client fails to connect on public Wi-Fi (hotels, airports, coffee shops) because the network requires a web-based login before allowing traffic.

### Captive Portal Detected

## Severity:
`S3` — Minor degradation; the user is blocked from the VPN until they complete the local network's authentication.

## Symptoms
- AnyConnect displays a notification: "The service provider in your current location is restricting access to the internet."
- The "Connect" button results in a "Socket Error" or "Connection Timeout."
- The user can browse to Google, but any internal corporate site fails to load.

## Quick checks
- Ask the user to open a fresh web browser tab and navigate to a non-HTTPS site (like example.com) to force the Wi-Fi login page to appear.
- Check if the user has "Captive Portal Detection" enabled in the AnyConnect preferences.


## Fix steps
1. Disconnect the VPN if it is currently trying to connect.
2. Open a web browser (Chrome, Edge, or Safari).
3. Attempt to load any public website. The hotel or airport "Terms of Service" or login page should appear.
4. Complete the required login or click the "I Agree" button.
5. Once the browser successfully loads a public page, go back to the Cisco AnyConnect window.
6. Click Connect. The VPN tunnel should now establish successfully.

## Escalate if
- The captive portal page refuses to load even after multiple browser refreshes.
- The user completes the portal login, but AnyConnect still reports "Restricted access."
- The corporate security policy forbids connecting to open Wi-Fi networks that utilize captive portals.

## Ticket fields to capture (when escalating)
- Network Location: (e.g., Marriott Guest Wi-Fi)
- OS Version: (e.g., Windows 10)
- Browser Used: (e.g., Microsoft Edge)