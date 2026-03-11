---
doc_id: KB-Z2A3B4C5-mailbox_quota
title: "Performance — Outlook — Mailbox Quota Full"
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
- mailbox
- quota
- full
- storage
- archive
- cleanup
- exchange
urls: []
---

# Mailbox Quota Full

# Outlook (Storage Management)

Use this guide to assist users whose Microsoft 365 mailbox has reached its maximum storage capacity (typically 50GB or 100GB), preventing them from sending or receiving new messages.

### Mailbox Quota Full

## Severity:
`S2` — High impact; the user is completely blocked from sending or receiving emails, which halts all business communications.

## Symptoms
- A yellow banner appears at the top of Outlook stating "Mailbox Full: Your mailbox is full and you can't send or receive messages."
- The user receives a Non-Delivery Report (NDR) from the system when trying to send mail, stating "Smtp; 554 5.2.2 mailbox full."
- External senders receive a bounce-back message stating the recipient's inbox is full.

## Quick checks
- Click File in the top left of Outlook. Under the Info tab, look for the Mailbox Settings section to see a visual bar indicating how much of the 50GB/100GB limit is currently in use.
- Check the Deleted Items and Junk Email folders, as items in these folders still count toward the total mailbox quota.


## Fix steps
1. Instruct the user to right-click the Deleted Items folder and select Empty Folder.
2. Click File > Info > Mailbox Settings > Cleanup Tools > Mailbox Cleanup.
3. Use the Find items larger than option (e.g., find items larger than 5000 KB) to identify and delete old emails with massive attachments that are no longer needed.
4. If the user must keep their emails for legal or business reasons, instruct them to move older folders into their Online Archive (if enabled). 
5. In the left navigation pane, look for a folder set named "Online Archive - [User Email]". 
6. Drag and drop older year-specific folders from the primary Inbox into the Online Archive. This moves the data to a separate cloud storage area with its own quota, freeing up the primary mailbox immediately.
7. Once enough space is cleared (usually below 90% capacity), the "Mailbox Full" banner will disappear, and pending incoming emails will begin to flow in.

## Escalate if
- The user has emptied their folders and moved items to the archive, but the storage bar still shows as 100% full.
- The Online Archive is missing or throws an error when the user tries to move files into it.
- The user is an executive or high-volume user who legitimately requires a mailbox increase to a higher license tier (e.g., moving from a 50GB E3 license to a 100GB E5 license).

## Ticket fields to capture (when escalating)
- Current Mailbox Size: (e.g., 49.9 GB of 50 GB)
- Archive Enabled: (Yes/No)
- License Type: (e.g., Microsoft 365 Business Standard vs. Enterprise E5)