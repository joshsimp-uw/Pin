---
doc_id: KB-3F80700843-file_locke
title: "File Storage \u2014 SharePoint (Team/Department Files) \u2014 File locked\
  \ / can't edit"
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
- file_locked_can_t_edit
urls:
- https://acme.sharepoint.com
---

# File locked / can't edit

# SharePoint (Team/Department Files)

SharePoint stores team and department documents. ACME tenant: https://acme.sharepoint.com

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
