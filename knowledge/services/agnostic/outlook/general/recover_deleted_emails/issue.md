---
doc_id: KB-H6I7J8K9-recover_emails
title: "General — Outlook — Recover Deleted Emails"
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
- deleted
- recover
- missing
- recycle-bin
- purge
- exchange
urls: []
---

# Recover Deleted Emails

# Outlook (Data Recovery)

Use this guide to assist users who accidentally deleted an email and then emptied their "Deleted Items" folder, or users whose emails were purged by an automated retention policy.

### Recover Deleted Emails

## Severity:
`S2` — High impact; the user has lost data that is no longer in their primary folders, requiring a server-side recovery from the Exchange dumpster.

## Symptoms
- The user accidentally deleted a folder or a specific thread and cannot find it in the Deleted Items folder.
- The user "hard deleted" an email by pressing Shift + Delete.
- The user's Deleted Items folder was emptied, and they realized they needed a document from one of those emails.

## Quick checks
- Ensure the user is not just looking in the wrong subfolder or has a search filter applied that is hiding the mail.
- Confirm the deletion happened within the last 14 to 30 days (the standard retention period for the Exchange "Recoverable Items" folder).

## Fix steps
1. Open Outlook and click on the Deleted Items folder in the left-hand navigation pane.
2. Look at the Home tab on the ribbon. In the Actions group, click the button that says Recover Deleted Items from Server.
3. A new window will open showing all items that were purged from the Deleted Items folder but are still stored on the Exchange server.
4. Use the search bar or sort by the "Deleted On" column to find the missing emails.
5. Select the desired emails and ensure the Restore Selected Items radio button is selected at the bottom.
6. Click OK. The emails will be moved back into the Deleted Items folder.
7. The user can then drag the recovered emails back into their Inbox or a specific subfolder.


## Escalate if
- The Recover Deleted Items window is empty, even though the deletion was recent.
- The user is trying to recover an email deleted more than 30 days ago (requires an administrator to perform a Content Search in the Microsoft 365 Compliance Center).
- The user is trying to recover mail from a Shared Mailbox and does not see the "Recover Deleted Items" button.

## Ticket fields to capture (when escalating)
- Approximate Deletion Date: (When did it go missing?)
- Estimated Number of Emails: (Single email vs. entire folder)
- Search Keywords: (Subject line or sender name of the missing mail)