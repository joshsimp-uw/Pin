---
doc_id: KB-3F80700843-sync_issue
title: "File Storage \u2014 SharePoint (Team/Department Files) \u2014 Sync issues\
  \ with SharePoint folder"
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
- sync_issues_with_sharepoint_folder
urls:
- https://acme.sharepoint.com
---

# Sync issues with SharePoint folder

# SharePoint (Team/Department Files)

SharePoint stores team and department documents. ACME tenant: https://acme.sharepoint.com

### Sync issues with SharePoint folder

## Severity:
`S2` — Major degradation; user work significantly impacted. Escalate within same business day.

## Symptoms
- Folder not updating
- Errors in sync client

## Quick checks
- Confirm OneDrive sync client is running
- Try re-syncing the library

## Fix steps
1. Restart OneDrive sync client.
2. Stop syncing the library and set it up again.
3. If errors persist, capture the error message and contact IT.

## Escalate if
- Multiple libraries fail to sync
- Work files missing

## Ticket fields to capture (when escalating)
- Library name: Which team/site
- Error message: As shown


## Escalation logic (for chatbot / help desk)
- Permission/access blocks work → **S2**
- Single file lock/how-to → **S3**
- Broad access loss across users or suspected data loss → **S1**
