---
doc_id: KB-T5U6V7W8-sync_stuck
title: "Connectivity — OneDrive — Sync Stuck Processing"
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
- sync
- stuck
- processing
- pending
- reset
- cache
urls: []
---

# Sync Stuck Processing

# OneDrive (Sync Engine Troubleshooting)

Use this guide to resolve issues where the OneDrive sync client hangs indefinitely, preventing new files from uploading or downloading from the cloud.

### Sync Stuck Processing

## Severity:
`S3` — Minor degradation; user cannot share recent files with colleagues, and collaborative documents may become out of sync or conflicted.

## Symptoms
- The OneDrive icon in the system tray constantly displays the circular syncing arrows but never finishes.
- Clicking the icon shows a status of "Processing changes" or "Sync pending" for hours or days.
- The file list inside the OneDrive menu shows 0 KB / 0 KB syncing, or gets stuck on a specific file name.

## Quick checks
- Verify the user is not trying to sync an open database file (like a .pst Outlook data file or an active Access database), which constantly locks the file and prevents sync.
- Check if the local hard drive is completely full, giving OneDrive no space to unpack incoming files.

## Fix steps
1. Click the blue OneDrive icon in the system tray.
2. Click the gear icon in the top right corner and select Pause syncing, then choose 2 hours.
3. Wait 10 seconds, click the gear icon again, and select Resume syncing. This soft reset often clears minor hangups.
4. If the sync is still stuck, press the Windows Key + R to open the Run dialog.
5. Type `%localappdata%\Microsoft\OneDrive\onedrive.exe /reset` and press Enter.
6. The OneDrive icon will disappear from the system tray as the background service is completely killed and its local cache is rebuilt.
7. Wait two minutes. If the icon does not reappear automatically, open the Windows Start menu, search for OneDrive, and launch it manually.
8. The app will say "Processing changes" again, but it should now correctly count down and finish.

## Escalate if
- The reset command throws a "Windows cannot find..." error (indicating a corrupted or missing OneDrive installation).
- The sync completes, but a specific handful of files remain permanently stuck with red 'X' icons due to unresolvable sync conflicts.
- The OneDrive app crashes completely (disappears from the tray) every time it attempts to process the changes.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Pro)
- Stuck File Name: (If the app is stuck on one specific file)
- Reset Attempted: (Did you run the /reset command? Yes/No)