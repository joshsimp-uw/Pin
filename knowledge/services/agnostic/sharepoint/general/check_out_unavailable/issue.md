---
doc_id: KB-C1H2E3K4-check_out_missing
title: "General — SharePoint — Check Out Unavailable"
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
- check-out
- lock
- edit
- permissions
- library-settings
urls: []
---

# Check Out Unavailable

# SharePoint (Document Locking)

Use this guide to troubleshoot scenarios where a user wants to "Check Out" a file to prevent others from editing it, but the option is missing from the file menu or the library settings.

### Check Out Unavailable

## Severity:
`S3` — Minor degradation; users can still edit files but risk creating sync conflicts if multiple people edit the same document simultaneously.

## Symptoms
- The user right-clicks a file, but the "Check out" option does not appear in the context menu.
- The library is allowing multiple users to edit at once, but the project requirements mandate a strict one-user-at-a-time lock.
- A red arrow indicating a checked-out status is missing from all files in the library.

## Quick checks
- Verify if the document library is in "Classic" view, as the menu structure is different than the "Modern" experience.
- Check if the file is already checked out to another user (indicated by a small red arrow over the file icon).

## Fix steps
1. (Site Owner Action): Navigate to the document library in a web browser.
2. Click the Gear icon > Library settings > More library settings.
3. Under General Settings, click Advanced settings.
4. Scroll to the section titled Require Check Out.
5. If it is set to "No", change it to "Yes" to force users to check out files before editing. Click OK.
6. (User Action): If the setting is already "Yes" but the menu option is missing, instruct the user to refresh their browser.
7. If using the OneDrive sync client locally, right-click the file in File Explorer, select "Show more options", and look for the SharePoint > Check out menu item there.

## Escalate if
- The user has "Member" access but still cannot see the check-out option after the site owner enables it.
- A file is stuck in a checked-out state to a user who has left the company (requires a Site Owner or Admin to "Discard check out" or "Check in").
- The "Require Check Out" setting is greyed out in Library Settings.

## Ticket fields to capture (when escalating)
- Site URL: (The full web link)
- Library Name: (e.g., Legal Contracts)
- Current Setting: (Is Require Check Out enabled? Yes/No)