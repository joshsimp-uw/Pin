---
doc_id: KB-A1L2E3R4-file_alerts
title: "Configuration — SharePoint — Set Up File Alerts"
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
- alerts
- notifications
- email
- monitoring
- library
urls: []
---

# Set Up File Alerts

# SharePoint (User Notifications)

Use this guide to help users configure automatic email notifications so they are alerted whenever a specific file or an entire document library is modified, deleted, or added to by a colleague.

### Set Up File Alerts

## Severity:
`S4` — Proactive request; the user wants to stay updated on project changes without manually checking the site.

## Symptoms
- The user complains they "never know when the boss updates the tracker."
- The user wants to receive a daily summary of all changes instead of individual emails for every click.

## Quick checks
- Confirm the user has at least "Read" access to the items they want to monitor.
- Verify the user's corporate email is correctly associated with their SharePoint profile.

## Fix steps
1. Navigate to the document library or specific folder in the web browser.
2. To alert on the whole library: Click the three dots (...) in the top toolbar and select Alert me.
3. To alert on a single file: Right-click the file, select the three dots (More), and select Alert me.
4. In the "New Alert" window, verify the Alert Title is descriptive.
5. Under Change Type, choose if you want alerts for All changes, New items only, or Deleted items only.
6. Under When to Send Alerts, choose between "Send notification immediately", "Send a daily summary", or "Send a weekly summary".
7. Click OK. The user will receive an initial confirmation email from SharePoint.

## Escalate if
- The user sets up the alert but never receives the confirmation email or any subsequent update notifications (suggesting the SharePoint outgoing mail service is blocked or the emails are going to Junk).
- The "Alert me" button is missing from the menu (indicating the site administrator has disabled the Alerting service for this specific site collection).
- The user wants to set up an alert for a different person (this requires "Manage Lists" permissions).

## Ticket fields to capture (when escalating)
- Site URL: (The full web link)
- Alert Frequency: (Immediate vs. Daily/Weekly)
- Notification Status: (Did the user get the confirmation email? Yes/No)