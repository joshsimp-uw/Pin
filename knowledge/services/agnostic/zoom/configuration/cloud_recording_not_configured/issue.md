---
doc_id: KB-Z5O6R7C8-cloud_recording
title: "Configuration — Zoom — Cloud Recording Not Configured"
service: Unified Communications
audience:
- End Users
- Helpdesk
owner: Collaboration Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- zoom
- recording
- cloud
- storage
- missing-button
- archive
urls: []
---

# Cloud Recording Not Configured

# Zoom (Meeting Archives)

Use this guide to assist users who are unable to record their meetings to the cloud or cannot find the Record button in their meeting toolbar.

### Cloud Recording Not Configured

## Severity:
`S3` — Minor degradation; the user cannot archive important meetings, which may lead to a loss of project documentation or training materials.

## Symptoms
- The Record button is missing from the bottom navigation bar during a meeting the user is hosting.
- When the user clicks Record, they only see an option for "Record on this Computer" and no option for "Record to the Cloud."
- The user receives an email stating their cloud recording failed due to insufficient storage.

## Quick checks
- Verify the user's account type. "Basic" (free) accounts do not have access to cloud recording.
- Check if the user is the actual Host of the meeting. Participants cannot record to the cloud unless granted permission by the host.

## Fix steps
1. Instruct the user to log into the corporate Zoom web portal (company.zoom.us).
2. Click Settings in the left-hand menu.
3. Click the Recording tab at the top.
4. Ensure the toggle for Cloud recording is turned On.
5. Check the specific sub-settings, such as Record active speaker with shared screen, to ensure the desired layout is captured.
6. If the user wants to allow others to record, scroll down to the Local recording section and ensure it is enabled.
7. If the user has run out of space, they must go to the Recordings menu and delete old, unneeded videos to free up their assigned quota.

## Escalate if
- The Cloud recording toggle is greyed out and locked by an administrator.
- The user is a "Licensed" user but the cloud option is still missing after enabling it in settings.
- Recordings are showing as "Processing" for more than 24 hours.

## Ticket fields to capture (when escalating)
- Account License: (Basic or Licensed)
- Meeting ID: (The 11-digit number)
- Recording Type: (Cloud or Local)