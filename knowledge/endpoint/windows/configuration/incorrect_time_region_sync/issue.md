---
doc_id: KB-C3D4E5F6G7-time_sync
title: "Configuration — Endpoints — System Time & Region Sync"
service: Endpoint Configuration
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- time
- clock
- region
- sync
- certificate
urls: []
---

# System Time & Region Sync

# Endpoints (Configuration & Security)

Use this guide to resolve system clock drift. Incorrect time often causes security certificate errors in browsers and prevents login to SSO services (Okta/Azure AD).

### Time Region Sync

## Severity:
`S2` — High impact; incorrect time often prevents authentication to corporate tools.

## Symptoms
- "Your clock is ahead/behind" errors in Chrome or Edge.
- Unable to log in to Microsoft Teams or Outlook (MFA/Token mismatch).
- System clock shows the wrong hour or date after waking from sleep.

## Quick checks
- Check if the user is currently on a VPN (which may affect NTP sync).
- Ensure the device has an active internet connection.

## Fix steps
1. Right-click the time/date in the Taskbar and select Adjust date and time.
2. Ensure Set time automatically is toggled to On.
3. Ensure Set time zone automatically is toggled to On.
4. Scroll down to "Synchronize your clock" and click the Sync now button.
5. If the sync fails, open Command Prompt (Admin) and run:
   `w32tm /resync`

## Escalate if
- The time resets to a specific date (e.g., Jan 1, 2000) every time the computer restarts (possible CMOS battery failure).
- The "Sync now" button returns an "Access Denied" or "Time synchronization failed" error repeatedly.
- The user is unable to change time settings due to Group Policy restrictions.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Current System Time: (The time currently shown on the device)
- Actual Local Time: (The real time)
- Error Code: (e.g., 0x800705B4 during sync)