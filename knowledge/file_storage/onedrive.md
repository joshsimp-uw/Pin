---
doc_id: KB-72E6780D9F
title: File Storage — OneDrive (Personal Files)
service: OneDrive for Business
audience:
  - End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
  - onedrive
  - files
  - sync
  - m365
urls:
  - https://portal.office.com
---

# OneDrive (Personal Files)

Use OneDrive for your personal work files. Access via https://portal.office.com → OneDrive.

## Common issues

### OneDrive not syncing

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Sync icon shows errors
- Files don't appear on other devices
- Status stuck on 'Processing changes'

**Quick checks**
- Confirm internet connection
- Confirm you are signed in to OneDrive

**Fix steps**
1. Click the OneDrive cloud icon and review any error message.
2. Pause syncing for 1 minute, then resume.
3. Restart OneDrive from the icon menu.
4. Restart your computer if the issue persists.

**Escalate if**
- Errors persist after restart
- Work files missing across devices

**Ticket fields to capture (when escalating)**
- **Error message:** As shown in OneDrive
- **File path:** Folder/file affected

### Can't find a file

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- File missing from folder
- You think you deleted it

**Quick checks**
- Use search in OneDrive
- Check Recycle Bin

**Fix steps**
1. Search OneDrive for the filename.
2. Check OneDrive Recycle Bin and restore if found.
3. Check 'Version history' if you need an older copy.

**Escalate if**
- File not in Recycle Bin and business-critical
- Large set of files missing

**Ticket fields to capture (when escalating)**
- **File name:** Exact name if possible
- **Approx date last seen:** Date/time

### Sharing link not working

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- Recipient can't open link
- Permission denied

**Quick checks**
- Confirm the recipient email is correct
- Try generating a new link

**Fix steps**
1. Create a new share link and ensure it is set to the correct permission (View/Edit).
2. If sharing to an external recipient is required, follow company policy and request IT approval if needed.

**Escalate if**
- Sharing is business-critical and blocked
- You need external sharing and it fails consistently

**Ticket fields to capture (when escalating)**
- **Recipient:** Internal or external
- **Permission needed:** View/Edit


## Escalation logic (for chatbot / help desk)
- Sync broken with work impact → **S2**
- Single file restore / how-to → **S3**
- Suspected data loss across many files → **S1**
