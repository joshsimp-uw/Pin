---
doc_id: KB-Y5Z6A7B8-stuck_updating
title: "Connectivity — Outlook — Stuck Updating Inbox"
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
- stuck
- updating
- inbox
- downloading
- sync
- ost
urls: []
---

# Stuck Updating Inbox

# Outlook (Sync Troubleshooting)

Use this guide to resolve issues where Outlook is technically connected to the server, but the synchronization process hangs indefinitely, preventing new emails from displaying in the folder.

### Stuck Updating Inbox

## Severity:
`S3` — Minor degradation; user can temporarily use webmail as a workaround, but their desktop client is outdated and sluggish.

## Symptoms
- The status bar at the bottom right of Outlook says "Updating Inbox" or "Downloading 1 of X bytes" and the progress bar never moves.
- The user receives a notification on their phone about a new email, but it does not appear in their desktop Outlook.
- Switching between folders takes a very long time, and Outlook occasionally flashes "Not Responding" at the top of the window.

## Quick checks
- Verify the user is not on an extremely slow public Wi-Fi network or a metered cellular hotspot.
- Check the Outbox to see if the user is trying to send a massive attachment (like a 50MB video file) that is clogging the entire sync queue.

## Fix steps
1. Right-click the Inbox folder in the left navigation pane and select Properties.
2. Go to the General tab and click the Clear Offline Items button. Click OK to confirm.
3. Switch to a different folder (like Sent Items), then switch back to the Inbox. Click the Send / Receive tab and click Update Folder to force a fresh download of the inbox contents.
4. If the sync remains stuck, close Outlook entirely.
5. Press the Windows Key + R to open the Run dialog.
6. Type `%localappdata%\Microsoft\Outlook` and press Enter.
7. Locate the file that ends in `.ost` (usually named after the user's email address). 
8. Right-click the `.ost` file and rename it to `.old` (e.g., user@company.com.old).
9. Reopen Outlook. It will automatically recreate a fresh `.ost` database and begin a clean, full sync from the cloud. (Note: This initial sync may take 15-30 minutes depending on the mailbox size).

## Escalate if
- Renaming the `.ost` file fails because Windows says the file is currently in use (requires forcing the Outlook.exe process closed in Task Manager).
- The full sync finishes, but the inbox immediately gets stuck on "Updating" again the next day.
- The user's mailbox is approaching the 100GB limit, which causes the `.ost` file to become unstable and prone to constant sync freezing.

## Ticket fields to capture (when escalating)
- Outlook Version: (e.g., Microsoft 365 Apps for Enterprise)
- Mailbox Size: (Approximate size in GB)
- OST Rebuild Attempted: (Yes/No)