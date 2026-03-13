---
doc_id: KB-E1X2S3R4-external_sharing
title: "Permissions — SharePoint — External Sharing Restricted"
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
- external
- sharing
- guest
- policy
- blocked
- security
urls: []
---

# External Sharing Restricted

# SharePoint (Security Policies)

Use this guide to troubleshoot issues where a site owner is trying to share a folder or document with an external partner, but the option to share outside the organization is missing or greyed out.

### External Sharing Restricted

## Severity:
`S3` — Minor degradation; users are unable to collaborate with third-party vendors, potentially delaying project timelines.

## Symptoms
- The Share dialog box only allows the user to enter internal company email addresses.
- The option "Anyone with the link" is greyed out with a message stating "Your organization's policy prevents you from selecting this option."
- The user enters an external email, and a red error appears saying "This person is not in your organization."

## Quick checks
- Verify if the site contains sensitive or highly confidential data. Some sites are intentionally locked down via sensitivity labels.
- Confirm the external user's email address is spelled correctly and is not from a domain specifically blacklisted by the company.


## Fix steps
1. (Site Owner Action): Navigate to the site home page.
2. Click the Gear icon > Site permissions.
3. Click Advanced permissions settings.
4. Check the site collection settings to see if "External sharing" is enabled for this specific site.
5. If the site is a "Communication" site, external sharing may be disabled by default.
6. (Admin Action): Log into the SharePoint Admin Center.
7. Navigate to Sites > Active sites and select the target site.
8. Click the Settings tab and select Sharing.
9. Change the sharing level from "Only people in your organization" to "New and existing guests" or "Anyone". Click Save.
10. Wait 5 minutes and have the site owner attempt to share the file again.

## Escalate if
- The sharing level is already set to "Anyone" in the admin center, but the user is still blocked.
- The user is trying to share with a specific domain (e.g., @competitor.com) that is globally blocked at the tenant level.
- The user receives an error stating "This site is currently under a legal hold and cannot be shared."

## Ticket fields to capture (when escalating)
- Site URL: (The full web link)
- External Domain: (e.g., @partner-vendor.com)
- Admin Center Status: (What is the current sharing level set to?)