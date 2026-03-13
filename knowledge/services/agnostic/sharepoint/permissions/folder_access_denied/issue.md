---
doc_id: KB-F1A2D3N4-folder_access
title: "Permissions — SharePoint — Folder Access Denied"
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
- access-denied
- permissions
- folder
- member
- inheritance
urls: []
---

# Folder Access Denied

# SharePoint (Direct Access)

Use this guide to resolve issues where a user is a member of a SharePoint site but receives an "Access Denied" error when trying to open a specific subfolder within a library.

### Folder Access Denied

## Severity:
`S3` — Minor degradation; the user is blocked from specific data, which may halt their ability to complete a specific task.

## Symptoms
- The user can see the parent library but clicks a folder and sees "Access Denied" or "You need permission to access this site."
- The folder is visible in the list, but clicking it results in a blank page or an infinite loading spinner.
- The user was recently added to the site's "Members" group but still cannot see certain folders.

## Quick checks
- Ask the user if other people on their team can see the folder.
- Verify if the folder has a "lock" icon on it, indicating unique permissions.


## Fix steps
1. (Site Owner Action): Navigate to the library and find the problematic folder.
2. Click the three dots (...) next to the folder and select Manage access.
3. Click Advanced in the bottom right of the panel.
4. Look for a yellow banner that says "This folder has unique permissions." This means it is not inheriting from the site.
5. Check the list of users and groups. If the user or their team group is not listed, click Grant Permissions and add them.
6. If the folder should be visible to everyone on the site, click Delete unique permissions to restore inheritance. (Warning: This will remove any custom access previously set for this folder).
7. Have the user clear their browser cache and try again.

## Escalate if
- The user is listed with "Full Control" on the folder but still receives an "Access Denied" error.
- The folder belongs to a private "Channel" in Microsoft Teams (these folders have complex backend permissions managed by Teams).
- The user is an external guest who has not yet accepted their initial invitation email.

## Ticket fields to capture (when escalating)
- Folder Path: (e.g., /Documents/Finance/2026_Budgets)
- User Email: (The person getting the error)
- Inheritance Status: (Unique or Inherited?)