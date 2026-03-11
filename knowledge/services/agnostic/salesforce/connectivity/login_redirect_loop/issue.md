---
doc_id: KB-L1R2D3L4-login_loop
title: "Connectivity — Salesforce — Login Redirect Loop"
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
- login
- redirect
- loop
- browser
- cookies
- cache
- sso
urls: []
---

# Login Redirect Loop

# Salesforce (Browser Connectivity)

Use this guide to troubleshoot issues where a user attempts to log into Salesforce, but the browser flickers between URLs indefinitely or returns an error stating "Too many redirects".

### Login Redirect Loop

## Severity:
`S3` — Minor degradation; the user is blocked from the web interface but can often still access Salesforce via the mobile app or API integrations.

## Symptoms
- The browser address bar rapidly changes between the corporate My Domain URL and the standard login page.
- The browser eventually displays a white screen with the message "The page isn't redirecting properly."
- The issue occurs specifically after the user successfully completes an MFA or SSO challenge.

## Quick checks
- Check if the user has multiple Salesforce tabs open in the same browser window, which can cause session token conflicts.
- Verify if the user is using an unsupported browser or an outdated version of Chrome or Edge.

## Fix steps
1. Instruct the user to completely close all open browser windows and tabs.
2. Open a new Incognito or InPrivate window and attempt to log in. If this works, the issue is definitely stored local browser data.
3. In the standard browser window, navigate to Settings > Privacy and Security > Cookies and other site data.
4. Select See all site data and search for salesforce.com. 
5. Click the trash can icon to remove all cookies related to Salesforce.
6. Search for the company's specific My Domain (e.g., acme--c.visualforce.com) and remove those cookies as well.
7. Restart the browser and log in normally.

## Escalate if
- The redirect loop persists even in an Incognito window (indicating a server-side configuration error with the My Domain settings).
- The user is being redirected to a custom login page that is currently down for maintenance.
- The issue only occurs when the user is on the corporate VPN, suggesting a proxy server is stripping required session headers.

## Ticket fields to capture (when escalating)
- Browser and Version: (e.g., Chrome v122)
- My Domain URL: (The specific company login URL)
- Incognito Test Result: (Did it work in private mode? Yes/No)