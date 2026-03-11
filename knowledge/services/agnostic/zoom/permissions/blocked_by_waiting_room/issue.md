---
doc_id: KB-Z1B2W3R4-blocked_waiting_room
title: "Permissions — Zoom — Blocked by Waiting Room"
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
- waiting-room
- blocked
- sso
- guest
- permission
- identity
urls: []
---

# Blocked by Waiting Room

# Zoom (Access Control)

Use this guide to troubleshoot scenarios where a user is stuck in a Zoom Waiting Room indefinitely, or is being forced into a Waiting Room despite being an internal employee.

### Blocked by Waiting Room

## Severity:
`S3` — Minor degradation; the user is unable to join the meeting on time, which may cause them to miss critical information.

## Symptoms
- The user sees a screen stating: Please wait, the meeting host will let you in soon.
- The host does not receive a notification that the user is waiting.
- Internal employees are being held in the waiting room while others join directly.

## Quick checks
- Verify the user is logged into the Zoom desktop client with their corporate SSO account. Users who join as "Guests" or via personal accounts are often automatically routed to the Waiting Room by security policy.
- Check if the meeting host is currently in the meeting. If the host has not joined, everyone will be held in the waiting room.


## Fix steps
1. Instruct the user to leave the meeting.
2. Open the Zoom desktop app, click their profile icon, and select Sign Out.
3. Click Sign In, select Sign In with SSO, and use the corporate domain to log back in.
4. Attempt to join the meeting again. If configured correctly, SSO users will bypass the waiting room.
5. (Host Action): If the user is an external guest, the host must click the Participants button in the meeting toolbar.
6. Look at the top of the participants list and click Admit next to the user's name.
7. To avoid this for all participants, the host can click Security in the toolbar and uncheck Enable Waiting Room (if permitted by corporate policy).

## Escalate if
- The host is clicking Admit but the user remains stuck on the waiting screen.
- The user is confirmed to be on SSO but is still forced into the waiting room for all internal meetings.
- The Waiting Room settings are greyed out and locked at the account level.

## Ticket fields to capture (when escalating)
- Meeting ID: (The 11-digit number)
- User Login Status: (SSO vs Guest)
- Host Presence: (Was the host in the meeting? Yes/No)