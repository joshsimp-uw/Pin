---
doc_id: KB-3F80700843
title: File Storage — SharePoint (Team/Department Files)
service: SharePoint Online
audience:
  - End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
  - sharepoint
  - m365
  - permissions
  - files
urls:
  - https://acme.sharepoint.com
---

# SharePoint (Team/Department Files)

SharePoint stores team and department documents. ACME tenant: https://acme.sharepoint.com

## Common issues

### Access denied to a SharePoint site or folder

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- You see 'Access denied' or cannot open a library
- You used to have access and lost it

**Quick checks**
- Confirm you are signed in with your @acme.com account
- Try opening in an InPrivate/Incognito window

**Fix steps**
1. Sign out and sign back in with your ACME account.
2. Try again in an InPrivate/Incognito window.
3. If you still cannot access, request access from the site owner (or submit a ticket if you don't know the owner).

**Escalate if**
- You cannot work due to missing access
- Multiple users report loss of access

**Ticket fields to capture (when escalating)**
- **Site URL:** Copy/paste
- **Used to have access:** Yes/No

### File locked / can't edit

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- Document opens read-only
- Says 'locked for editing'

**Quick checks**
- Wait 2–3 minutes and retry
- Check if another user is editing

**Fix steps**
1. Close the document and wait a few minutes.
2. Reopen and try again.
3. If needed, use 'Version history' to restore a prior version.

**Escalate if**
- File stays locked for hours
- Critical shared document blocks a team deadline

**Ticket fields to capture (when escalating)**
- **Document name:** File name
- **How long locked:** Minutes/hours

### Sync issues with SharePoint folder

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Folder not updating
- Errors in sync client

**Quick checks**
- Confirm OneDrive sync client is running
- Try re-syncing the library

**Fix steps**
1. Restart OneDrive sync client.
2. Stop syncing the library and set it up again.
3. If errors persist, capture the error message and contact IT.

**Escalate if**
- Multiple libraries fail to sync
- Work files missing

**Ticket fields to capture (when escalating)**
- **Library name:** Which team/site
- **Error message:** As shown


## Escalation logic (for chatbot / help desk)
- Permission/access blocks work → **S2**
- Single file lock/how-to → **S3**
- Broad access loss across users or suspected data loss → **S1**
