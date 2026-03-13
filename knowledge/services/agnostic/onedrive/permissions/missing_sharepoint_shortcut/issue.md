---
doc_id: KB-N5O6P7Q8-missing_shortcut
title: "Permissions — OneDrive — Missing SharePoint Shortcut"
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
- sharepoint
- shortcut
- sync
- local
- explorer
- files
urls: []
---

# Missing SharePoint Shortcut

# OneDrive (Cross-Platform Sync)

Use this guide to help users who were recently granted access to a shared department SharePoint site, but cannot find those files natively in their local Windows File Explorer.

### Missing SharePoint Shortcut

## Severity:
`S4` — Proactive request; the user can access the files via the web browser but wants the convenience of local desktop access.

## Symptoms
- The user received an email saying they were added to the "Marketing Team" SharePoint site.
- They open File Explorer, click on their OneDrive folder, but the Marketing files are nowhere to be found.
- The user does not want to use the web browser to upload and download files every time they work.

## Quick checks
- Ask the user to click the link in their email to verify they can actually load the SharePoint site in their web browser (confirming their permissions are correct).

## Fix steps
1. Instruct the user to open their web browser and navigate to the shared SharePoint document library they want to sync.
2. Look at the toolbar menu located just above the list of files.
3. Click the button that says Add shortcut to My files (it usually has a small OneDrive cloud icon next to it).
4. A notification will pop up in the top right corner saying "Added 1 shortcut to My files".
5. Instruct the user to open Windows File Explorer on their computer and navigate to their primary OneDrive folder.
6. Wait a few moments for the background sync engine to catch up. A new folder with a small "link" icon on it will appear, bearing the name of the SharePoint site. The user can now access those shared files locally.

## Escalate if
- The user clicks the shortcut button on the web, but the folder never appears in their local File Explorer even after restarting the OneDrive app.
- The user receives an error on the web stating "We couldn't add the shortcut" (this often happens if they are already using the legacy "Sync" button for that exact same library).
- The user lacks the permission to even view the SharePoint site on the web.

## Ticket fields to capture (when escalating)
- Target SharePoint URL: (The exact web link to the document library)
- Sync Method Attempted: (Add Shortcut vs. Legacy Sync Button)
- Error Message: (Any specific text shown on the web or desktop)
