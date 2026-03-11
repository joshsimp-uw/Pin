---
doc_id: KB-O1I2S3F4-outlook_sync_fail
title: "Connectivity — Salesforce — Outlook Integration Sync Failure"
service: CRM Operations
audience:
- End Users
- Helpdesk
owner: Sales Operations
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- salesforce
- outlook
- integration
- side-panel
- sync
- email
- calendar
urls: []
---

# Outlook Integration Sync Failure

# Salesforce (Desktop Integration)

Use this guide to resolve issues where the Salesforce side panel in Outlook fails to load, displays an error, or refuses to log emails and meetings to Salesforce records.

### Outlook Integration Sync Failure

## Severity:
`S3` — Minor degradation; the user can still use Salesforce and Outlook separately, but the automated data logging workflow is broken.

## Symptoms
- The Salesforce icon in the Outlook ribbon is greyed out or does not respond when clicked.
- The side panel opens but displays a message saying "Salesforce is taking too long to load" or "Session Expired."
- Emails marked for "Log on Send" are not appearing in the Activity History of the corresponding Salesforce contact.

## Quick checks
- Verify the user is running a supported version of Outlook (Microsoft 365 or Outlook 2019/2021).
- Confirm the user has not recently had their Salesforce or Microsoft 365 password changed.

## Fix steps
1. In the Outlook side panel, click the user's avatar or the gear icon and select Log Out.
2. Close Outlook entirely.
3. Open the computer's Control Panel > Internet Options.
4. Go to the General tab and click Delete under Browser history. Ensure Cookies and website data is checked and click Delete. (Outlook uses the underlying OS browser engine for the integration panel).
5. Open Outlook, click the Salesforce icon, and select Log in to Salesforce.
6. If the panel is completely missing, click Get Add-ins in the Outlook ribbon, search for Salesforce, and ensure it is turned On.
7. If the panel says "Browser not supported," ensure the user has the latest version of Microsoft Edge WebView2 Runtime installed on their PC.

## Escalate if
- The user successfully logs in, but the panel stays on a "Loading..." screen indefinitely.
- The integration works for some users but fails for everyone in a specific department (suggesting an Outlook Integration mapping issue in the Salesforce Setup).
- The user receives an error stating "Email tracking is disabled for your organization."

## Ticket fields to capture (when escalating)
- Outlook Version: (e.g., Office 365 Desktop Client)
- Integration Type: (Outlook Add-in vs. Einstein Activity Capture)
- OS Version: (e.g., Windows 11)