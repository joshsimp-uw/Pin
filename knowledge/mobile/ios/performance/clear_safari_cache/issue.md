---
doc_id: KB-Y5Z6A7B8-safari_cache
title: "General — iOS — Clear Safari Cache"
service: Mobile General
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- ios
- safari
- cache
- cookies
- browser
- website
- login
urls: []
---

# Clear Safari Cache

# iOS (Web Browser Data)

Use this guide to resolve issues where internal corporate web apps, SSO login pages (like Okta or Microsoft Entra), or generic websites are stuck in a login loop or displaying outdated information on an iPhone.

### Clear Safari Cache

## Severity:
`S3` — Minor degradation; user cannot access a specific web-based tool on their mobile device but can usually use a laptop as a workaround.

## Symptoms
- A specific website fails to load or looks visually broken (missing images or text).
- The user enters their correct SSO credentials, but the page simply refreshes and asks them to log in again indefinitely.
- The browser displays a "400 Bad Request" or "Cookie Too Large" error.

## Quick checks
- Instruct the user to open Safari, tap the Tabs icon (two overlapping squares), tap the Tab Groups list at the bottom, and select Private to open a Private Browsing window. If the site works perfectly in Private mode, it is a cache/cookie issue.
- Verify the phone has a working internet connection.

## Fix steps
1. Close the Safari app entirely by swiping up from the bottom of the screen and swiping the Safari card away in the app switcher.
2. Open the iOS Settings app.
3. Scroll down and tap on Safari.
4. Scroll down and tap the blue text that says Clear History and Website Data.
5. In the menu that pops up, select All history for the timeframe.
6. Tap the red Clear History button.
7. Reopen Safari and navigate to the problematic website to test again.

## Escalate if
- The "Clear History and Website Data" button is completely greyed out and cannot be tapped (this usually indicates an iOS Screen Time restriction or a strict MDM policy).
- The website still fails to load properly after clearing the data and restarting the phone.
- The site works on cellular data but fails strictly on the corporate Wi-Fi network.

## Ticket fields to capture (when escalating)
- iOS Version: (e.g., iOS 17.4)
- Affected URL: (The specific web address failing to load)
- Private Browsing Test: (Did it work in Private mode? Yes/No)
- Error Message: (Any specific text shown on the webpage)