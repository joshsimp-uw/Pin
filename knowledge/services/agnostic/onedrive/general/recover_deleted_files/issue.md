---
doc_id: KB-X9Y0Z1A2-recover_deleted
title: "General — OneDrive — Recover Deleted Files"
service: Cloud Storage
audience:
- End Users
- Helpdesk
owner: Cloud Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- onedrive
- deleted
- missing
- recover
- recycle-bin
- restore
- lost
urls: []
---

# Recover Deleted Files

# OneDrive (Data Recovery)

Use this guide to assist users who accidentally deleted important files or folders from their local OneDrive directory and need to retrieve them from the cloud before the organizational retention policy expires.

### Recover Deleted Files

## Severity:
`S2` — High impact; the user has lost critical data and risks permanent data loss if the file is not recovered within the 93-day recycle bin window.

## Symptoms
- A user accidentally pressed delete on a massive folder instead of a single file.
- A colleague deleted a shared file, and now it has disappeared from everyone else's synchronized computers.
- The user checked their local Windows Recycle Bin, but the file is missing or was permanently emptied.

## Quick checks
- Verify exactly when the user thinks the file was deleted. Files in the Microsoft 365 Recycle Bin are automatically and permanently purged after 93 days.
- Ensure the user is actually looking for a file that was stored in OneDrive, rather than a local un-synced folder like "Downloads".

## Fix steps
1. Instruct the user to open a web browser and navigate to portal.office.com or onedrive.com and sign in with their corporate credentials.
2. Open the OneDrive web application.
3. In the left-hand navigation pane, click on Recycle bin.
4. Locate the missing file or folder in the list. You can click the column headers to sort by "Date deleted" to easily find recent mistakes.
5. Click the circular checkmark next to the file name to select it.
6. Click the Restore button at the top of the page. The file will immediately reappear in its original location on the web and sync back down to the user's computer.
7. If the file is not in the primary Recycle bin, scroll to the very bottom of the page and click the link for the Second-stage recycle bin to check there.

## Escalate if
- The file is missing from both the first and second-stage recycle bins, requiring a SharePoint Administrator to attempt a PowerShell site recovery.
- The user is trying to restore a folder containing tens of thousands of files, which causes the web browser to crash or time out.
- The user claims they never deleted the file, but it randomly disappeared (indicating a potential malware infection or a severe sync conflict).

## Ticket fields to capture (when escalating)
- Target File Name: (e.g., Q1_Financial_Report.xlsx)
- Approximate Deletion Date: (When did it go missing?)
- Original File Path: (Where was the file located before deletion?)
