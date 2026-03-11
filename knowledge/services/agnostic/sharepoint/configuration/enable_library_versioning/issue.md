---
doc_id: KB-S1H2A3R4-enable_versioning
title: "Configuration — SharePoint — Enable Library Versioning"
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
- versioning
- history
- library
- settings
- content
urls: []
---

# Enable Library Versioning

# SharePoint (Document Library Settings)

Use this guide to assist Site Owners in enabling or configuring version history for a specific document library, ensuring that every save creates a restorable backup.

### Enable Library Versioning

## Severity:
`S4` — Proactive request; the user wants to implement a safety net for their team's collaborative documents.

## Symptoms
- The user clicks on a file and selects "Version history", but only the current version is visible.
- The user wants to limit the number of versions kept to save on storage quota but cannot find the setting.

## Quick checks
- Verify the user has "Full Control" or "Design" permissions for the site. Standard "Members" cannot change library-level settings.
- Ensure the library is not currently being synced via the legacy OneDrive sync client, which can occasionally conflict with versioning changes.

## Fix steps
1. Navigate to the SharePoint document library in a web browser.
2. Click the Gear icon in the top right corner and select Library settings.
3. Click More library settings to open the full administration page.
4. Under the General Settings column, click Versioning settings.
5. Under Document Version History, select Create major versions or Create major and minor (draft) versions depending on the team's needs.
6. Optional: Check the box for "Keep the following number of major versions" and enter a value (e.g., 500) to prevent excessive storage usage.
7. Scroll to the bottom and click OK. 
8. Any file modified from this point forward will now generate a version history entry.

## Escalate if
- The "Library settings" option is completely missing from the gear menu for a user who claims to be the site owner.
- Versioning is enabled, but the system fails to create new versions when files are saved (suggesting a server-side event receiver failure).
- The user needs to enable versioning across hundreds of sites simultaneously (requires a SharePoint Admin to run a PowerShell script).

## Ticket fields to capture (when escalating)
- Site URL: (The full web link to the SharePoint site)
- Library Name: (e.g., Project Documents)
- Permission Level: (Does the user have Full Control?)