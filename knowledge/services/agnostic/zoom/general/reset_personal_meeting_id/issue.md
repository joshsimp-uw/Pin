---
doc_id: KB-Z7P8M9I0-reset_pmi
title: "General — Zoom — Reset Personal Meeting ID"
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
- pmi
- personal-meeting-id
- reset
- link
- security
- privacy
urls: []
---

# Reset Personal Meeting ID

# Zoom (User Privacy)

Use this guide to help users who need to change their 10-digit Personal Meeting ID (PMI) because the link has been leaked to unauthorized individuals or they are receiving uninvited guests in their private meeting room.

### Reset Personal Meeting ID

## Severity:
`S3` — Minor degradation; the user must update all recurring calendar invites that used the old ID, but their account remains secure.

## Symptoms
- Uninvited participants are joining the user's personal meeting room.
- The user wants to change their "Personal Link" alias (e.g., zoom.us/my/username) to something different.
- The user's current PMI is too easy to guess (e.g., 111-222-3333).

## Quick checks
- Confirm the user understands that once the PMI is changed, any existing calendar invites using the old 10-digit ID will no longer work.

## Fix steps
1. Instruct the user to log into the Zoom web portal at company.zoom.us.
2. Click Profile in the left-hand navigation menu.
3. Locate the Personal Meeting ID section.
4. Click Edit on the right side of the 10-digit ID.
5. Enter a new 10-digit number. Note: Some organizations restrict this; if they cannot type a new one, click the link to Change to a different ID.
6. If the user wants to change their Personal Link (the name version), click Edit next to the URL below the ID.
7. Enter the new alias and click Save Changes.
8. Advise the user to enable a Waiting Room or a Passcode on their PMI settings moving forward to prevent future "Zoom-bombing" incidents.

## Escalate if
- The Edit button is missing or the user receives an error stating "You do not have permission to change your PMI."
- The user changes the ID but uninvited guests are still able to join (suggesting the user is still using the old link in their Outlook signature).

## Ticket fields to capture (when escalating)
- Account Type: (Licensed is usually required to customize PMI)
- New PMI Requested: (Do not record the specific ID in the ticket for security)
- Reason for Reset: (e.g., Security breach or Ease of use)