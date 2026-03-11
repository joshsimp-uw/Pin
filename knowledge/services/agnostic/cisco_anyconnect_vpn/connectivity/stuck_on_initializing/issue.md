---
doc_id: KB-S1T2I3N4-stuck_initializing
title: "Connectivity — Cisco VPN — Stuck on Initializing"
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
- stuck
- initializing
- contacting
- dtls
- firewall
urls: []
---

# Stuck on Initializing

# Cisco AnyConnect (State Machine Troubleshooting)

Use this guide to troubleshoot scenarios where AnyConnect remains stuck on "Initializing..." or "Contacting..." for several minutes without ever reaching the username/password prompt.

### Stuck on Initializing

## Severity:
`S3` — Minor degradation; the user's workflow is delayed as the client fails to negotiate the initial encrypted tunnel.

## Symptoms
- The status message in the AnyConnect window never changes from "Initializing" or "Contacting [Gateway]."
- The "Cancel" button is responsive, but re-attempting the connection leads to the same hang.
- The user is working from a location with a restrictive firewall (like a library or a strictly managed home router).

## Quick checks
- Verify the user's internet connection is stable. A high-latency or "dropping" connection will cause the initialization to hang.
- Check if the user has any other VPN clients (like NordVPN or GlobalProtect) running simultaneously, which can conflict with the network drivers.

## Fix steps
1. Close AnyConnect.
2. Open the Windows Task Manager (Ctrl+Shift+Esc), go to the Services tab, find "vpnagent" (Cisco AnyConnect Secure Client Agent), right-click it, and select Restart.
3. If the hang persists, the local router may be blocking UDP 443 (DTLS). 
4. Open AnyConnect, click the gear icon, and go to the Preferences tab.
5. Uncheck the box for Allow bypass of the VPN (if applicable) and ensure no other conflicting settings are active.
6. Re-attempt the connection. If it still hangs, try connecting via a mobile hotspot to see if the issue is specific to the user's local Wi-Fi router.

## Escalate if
- The client works on a mobile hotspot but fails on the home network (requires the user to enable "IPsec Passthrough" or "VPN Passthrough" on their home router).
- The "Cisco AnyConnect Secure Client Agent" service fails to start or keeps stopping automatically.
- DART logs show a "Base Filtering Engine" (BFE) error in Windows.

## Ticket fields to capture (when escalating)
- Status Message: (e.g., Initializing vs Contacting)
- Hotspot Test Result: (Did it work on a different network? Yes/No)
- Conflicting VPNs: (Are other VPNs installed?)