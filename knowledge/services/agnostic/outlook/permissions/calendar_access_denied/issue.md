---
doc_id: KB-C4D5E6F7-calendar_access
title: "Permissions — Outlook — Calendar Access Denied"
service: Messaging & Collaboration
audience:
- End Users
- Helpdesk
owner: Cloud Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- outlook
- calendar
- permissions
- shared
- access
- denied
- exchange
urls: []
---

# Calendar Access Denied

# Outlook (Calendar Sharing)

Use this guide to troubleshoot issues where a user attempts to view a colleague's shared calendar but receives an "Access Denied" error or can only see "Busy" time without event details.

### Calendar Access Denied

## Severity:
`S3` — Minor degradation; the user cannot coordinate meetings efficiently, but basic email and personal calendar functions remain active.

## Symptoms
- The user clicks on a shared calendar in their list, and it displays "No Connection" or "Could not be updated."
- A popup appears stating "You do not have permission to view this calendar."
- The user can see that a colleague is busy, but cannot see the meeting titles or locations required for scheduling.

## Quick checks
- Verify the colleague has actually shared the calendar with the specific user, rather than just the "My Organization" default group.
- Ask if the user is trying to access the calendar from a mobile device, as some mobile sync protocols (like POP/IMAP) do not support shared calendar metadata.

## Fix steps
1. Instruct the owner of the calendar (the colleague) to open Outlook and go to the Calendar view.
2. Right-click their primary calendar and select Permissions or Share Calendar.
3. In the Permissions tab, verify the affected user is listed. If not, click Add and search for them in the Global Address List.
4. Ensure the Permission Level is set to at least Can view all details (to see titles) or Can edit (for delegates).
5. On the affected user's computer, right-click the shared calendar in their list and select Remove Calendar.
6. Click Add Calendar > From Address Book and re-add the colleague. This forces Outlook to fetch the updated permission manifest from the Exchange server.

## Escalate if
- The owner has granted Full Details permissions, but the user still only sees "Busy" or receives a permission error.
- The user is trying to access a calendar belonging to a user in a different, federated organization (requires a cross-tenant sharing policy check).
- The calendar is part of an Microsoft 365 Group or Shared Mailbox rather than an individual user's account.

## Ticket fields to capture (when escalating)
- Calendar Owner: (The person sharing the calendar)
- Affected User: (The person trying to view it)
- Permission Level Set: (e.g., Reviewer, Editor, or Availability Only)