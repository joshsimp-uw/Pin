---
doc_id: KB-R1S2R3B4-site_recycle_bin
title: "General — SharePoint — Restore Site Recycle Bin"
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
- deleted
- restore
- recycle-bin
- missing
- recovery
urls: []
---

# Restore Site Recycle Bin

# SharePoint (Data Recovery)

Use this guide to assist users who have deleted files or folders from a shared SharePoint site and need to retrieve them from the site-level recycle bin.

### Restore Site Recycle Bin

## Severity:
`S2` — High impact; project data has been removed from the shared environment, potentially blocking an entire team.

## Symptoms
- A user accidentally deleted a folder and it has disappeared for all site members.
- The user checked their personal Windows Recycle Bin, but it is empty because the deletion happened on the cloud server.
- A "File Not Found" error occurs when clicking a previously working link to a document.

## Quick checks
- Verify the deletion occurred within the last 93 days. SharePoint items are permanently purged after this window.
- Confirm the user looking for the file has "Member" or "Owner" permissions for the site.


## Fix steps
1. Navigate to the SharePoint site home page in a web browser.
2. Look at the left-hand navigation menu (Quick Launch). Click on Recycle bin.
3. If the link is not visible in the menu, click the Gear icon > Site contents. The Recycle bin link is located in the top right of the Site Contents page.
4. Locate the deleted file or folder. You can sort by "Deleted" or "Deleted by" to find specific items.
5. Select the checkmark next to the item name.
6. Click Restore at the top of the list. The file will return to its original folder location.
7. If the file is not found, scroll to the bottom of the page and click Second-stage recycle bin to check for items deleted by a site owner or purged from the first bin.

## Escalate if
- The item is missing from both the first and second-stage recycle bins.
- The user is trying to restore a site collection that was deleted (requires a SharePoint Global Admin).
- The user receives an "Access Denied" error when trying to open the Recycle Bin.

## Ticket fields to capture (when escalating)
- Site URL: (The full web link)
- Deleted Item Name: (e.g., Project_Plan_2026.pptx)
- Date Deleted: (Approximate date)