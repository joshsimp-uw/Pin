---
doc_id: KB-D1E2S3K4-open_desktop
title: "Connectivity — SharePoint — File Open in Desktop App"
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
- desktop-app
- word
- excel
- browser
- edit
- office-online
urls: []
---

# File Open in Desktop App

# SharePoint (Office Integration)

Use this guide to assist users who want their SharePoint documents to open directly in the full desktop version of Word, Excel, or PowerPoint instead of the web browser version.

### File Open in Desktop App

## Severity:
`S4` — Proactive request; the user can still work in the web version, but requires the advanced features and local interface of the desktop applications.

## Symptoms
- The user clicks a file name in a SharePoint library and it immediately opens a new browser tab with the Office Online editor.
- The user complains that the web version of Excel lacks the advanced formatting or macros they need.

## Quick checks
- Verify the user has a valid Microsoft 365 license and the Office desktop applications are installed on their computer.
- Ensure the user is signed into the desktop Office app with the same corporate account they use for SharePoint.

## Fix steps
1. (Individual File): Click the three dots (...) next to the file name in SharePoint.
2. Select Open > Open in app. The browser will prompt "Always allow portal.office.com to open links of this type." Check the box and click Open.
3. (Site-wide Preference): Click the Gear icon in the top right of the SharePoint site and select Site contents.
4. Click Site settings. Under the Site Collection Administration section, look for Site collection features. (Note: This may require Site Owner permissions).
5. Find the feature Open Documents in Client Applications by Default and click Activate.
6. (Personal Preference): In the SharePoint library, click the Gear icon > Library settings > More library settings.
7. Click Advanced settings.
8. Under Opening Documents in the Browser, select Open in the client application. Click OK.

## Escalate if
- The Open in app option is clicked, but the desktop application never launches or throws a "Protocol not supported" error.
- The file opens in the desktop app but is in "Read-Only" mode even though the user has edit permissions.
- The user is using a non-Windows OS (like Linux) that does not support the Office desktop suite.

## Ticket fields to capture (when escalating)
- Office Version: (e.g., M365 Apps for Enterprise)
- Browser: (e.g., Chrome, Edge)
- Error Message: (Exact text of any popup)