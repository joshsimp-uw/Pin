---
doc_id: KB-Z9W0C1J2-web_client_missing
title: "General — Zoom — Web Client Join Missing"
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
- web-client
- join
- browser
- chrome
- download
- missing-link
urls: []
---

# Web Client Join Missing

# Zoom (Browser Access)

Use this guide to assist users who are unable to install the Zoom desktop client and are missing the option to join a meeting through their web browser.

### Web Client Join Missing

## Severity:
`S3` — Minor degradation; the user is blocked from the meeting because they lack administrative rights to install the full client.

## Symptoms
- The meeting link only prompts the user to "Download & Run Zoom."
- There is no link that says "Join from your browser."
- The user is on a locked-down corporate device or a public computer.

## Quick checks
- Ensure the user has not accidentally dismissed the "Join from your browser" link, which often only appears after a failed download attempt.

## Fix steps
1. Instruct the user to click the meeting link as usual.
2. When the "Download" page appears, wait about 5 seconds.
3. If the link Join from your browser does not appear automatically, click the link that says download here.
4. Immediately after clicking that, look at the bottom of the page. The link Join from your browser should now be visible.
5. If it is still missing, the site administrator may have disabled web-based joining. 
6. An admin must log into the Zoom portal, go to Account Settings > Meeting, and ensure the Show a "Join from your browser" link toggle is turned On.

## Escalate if
- The admin setting is enabled but the link remains hidden for all users.
- The web client loads but the user cannot connect their audio or video (common on older versions of Safari or Internet Explorer).

## Ticket fields to capture (when escalating)
- Browser: (e.g., Chrome, Safari)
- Device Type: (e.g., Windows Laptop vs Chromebook)
- Admin Setting Status: (Is Join from Browser enabled?)