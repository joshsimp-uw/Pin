---
doc_id: KB-I1P2R3V4-insufficient_privileges
title: "Permissions — Salesforce — Insufficient Privileges Error"
service: CRM Operations
audience:
- End Users
- Helpdesk
owner: Sales Operations
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- salesforce
- permissions
- access
- denied
- privileges
- record-owner
- sharing-rules
urls: []
---

# Insufficient Privileges Error

# Salesforce (Data Security)

Use this guide to troubleshoot the generic "Insufficient Privileges" error, which occurs when a user has a link to a record but their Profile or Role does not grant them the necessary rights to view or edit it.

### Insufficient Privileges Error

## Severity:
`S3` — Minor degradation; the user is blocked from a specific record or action, which halts their immediate workflow for that specific customer or deal.

## Symptoms
- The user clicks a link to an Account or Opportunity and sees a white page with the message "Insufficient Privileges: You do not have the level of access necessary to perform the operation you requested."
- The user can see a record but the "Edit" button is missing.
- The user tries to save changes to a record but receives the error upon clicking save.

## Quick checks
- Check the Record Owner field at the top of the page. If the user is not the owner, they likely rely on Sharing Rules or the Role Hierarchy to see it.
- Ask the user if they were able to access this specific record yesterday. If yes, the record owner or an automated process may have changed the sharing settings.

## Fix steps
1. Instruct the user to send the URL of the record to their direct manager.
2. The manager should check if they can see the record. If the manager can see it, they can click the Sharing button on the record (in Lightning) to see why the subordinate is blocked.
3. If the user needs permanent access, a System Admin must check the Organization-Wide Defaults (OWD). If the object is set to "Private," the user needs a Sharing Rule or to be placed higher in the Role Hierarchy.
4. To grant one-time access, the Record Owner can click the Sharing button and manually add the user with "Read/Write" access.
5. If the error occurs when clicking a button (like "Convert Lead"), verify the user has the specific "Convert Leads" checkbox enabled on their Profile.

## Escalate if
- The user is the Record Owner but still receives an "Insufficient Privileges" error (suggesting a corrupted Profile or a conflicting Permission Set).
- The error occurs when the user is trying to access a standard report or dashboard.
- The user has "Modify All Data" permissions but is still being blocked.

## Ticket fields to capture (when escalating)
- Record ID: (The 15 or 18 character ID from the URL)
- Profile Name: (The user's Salesforce profile)
- Action Attempted: (e.g., Viewing, Editing, Deleting)