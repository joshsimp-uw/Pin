---
doc_id: KB-Z1M2T3L4-meeting_timeout
title: "General — Zoom — Meeting 40 Minute Timeout"
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
- timeout
- limit
- basic
- licensed
- upgrade
- 40-minutes
urls: []
---

# Meeting 40 Minute Timeout

# Zoom (Account Licensing)

Use this guide to assist users whose meetings are being cut off at exactly 40 minutes, indicating they are using a Basic account instead of a corporate Licensed account.

### Meeting 40 Minute Timeout

## Severity:
`S3` — Minor degradation; the user can restart a new meeting, but the disruption is unprofessional and hinders long-form collaboration.

## Symptoms
- A warning appears in the meeting stating "Your meeting will end in 10 minutes."
- The meeting abruptly closes for all participants after 40 minutes of duration.
- The user's profile in the Zoom client shows a "Basic" tag next to their name.

## Quick checks
- Click the user's profile picture in the top right of the Zoom app and check the account type. 
- Verify the user is logged in with their corporate SSO email and not a personal account.

## Fix steps
1. Instruct the user to log out of the Zoom desktop client.
2. Click Sign In and select the Sign In with SSO option.
3. Enter the corporate domain (e.g., companyname) and complete the browser-based login.
4. Once logged back in, check the profile again. It should now say "Licensed."
5. If the user is on the correct account but still "Basic," an administrator must log into the Zoom Admin Portal.
6. Navigate to Users > Active Users, find the user, and change their User Type from Basic to Licensed.
7. The change is instant; the user does not need to restart their current meeting for the limit to be lifted on the next one.

## Escalate if
- The user is assigned a license in the portal but the client still shows them as "Basic" after multiple logouts.
- The company has run out of available Zoom licenses.

## Ticket fields to capture (when escalating)
- Current User Type: (Basic or Licensed)
- SSO Domain Used: (e.g., company.zoom.us)
- Meeting ID: (The affected 11-digit ID)