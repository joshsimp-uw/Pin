---
doc_id: KB-S1B2M3N4-sync_missing
title: "Connectivity — SharePoint — Sync Button Missing"
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
- sync
- onedrive
- missing-button
- offline
- library-settings
urls: []
---

# Sync Button Missing

# SharePoint (Sync Configuration)

Use this guide to troubleshoot issues where a user wants to sync a library to their computer, but the "Sync" button is missing from the top toolbar of the SharePoint site.

### Sync Button Missing

## Severity:
`S3` — Minor degradation; the user is forced to use the web browser for file management, reducing their efficiency.

## Symptoms
- The toolbar shows "New," "Upload," and "Automate," but the "Sync" button is nowhere to be found.
- The button is visible for colleagues on the same site but missing for the specific user.
- The "Add shortcut to OneDrive" button is also missing.

## Quick checks
- Verify if the site is a legacy SharePoint Server site (On-Premise) or SharePoint Online, as legacy versions have different sync requirements.
- Check if the site is currently in "Classic" view. Some classic views hide modern toolbar buttons.


## Fix steps
1. (Site Configuration): If the user is a Site Owner, have them click the Gear icon > Library settings > More library settings.
2. Click Advanced settings.
3. Scroll down to the Offline Client Availability section.
4. Ensure the radio button for Allow items from this document library to be downloaded to offline clients? is set to Yes.
5. If it was set to No, change it to Yes and click OK. Refresh the browser; the Sync button should now appear.
6. (Browser Check): Ensure the user is not using an extremely outdated browser. Recommend Microsoft Edge for the best sync integration.
7. If the button is missing because of "Classic" view, click the Exit classic experience link in the bottom left corner of the page.

## Escalate if
- Offline Client Availability is set to "Yes" but the button remains missing.
- The global SharePoint Admin Center has disabled sync for the entire organization (requires an M365 Global Admin to check).
- The user has the button, but clicking it does absolutely nothing (indicating the OneDrive application is not installed or the URI protocol is blocked).

## Ticket fields to capture (when escalating)
- Site URL: (The full web link)
- Offline Client Setting: (Was it set to Yes or No?)
- OneDrive App Status: (Is OneDrive installed and running?)