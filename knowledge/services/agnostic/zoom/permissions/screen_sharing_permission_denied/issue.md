---
doc_id: KB-Z5S6P7D8-screenshare_denied
title: "Permissions — Zoom — Screen Sharing Permission Denied"
service: Unified Communications
audience:
- End Users
- Helpdesk
owner: Collaboration Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- zoom
- screenshare
- permission
- denied
- host
- participant
- security
urls: []
---

# Screen Sharing Permission Denied

# Zoom (Meeting Permissions)

Use this guide to resolve issues where a participant attempts to share their screen but receives an error stating that the host has disabled this feature.

### Screen Sharing Permission Denied

## Severity:
`S3` — Minor degradation; the meeting can proceed, but the user cannot present data or demonstrate a technical issue.

## Symptoms
- A popup appears saying: Host disabled participant screen sharing.
- The Share Screen button is greyed out or does not respond.
- This often happens in larger meetings where the host has enabled strict security defaults.

## Quick checks
- Verify if the user is a co-host. Co-hosts usually have automatic sharing rights.
- Check if the meeting is a "Webinar" format, which has much stricter sharing controls than a standard "Meeting."


## Fix steps
1. (Host Action): Click the Security icon in the meeting toolbar.
2. Under the section Allow participants to:, check the box for Share Screen. This change is effective immediately for all participants.
3. (Alternative Host Action): Click the arrow next to the Share Screen button and select Advanced Sharing Options.
4. Under Who can share?, change the selection to All Participants.
5. (Individual User): If the host has enabled sharing but the user still cannot share, check OS-level permissions.
6. (macOS): Go to System Settings > Privacy & Security > Screen Recording and ensure Zoom is toggled to On.
7. (Windows): Ensure no third-party "Privacy" apps are blocking Zoom's ability to capture the desktop.

## Escalate if
- The host enables sharing in the security menu, but participants still receive the "Host disabled" error.
- The host is unable to find the sharing options in their menu.
- The user is on macOS and has enabled permissions, but Zoom still fails to capture the screen (requires a TCC database reset).

## Ticket fields to capture (when escalating)
- OS Platform: (e.g., macOS Sonoma or Windows 11)
- Meeting Type: (Standard Meeting vs Webinar)
- Host Setting Status: (Was "All Participants" enabled?)