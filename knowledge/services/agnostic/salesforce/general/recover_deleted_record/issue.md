---
doc_id: KB-R1E2C3O4-recover_record
title: "General — Salesforce — Recover Deleted Record"
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
- delete
- recover
- recycle-bin
- restore
- account
- opportunity
urls: []
---

# Recover Deleted Record

# Salesforce (Data Recovery)

Use this guide to assist users who accidentally deleted a Salesforce record (such as an Account, Contact, or Opportunity) and need to restore it before it is permanently purged.

### Recover Deleted Record

## Severity:
`S2` — High impact; critical sales or customer data has been removed from the system, disrupting active pipelines and reporting.

## Symptoms
- A user tried to merge records and accidentally deleted the primary one.
- A search for a known Record ID or name returns "Record Deleted" or "Insufficient Privileges."
- An Opportunity has disappeared from a team dashboard.

## Quick checks
- Verify the record was deleted within the last 15 days. Salesforce only retains items in the Recycle Bin for 15 days before they are permanently unrecoverable.
- Ensure the user is the one who deleted the record, or is the owner, or is a System Admin (only these roles can typically see the item in their bin).

## Fix steps
1. Instruct the user to log into Salesforce.
2. If using Lightning Experience: Click the App Launcher (the 9 dots in the top left) and search for Recycle Bin.
3. Select the Recycle Bin app. 
4. By default, it shows My Recycle Bin. If the user didn't delete the record but needs it back, a System Admin must switch the view to Org Recycle Bin.
5. Use the search bar in the top right of the list to find the name of the deleted record.
6. Check the box next to the record name.
7. Click the Restore button in the top right corner.
8. The record will be returned to its original state, including its related lists (like Tasks and Notes).

## Escalate if
- The record is missing from the Recycle Bin but was deleted less than 15 days ago.
- The user restores the record, but all the associated "Related" data (like attachments or child opportunities) is missing.
- The user needs to restore more than 250 records at once (requires an admin to use Data Loader or the Recycle Bin API).

## Ticket fields to capture (when escalating)
- Record Type: (e.g., Lead, Account, Case)
- Record Name: (The exact name of the deleted item)
- Deleted Date: (Approximate time of deletion)