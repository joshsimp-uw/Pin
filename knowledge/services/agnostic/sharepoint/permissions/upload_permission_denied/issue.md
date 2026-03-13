---
doc_id: KB-U1P2D3N4-upload_denied
title: "Permissions — SharePoint — Upload Permission Denied"
service: Content Management
audience:
- End Users
- Helpdesk
owner: Cloud Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- sharepoint
- upload
- permissions
- read-only
- visitor
- member
urls: []
---

# Upload Permission Denied

# SharePoint (Contribution Rights)

Use this guide to assist users who can view and download files from SharePoint but receive an error or find the "Upload" and "New" buttons missing when trying to add content.

### Upload Permission Denied

## Severity:
`S3` — Minor degradation; the user is relegated to a passive "read-only" role, preventing them from contributing to the project.

## Symptoms
- The "Upload" and "New" buttons are completely missing from the top toolbar.
- Dragging a file into the library results in a red banner saying "You do not have permission to upload to this folder."
- The user can edit existing files (in some cases) but cannot create new ones.

## Quick checks
- Verify if the user is in the "Visitors" group (Read-only) instead of the "Members" group (Edit/Contribute).
- Check if the library has reached its storage quota, which can sometimes disable the upload button for all non-admin users.

## Fix steps
1. (Site Owner Action): Click the Gear icon > Site permissions.
2. Click Advanced permissions settings.
3. Click on the Site Members group (e.g., "Marketing Members").
4. Check if the user's name is in this list. If not, add them.
5. If the user is in the "Visitors" group, remove them and add them to the "Members" group instead.
6. Check the permission level for the "Members" group. It should be set to "Edit" or "Contribute". If it is set to "Read", change it.
7. Instruct the user to refresh their page. The "Upload" and "New" buttons should appear immediately.

## Escalate if
- The user is a "Member" and the group has "Edit" rights, but the upload button remains missing.
- The user is trying to upload to a folder that has been "Locked" by a compliance policy or a workflow.
- The issue is only happening for a specific file type (e.g., .exe or .vbs) that is blocked by a global tenant security policy.

## Ticket fields to capture (when escalating)
- Site URL: (The full web link)
- Current Permission Level: (e.g., Visitor, Member, Owner)
- Missing Buttons: (Is it just Upload, or New as well?)