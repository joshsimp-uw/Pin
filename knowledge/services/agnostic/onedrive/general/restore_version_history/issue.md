---
doc_id: KB-B3C4D5E6-version_history
title: "General — OneDrive — Restore Version History"
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
- version
- history
- overwrite
- rollback
- mistake
- autosave
urls: []
---

# Restore Version History

# OneDrive (Data Recovery)

Use this guide to resolve issues where a user accidentally modified a document, deleted crucial text, or broke an Excel formula, and AutoSave immediately overwrote the cloud file with the broken version.

### Restore Version History

## Severity:
`S3` — Minor degradation; the file still exists, but the user cannot continue working until the data is rolled back to a previous, clean state.

## Symptoms
- The user left their keyboard, a cat walked across it, and AutoSave saved the gibberish to the cloud.
- Two users were co-authoring a document, and one user accidentally deleted an entire section of the report.
- The file opens successfully, but the data is completely wrong or corrupted.

## Quick checks
- Verify that the file actually resides inside the OneDrive directory. Version history does not exist for files saved purely to a local drive.
- Remind the user that restoring an old version will overwrite any legitimate changes made since that specific timestamp.

## Fix steps
1. (From File Explorer): Open Windows File Explorer and navigate to the broken file.
2. Right-click the file and select Version history (you may need to click "Show more options" first on Windows 11).
3. A small window will appear listing all previous saves by date, time, and the name of the user who modified it.
4. Hover over the desired previous date, click the three dots (More options), and select Restore. This replaces the current file with the old one.
5. (From within Word/Excel): Open the broken document in the desktop application.
6. Click the title of the document at the very top center of the window to open the drop-down menu.
7. Click Version History. A panel will open on the right side.
8. Click Open version under the target timestamp to open it in a read-only window. If it looks correct, click the Restore button at the top of that window.

## Escalate if
- The Version History panel is completely empty or throws a "Cannot retrieve versions" error.
- The file is encrypted by ransomware, meaning the user needs an administrator to trigger a mass "Files Restore" for the entire OneDrive account, rather than fixing a single file.

## Ticket fields to capture (when escalating)
- Target File Name: (e.g., Project_Timeline.docx)
- Desired Rollback Date: (e.g., March 9th at 4:00 PM)
- Co-authoring Status: (Were multiple people editing this file?)
