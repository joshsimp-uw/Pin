---
doc_id: KB-T5Z6O7N8-user_timezone
title: "Configuration — Salesforce — Incorrect User Timezone"
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
- timezone
- gmt
- time
- calendar
- tasks
- dead-lines
urls: []
---

# Incorrect User Timezone

# Salesforce (Regional Settings)

Use this guide to resolve issues where a user's Salesforce timestamps, task deadlines, and event reminders are showing the wrong time, typically defaulting to GMT or a corporate headquarters time zone.

### Incorrect User Timezone

## Severity:
`S3` — Minor degradation; the user is able to work, but scheduled tasks and activity logs are confusing and inaccurate for their local region.

## Symptoms
- The user receives an alert for a meeting that says it starts at 2:00 PM, but their local clock says 10:00 AM.
- Activity history timestamps on Lead records do not match the time the user actually made the call.
- All times in the system end in "GMT" or "UTC" instead of a local designation like "PST" or "EST".

## Quick checks
- Ask the user if they recently traveled or if they are a new hire whose profile was cloned from a user in a different region.
- Verify the computer's local Windows clock is set correctly, as Salesforce sometimes uses browser-side scripts to calculate time differences.


## Fix steps
1. Instruct the user to log into Salesforce and click on their Avatar/Profile picture in the top right corner.
2. Select Settings from the dropdown menu.
3. In the left-hand navigation pane, click on Language & Time Zone (under the "Language & Locale" section).
4. Locate the Time Zone dropdown menu.
5. Change the selection to the user's actual local time zone (e.g., (GMT-08:00) Pacific Standard Time (America/Los_Angeles)).
6. Click Save at the top or bottom of the page.
7. Instruct the user to refresh their browser. All record timestamps and calendar events will now display in their local time.

## Escalate if
- The Time Zone field is greyed out or missing from the user's settings page (indicating it is being forcibly overridden by a System Admin via a global profile setting).
- The user changes their time zone, but the reports they run still display data in a different time zone (Reporting Time Zone is a separate setting managed by administrators).

## Ticket fields to capture (when escalating)
- User Location: (e.g., London, UK vs. New York, USA)
- Current Salesforce Time Zone: (e.g., GMT +00:00)
- Desired Time Zone: (e.g., EST -05:00)