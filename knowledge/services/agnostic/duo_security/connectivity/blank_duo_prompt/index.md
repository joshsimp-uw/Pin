---
doc_id: KB-M3N4O5P6-blank_prompt
title: "Connectivity — Duo Security — Blank Duo Prompt"
service: Identity and Access Management
audience:
- End Users
- Helpdesk
owner: Identity Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- duo
- prompt
- blank
- white-screen
- browser
- extension
- blocked
urls: []
---

# Blank Duo Prompt

# Duo Security (Browser Troubleshooting)

Use this guide to resolve issues where the Duo authentication window fails to load, displaying only a blank white box or an endlessly spinning loading circle when the user attempts to log into a web application.

### Blank Duo Prompt

## Severity:
`S3` — Minor degradation; user cannot log into a specific web-based tool but can usually access desktop applications or use an alternate browser.

## Symptoms
- The web page loads perfectly until the SSO redirect hits the Duo authentication step, at which point the iFrame or popup remains completely blank.
- A "Connection refused" or "Site cannot be reached" error appears exclusively inside the Duo prompt box.
- The user is using a heavily customized browser or is on a restricted guest Wi-Fi network.

## Quick checks
- Instruct the user to copy the URL and open it in an Incognito (Chrome) or InPrivate (Edge) window. If the Duo prompt loads perfectly there, the issue is caused by a local browser extension or corrupted cache.
- Ask if the user recently installed a strict ad-blocker like uBlock Origin or a privacy extension like Privacy Badger.

## Fix steps
1. Click the puzzle piece or extension icon in the top right corner of the web browser.
2. Locate any ad-blockers, pop-up blockers, or script-blocking extensions.
3. Pause or disable these extensions specifically for the current site, or globally as a test.
4. Refresh the page to see if the Duo prompt loads.
5. If extensions are not the cause, open the browser settings and navigate to the Privacy and Security section.
6. Look for Cookies and other site data and ensure that Block third-party cookies is turned off. Duo relies on third-party cookies to remember devices and pass authentication tokens back to the main application.
7. Clear the browser cache and cookies, completely close the browser, reopen it, and attempt the login again.

## Escalate if
- The prompt is blank across all installed web browsers (Chrome, Edge, Firefox) and in Incognito mode.
- The issue is only happening when the user is connected to a specific corporate office network (indicating a firewall or proxy is blocking Duo's cloud IP addresses).
- The prompt loads but immediately displays a red banner stating "Access denied by policy".

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Browser Used: (e.g., Firefox v123)
- Incognito Test Result: (Did the prompt load in private mode? Yes/No)
- Application: (The web app the user was trying to access)