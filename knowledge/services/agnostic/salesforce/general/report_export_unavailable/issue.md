---
doc_id: KB-X1P2O3R4-export_unavailable
title: "General — Salesforce — Report Export Unavailable"
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
- report
- export
- excel
- csv
- permissions
- missing-button
urls: []
---

# Report Export Unavailable

# Salesforce (Reporting & Analytics)

Use this guide to resolve issues where a user is able to view a Salesforce report but is missing the "Export" button required to pull the data into Excel or CSV format.

### Report Export Unavailable

## Severity:
`S3` — Minor degradation; the user has access to the information within the CRM, but their ability to perform offline analysis or data migration is blocked.

## Symptoms
- The user clicks the drop-down arrow next to the "Edit" button on a report, but "Export" is not listed in the menu.
- The user can see the data on their screen but cannot find any way to save it to their local machine.
- Other members of the same team are able to export the exact same report.

## Quick checks
- Check if the report is in a "Joined Report" format. Salesforce Lightning sometimes restricts exporting joined reports directly from the main interface.
- Ask the user if they were ever able to export reports in the past, or if this is a new requirement for their role.


## Fix steps
1. Verify the user's Profile permissions. A System Admin must ensure the Export Reports permission is checked under the "Administrative Permissions" section of the user's Profile or an assigned Permission Set.
2. If the user has the permission but still cannot see the button, ensure they are not in "Edit" mode. The Export button only appears on the report "Run" page, not the "Builder" page.
3. Instruct the user to click the arrow next to the Edit button and look for Export.
4. If they are using a custom Report Type, ensure the "Allow Reports" checkbox is enabled on the underlying objects.
5. If the organization uses a "Shield" or "Event Monitoring" security package, check if a transaction security policy is blocking the export due to the number of rows or the sensitive nature of the data.

## Escalate if
- The user has the "Export Reports" permission, but the button remains missing after clearing browser cache and cookies.
- The user attempts to export but receives an error stating "Your organization's security settings prevent you from exporting this many records."
- The user needs to export a report with more than 256 columns (Salesforce limit).

## Ticket fields to capture (when escalating)
- Report Name: (The specific report name)
- Profile Name: (The user's Salesforce profile)
- Number of Rows: (Approximate size of the report)