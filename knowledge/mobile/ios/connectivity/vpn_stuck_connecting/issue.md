---
doc_id: KB-Q7R8S9T0-vpn_stuck
title: "Connectivity — iOS — VPN Stuck Connecting"
service: Mobile Connectivity
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- ios
- vpn
- remote
- access
- network
- cisco
urls: []
---

# VPN Stuck Connecting

# iOS (Remote Access)

Use this guide to assist users who are trying to access internal corporate resources on their iPhone, but the mobile VPN client is hung or failing to route traffic.

### VPN Stuck Connecting

## Severity:
`S2` — High impact; the remote user cannot access internal web apps, intranet sites, or synced file shares on their mobile device.

## Symptoms
- The VPN app (e.g., Cisco Secure Client, GlobalProtect) says "Connecting..." endlessly but never turns green.
- The VPN switch in the iOS Settings app continuously toggles itself off immediately after the user turns it on.
- The VPN says it is connected, but Safari returns "Server cannot be found" for all internal URLs.

## Quick checks
- Open Safari and load a public website like apple.com to verify the iPhone has a working cellular or Wi-Fi internet connection first.
- Check if the user is using a public hotel or airport Wi-Fi network that requires them to accept terms on a "captive portal" page before the VPN can tunnel out.

## Fix steps
1. Open the corporate VPN app on the iPhone and tap the toggle to turn it Off or Cancel the connection attempt.
2. Force close the VPN app by swiping up from the bottom of the screen to open the app switcher, then swiping the app card up and away.
3. Open the iOS Settings app, tap General, scroll down, and tap VPN & Device Management.
4. Tap VPN to see the list of profiles. Ensure the correct corporate profile is checked.
5. If the Status says Connecting, toggle the switch off here to force-kill the hung connection.
6. Re-open the dedicated VPN app from the home screen and attempt to connect again. Enter any required MFA prompts.

## Escalate if
- The VPN profile is entirely missing from the General > VPN & Device Management menu.
- The app immediately crashes back to the home screen every time the user attempts to open it.
- The user connects successfully but is prompted for a "Certificate Password" they do not have.

## Ticket fields to capture (when escalating)
- iOS Version: (e.g., iOS 17.4)
- VPN Client App: (e.g., Cisco Secure Client)
- Network Connection: (Wi-Fi vs. Cellular 5G/LTE)
- Error Message: (Any text displayed in the VPN app logs)