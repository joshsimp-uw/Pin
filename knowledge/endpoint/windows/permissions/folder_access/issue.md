---
doc_id: KB-L2M3N4O5P6-folder_access
title: "Permissions — Endpoints — Folder Access Denied"
service: Endpoint Permissions
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- permissions
- access
- denied
- folder
- share
- ntfs
- security
urls: []
---

# Folder Access Denied

# Endpoints (File System Permissions)

Use this guide to troubleshoot issues where a user cannot open, modify, or save files within a specific local or shared network directory due to NTFS permission restrictions.

### Folder Access Denied

## Severity:
`S3` — Minor degradation; user is blocked from specific files or folders needed for their workflow.

## Symptoms
- Double-clicking a folder results in a pop-up stating "You don't currently have permission to access this folder."
- The user can open a file but cannot save changes (Read-Only access).
- A newly created file disappears or throws an error when attempting to move it into a shared department folder.

## Quick checks
- Confirm if the user recently changed roles or departments, which might have altered their Active Directory group memberships.
- Verify if other users in the same department are experiencing the same access issue.

## Fix steps
1. Right-click the problematic folder and select Properties.
2. Navigate to the Security tab.
3. Check the "Group or user names" list to see if the user's individual account or their department's security group is listed.
4. Highlight the relevant user or group and look at the "Permissions" box below to verify they have Read, Write, or Modify access checked.
5. If permissions are missing, and you have Admin rights, click Edit to add the user/group and assign the appropriate access level.
6. (Network Shares) If this is a network drive, use Active Directory Users and Computers (ADUC) to verify the user is a member of the correct security group for that share, then ask the user to log off and log back in to refresh their access token.

## Escalate if
- The Security tab is completely missing or greyed out.
- The permissions appear correct, but the user is still actively blocked from accessing the folder.
- The folder owner is listed as "Unknown" or a deleted SID (e.g., S-1-5-21-...), requiring a forced ownership takeover.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Folder Path: (The exact local or network path, e.g., `\\Server\Finance\Q3_Reports`)
- User Account: (The specific user requesting access)
- Required Access Level: (e.g., Read-Only vs. Modify/Write)