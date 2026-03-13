---
doc_id: KB-Z5R6E7C8-recover_recording
title: "General — Zoom — Recover Deleted Cloud Recording"
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
- recording
- recover
- trash
- deleted
- cloud
urls: []
---

# Recover Deleted Cloud Recording

# Zoom (Data Recovery)

Use this guide to help users retrieve a Zoom cloud recording that was accidentally deleted or automatically moved to the trash due to a retention policy.

### Recover Deleted Cloud Recording

## Severity:
`S2` — High impact; loss of critical meeting data, legal evidence, or training materials that cannot be recreated.

## Symptoms
- The user navigates to their "Recordings" list and the specific meeting is gone.
- A shared link to a recording now displays "This recording does not exist."

## Quick checks
- Confirm the deletion occurred within the last 30 days. Zoom permanently purges the trash after 30 days.

## Fix steps
1. Instruct the user to log into the Zoom web portal at company.zoom.us.
2. Click Recordings in the left-hand navigation pane.
3. Click the Cloud Recordings tab.
4. Look for a small link in the top right of the list that says Trash. Click it.
5. Find the meeting recording in the trash list.
6. Click Recover on the right side of the meeting entry.
7. Click Recover again in the confirmation popup.
8. The recording will return to the active "Cloud Recordings" list and any previous share links will become active again.

## Escalate if
- The Trash folder is empty or the recording is not listed (indicating it was either a local recording or was deleted more than 30 days ago).
- The user receives an "Access Denied" error when trying to access the Trash.

## Ticket fields to capture (when escalating)
- Meeting Date: (When was it recorded?)
- Meeting ID: (The 11-digit ID)
- Storage Quota: (Is the user's cloud storage full?)