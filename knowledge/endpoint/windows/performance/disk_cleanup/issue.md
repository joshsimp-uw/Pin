---
doc_id: KB-I9J0K1L2M3-disk_cleanup
title: "Performance — Endpoints — Disk Cleanup & Low Storage"
service: Endpoint Performance
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- storage
- disk
- space
- full
- cleanup
- c-drive
urls: []
---

# Disk Cleanup & Low Storage

# Endpoints (Hardware Storage)

Use this guide to troubleshoot devices that are running out of local storage space, which often leads to severe performance degradation, application crashes, and the inability to save work.

### Disk Cleanup

## Severity:
`S3` — Minor degradation; user cannot download new files or install updates, but core OS functions still run. (Note: Elevate to `S2` if the C: drive has 0 bytes free and the system is freezing).

## Symptoms
- Windows displays a persistent "Low Disk Space" notification in the system tray.
- The local C: drive shows a red storage bar in File Explorer.
- Applications crash when attempting to export or save large files.

## Quick checks
- Open the Recycle Bin on the Desktop and verify if it is holding a massive amount of deleted files.
- Ask the user to check their Downloads folder for old installers or large media files they no longer need.

## Fix steps
1. Click the Start menu, type Storage settings, and press Enter.
2. Toggle Storage Sense to On so Windows automatically cleans up temporary files in the future.
3. Click on Temporary files in the storage breakdown list.
4. Check the boxes for Windows Update Cleanup, Temporary Internet Files, and Thumbnails. (Warning: Do not check the Downloads folder unless the user explicitly agrees).
5. Click the Remove files button at the top of the list.
6. Alternatively, open the Start menu, type cleanmgr, right-click Disk Cleanup, and select Run as administrator to clear old system files.

## Escalate if
- The drive fills back up to 100% immediately after clearing space (indicating a runaway log file or malware).
- The user has deleted all personal files but the system partition is still inexplicably full.
- The storage drive is failing to read/write, resulting in blue screens (BSOD) or file corruption.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Total Drive Capacity: (e.g., 256GB SSD)
- Current Free Space: (e.g., 1.2GB)
- Top Consuming Folder: (e.g., C:\Windows\Temp)