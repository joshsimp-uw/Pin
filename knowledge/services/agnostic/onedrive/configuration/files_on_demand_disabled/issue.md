---
doc_id: KB-E5F6G7H8-files_on_demand
title: "Configuration — OneDrive — Files On-Demand Disabled"
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
- files
- on-demand
- storage
- space
- full
- sync
- download
urls: []
---

# Files On-Demand Disabled

# OneDrive (Storage Configuration)

Use this guide to assist users whose local computer hard drive has completely filled up because their OneDrive sync engine is attempting to download their entire terabyte of cloud data locally.

### Files On-Demand Disabled

## Severity:
`S3` — Minor degradation; the computer's local hard drive is full, causing the OS to run sluggishly and preventing the user from saving new local files.

## Symptoms
- Windows repeatedly throws a "Low Disk Space" warning for the C: drive.
- Opening File Explorer shows solid green checkmark icons next to every single file and folder in the OneDrive directory, rather than the blue outline of a cloud.
- The user recently set up a new computer and let it sync overnight.

## Quick checks
- Open File Explorer and click on This PC to verify that the local C: drive capacity is actually red and full.
- Confirm the user actually has internet access, as Files On-Demand requires an active connection to fetch files.


## Fix steps
1. Right-click the root OneDrive folder (e.g., "OneDrive - Corporate Name") in the left pane of File Explorer.
2. Select Free up space from the context menu. This will immediately purge the local copies of the files while leaving the placeholder icons intact, returning massive amounts of hard drive space.
3. To prevent this from happening again, click the OneDrive cloud icon in the system tray.
4. Click the gear icon and select Settings.
5. Navigate to the Sync and back up tab on the left, then expand Advanced settings.
6. Look for the Files On-Demand section and click the button that says Free up disk space or ensure the toggle for "Save space and download files as you use them" is turned on.

## Escalate if
- Freeing up space runs successfully, but the hard drive remains completely full (indicating a different application or hidden system log is consuming the space).
- The "Free up space" option is completely missing from the right-click menu and the OneDrive settings.
- The user is frequently working offline and legitimately needs the entire drive downloaded locally, requiring a hardware upgrade for a larger solid-state drive.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Total Drive Capacity: (e.g., 256GB)
- Free Space Remaining: (e.g., 1.2GB)
- Missing Menu Option: (Was Files On-Demand missing? Yes/No)
