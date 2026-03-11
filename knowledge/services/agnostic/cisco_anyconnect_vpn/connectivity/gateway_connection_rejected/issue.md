---
doc_id: KB-G1C2R3J4-gateway_rejected
title: "Connectivity — Cisco VPN — Gateway Connection Rejected"
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
- rejected
- clock-sync
- time
- ssl
- certificate
urls: []
---

# Gateway Connection Rejected

# Cisco AnyConnect (Security & Handshake)

Use this guide to resolve the "Secure Gateway has rejected the connection attempt" error, which most commonly occurs when there is a significant time mismatch between the user's computer and the VPN server.

### Gateway Connection Rejected

## Severity:
`S3` — Minor degradation; the user is blocked from connecting due to a local configuration mismatch.

## Symptoms
- AnyConnect displays a red error banner: "The Secure Gateway has rejected the connection attempt. A new connection attempt to the same or another Secure Gateway is needed."
- The error occurs almost immediately after clicking Connect, before the user can even enter their password.

## Quick checks
- Look at the Windows system clock in the bottom right corner. Compare it to your own clock or a reliable time source. If it is off by more than 5 minutes, the connection will fail.
- Verify if the user is using an extremely outdated version of AnyConnect that the gateway no longer supports.

## Fix steps
1. Right-click the time/date in the Windows taskbar and select Adjust date/time.
2. Ensure the toggles for Set time automatically and Set time zone automatically are both turned On.
3. Click the Sync now button under "Synchronize your clock."
4. Close the AnyConnect client completely.
5. Re-launch AnyConnect and attempt to connect again.
6. If the error persists, check for any expired personal certificates in the Windows Certificate Manager (certmgr.msc) that might be being presented to the gateway incorrectly.

## Escalate if
- The user's time is perfectly synced, but the gateway still rejects the connection.
- The error only happens when the user tries to connect to one specific regional gateway but works on others.
- The "Sync now" button in Windows fails with a "Time synchronization failed" error.

## Ticket fields to capture (when escalating)
- System Time Offset: (How many minutes was the clock off?)
- Gateway URL: (Which server rejected the connection?)
- Client Version: (e.g., v4.10)