---
doc_id: KB-V1P2N3G4-incorrect_gateway
title: "Configuration — Cisco VPN — Incorrect Gateway Address"
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
- gateway
- address
- server
- connection
urls: []
---

# Incorrect Gateway Address

# Cisco AnyConnect (Server Configuration)

Use this guide to assist users who are unable to connect because their VPN client is pointing to an old, decommissioned, or mistyped server URL.

### Incorrect Gateway Address

## Severity:
`S3` — Minor degradation; the user is blocked from connecting until the address is corrected, but the software itself is functioning.

## Symptoms
- The user clicks Connect and immediately receives an error: "The VPN server may be unreachable" or "Connection attempt has failed."
- The dropdown menu in the AnyConnect window is empty or contains an address like "vpn.oldcompany.com".
- The user is trying to use a regional gateway (e.g., Europe) while they are located in North America.

## Quick checks
- Verify the exact URL the user has typed into the box. Common typos include missing dots or using "http" instead of "https".
- Check if the user is connected to a network that requires a login (captive portal) before they can reach the gateway.

## Fix steps
1. Open the Cisco AnyConnect / Secure Client window from the system tray.
2. If the address box is editable, delete the current text.
3. Type the correct corporate gateway address (e.g., vpn.companyname.com).
4. Click Connect.
5. If the login prompt appears, the address is correct.
6. If the user cannot edit the box, they must select the correct entry from the dropdown menu if multiple profiles are available.
7. Instruct the user to always use the primary global gateway unless specifically told otherwise by their manager.

## Escalate if
- The user enters the correct address but the client automatically reverts it to the old, broken address upon restart.
- The correct gateway address is unreachable for all users in a specific geographic region (suggesting a regional ISP outage or DNS issue).
- The address box is greyed out and contains the wrong information, preventing any manual correction.

## Ticket fields to capture (when escalating)
- Attempted Gateway: (e.g., vpn.east.company.com)
- Error Message: (Exact text of the failure)
- User Location: (City/State)