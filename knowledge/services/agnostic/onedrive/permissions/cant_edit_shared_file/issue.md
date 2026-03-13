---
doc_id: KB-F7G8H9I0-cant_edit
title: "Permissions — OneDrive — Cannot Edit Shared File"
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
- shared
- edit
- read-only
- permissions
- access
urls: []
---

# Cannot Edit Shared File

# OneDrive (File Sharing)

Use this guide to troubleshoot issues where a user opens a document shared by a colleague but is unable to make any changes, type text, or modify formulas.

### Cannot Edit Shared File

## Severity:
`S3` — Minor degradation; the user can view the necessary information but collaborative workflows are halted.

## Symptoms
- The document opens in Word or Excel, but a yellow banner at the top says "Viewing - You only have permission to read this file."
- The user's typing cursor does not appear on the page.
- All formatting ribbon options at the top of the application are greyed out.

## Quick checks
- Verify that the user is actually signed into the Office application with their correct corporate credentials, and not a personal Microsoft account.
- Ask the user to confirm with the original sender whether they intended to grant editing rights.

## Fix steps
1. Instruct the user to contact the original owner of the document (the person who sent the link).
2. Walk the original owner through updating the link permissions. Have them locate the file in their OneDrive, right-click it, and select Manage Access.
3. In the access panel, locate the user's name or the specific sharing link being used.
4. Click the pencil icon or the dropdown menu next to the name and change the permission from Can view to Can edit.
5. Have the restricted user completely close out of the document and click the shared link again to refresh their access token.

## Escalate if
- The original owner confirms the user is set to "Can edit", but the document still opens in read-only mode for them.
- The file is stored in a strictly controlled SharePoint document library where the original sender does not actually have the authority to grant edit access.
- The user is trying to edit an unsupported file type (like a locked PDF or an old .doc format) that requires conversion first.

## Ticket fields to capture (when escalating)
- Target File URL: (The shareable link being used)
- Document Owner: (The user who created/owns the file)
- Affected User: (The user failing to edit)
