---
doc_id: KB-A1B2C3D4E5-default_apps
title: "Configuration — Endpoints — Incorrect Default Application"
service: Endpoint Configuration
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- configuration
- apps
- pdf
- browser
- windows
urls: []
---

# Incorrect Default Application

# Endpoints (Software Configuration)

Use this guide to resolve issues where files (PDFs, Images) or web links open in the incorrect application (e.g., PDFs opening in Edge instead of Adobe Acrobat).

### Default App Reset

## Severity:
`S3` — Minor degradation; user can still open files manually, but workflow is disrupted.

## Symptoms
- Double-clicking a file opens it in a browser or "generic" Windows app.
- Outlook links open in an unexpected web browser.
- File icons appear as generic white blocks or browser logos.

## Quick checks
- Verify if the preferred application (e.g., Adobe Acrobat, Chrome) is actually installed on the device.
- Check if a recent Windows Update or new software install reset the associations.

## Fix steps
1. Click the Start menu and type "Default Apps," then press Enter.
2. To fix by file type: Scroll down and select Choose defaults by file type.
3. Locate the extension (e.g., .pdf or .html) and click the current app icon.
4. Select the desired application from the list and click Set default.
5. Alternatively, right-click the file in File Explorer, select Open with > Choose another app, select the app, and check Always use this app to open files.

## Escalate if
- Default associations revert to system defaults immediately after a reboot.
- The desired application does not appear in the "Open with" list despite being installed.
- The "Default Apps" settings page crashes or hangs when opened.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- File Extension: (e.g., .pdf, .csv)
- Intended App: (e.g., Adobe Acrobat Pro)
- Error Message: (Any error shown when trying to change the association)
