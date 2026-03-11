---
doc_id: KB-S8T9U0V1-send_as_denied
title: "Permissions — Outlook — Send As Denied"
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
- send-as
- permissions
- shared-mailbox
- ndr
- exchange
- access
urls: []
---

# Send As Denied

# Outlook (Delegation & Shared Mailboxes)

Use this guide to resolve issues where a user attempts to send an email from a shared address (like info@company.com) but the message immediately bounces back with a permission error.

### Send As Denied

## Severity:
`S2` — High impact; the user cannot perform their departmental duties (e.g., customer support or billing) because they cannot send mail from the official group address.

## Symptoms
- The user receives a Non-Delivery Report (NDR) immediately after hitting send.
- The NDR contains the error: "This message could not be sent. You do not have the permission to send the message on behalf of the specified user."
- The error code is typically 0x80070005 or contains the phrase "Client has no permissions to send as this user."

## Quick checks
- Verify the user is selecting the correct address in the From field dropdown before sending.
- Check the "Sent Items" of the shared mailbox to see if other users are able to send successfully, ruling out a server-side transport issue.

## Fix steps
1. Open the Exchange Admin Center (EAC) or ask a junior admin to verify the mailbox settings.
2. Navigate to Recipients > Shared and select the target shared mailbox.
3. Under Delegation, verify the user is explicitly listed under Send As permissions. 
4. Note: Send on Behalf and Send As are different. Send As shows only the shared address, while Send on Behalf shows "User on behalf of Shared Address". Most departments require Send As.
5. If the user was recently added, inform them it can take up to 2 hours for the Exchange cloud to replicate this permission to the local Outlook client.
6. To force a refresh: Close Outlook and navigate to `%localappdata%\Microsoft\Outlook\Offline Address Books`. Delete the contents of the folder.
7. Reopen Outlook and click Send/Receive > Send/Receive Groups > Download Address Book.

## Escalate if
- The user is confirmed to have Send As permissions in the Admin Center, but the NDR persists after 24 hours.
- The user is trying to send from a Distribution List (DL) rather than a Shared Mailbox (DLs require different attribute tagging in the cloud).
- The user's account is a Guest or External user, which often cannot be granted Send As rights due to security defaults.

## Ticket fields to capture (when escalating)
- Shared Mailbox Address: (e.g., help@company.com)
- Permission Type: (Send As vs. Send on Behalf)
- Replication Time: (How long ago was the permission granted?)