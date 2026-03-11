---
doc_id: KB-E5F6G7H8I9-map_drive
title: "Connectivity — Endpoints — Map Network Drive"
service: Endpoint Connectivity
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- network
- drive
- share
- storage
- file explorer
urls: []
---

# Map Network Drive

# Endpoints (File Access)

Use this guide to manually reconnect shared department drives (like the S: or P: drive) when Group Policy fails to mount them automatically at login.

### Map Network Drives

## Severity:
`S3` — Minor degradation; user cannot access shared department files, halting specific workflows.

## Symptoms
- A previously available drive letter is missing from File Explorer under "This PC".
- A "Could not reconnect all network drives" notification appears in the system tray at startup.
- Double-clicking an existing drive letter results in a red X and an "Unavailable" error.

## Quick checks
- Confirm the user is connected to the corporate network via office LAN/Wi-Fi or an active VPN connection.
- Verify the user actually has approved access to the requested share.

## Fix steps
1. Open File Explorer and select This PC from the left-hand navigation pane.
2. Click the three horizontal dots (...) in the top menu bar and select Map network drive.
3. In the Drive list, select the standard letter used by your department for this share.
4. In the Folder box, type the exact path of the server and share (e.g., `\\fileserver01\marketing`).
5. Ensure Reconnect at sign-in is checked so the drive persists after a reboot.
6. Click Finish.

## Escalate if
- The user receives an "Access Denied" error when attempting to map the drive.
- The system prompts for network credentials but rejects the user's correct standard login.
- The server path cannot be reached, resulting in a "Network path was not found" error.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Drive Letter: (e.g., M:)
- Network Path: (e.g., `\\server\share`)
- Specific Error: (e.g., Access Denied vs. Path Not Found)