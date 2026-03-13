---
doc_id: KB-A1B2C3D4-file_path_long
title: "Configuration — OneDrive — File Path Too Long"
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
- file
- path
- length
- characters
- sync
- error
urls: []
---

# File Path Too Long

# OneDrive (Sync Errors)

Use this guide to troubleshoot scenarios where a user's files fail to upload to the cloud because the folder structure they created exceeds the strict Windows and SharePoint character limits.

### File Path Too Long

## Severity:
`S3` — Minor degradation; specific files fail to back up to the cloud, risking data loss, but the rest of the drive functions normally.

## Symptoms
- A red 'X' icon appears on the OneDrive cloud icon in the Windows system tray.
- Clicking the OneDrive icon displays a sync error stating "The file name or path is too long".
- The user is creating folders inside of folders inside of folders (deep nesting).

## Quick checks
- Click the OneDrive icon in the system tray and review the specific list of files throwing the error to identify the problematic directory.
- Ask the user if they recently moved a large archive of legacy files from an old network drive into their OneDrive.


## Fix steps
1. Open File Explorer and navigate to the specific file or folder flagged in the OneDrive error log.
2. Shorten the name of the file itself.
3. If the file name is already short, work backward up the folder tree and rename the parent folders to be shorter (e.g., change "2026 Q1 Financial Reports Final Drafts" to "2026 Q1 Financials").
4. Alternatively, move the file or parent folder closer to the root of the OneDrive directory (e.g., move it straight to the top-level "Documents" folder instead of burying it five layers deep).
5. Once the path is shortened, the red 'X' on the file will automatically change to a blue syncing icon, and the error will clear.

## Escalate if
- The user shortens the path significantly, but the sync error refuses to clear after restarting the OneDrive application.
- The issue is happening within a massive, synchronized SharePoint document library where the user does not have permission to rename the parent folders.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Affected File Path: (Paste the exact path failing to sync)
- OneDrive Version: (Found in OneDrive Settings > About)
