---
doc_id: KB-8D8E1A02E9-can_t_log_
title: "Business Application \u2014 Salesforce (Remote Users) \u2014 Can't log in\
  \ to Salesforce"
service: Salesforce
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- salesforce
- crm
- business_app
- can_t_log_in_to_salesforce
dns:
- salesforce.acme.com
urls:
- https://salesforce.acme.com
- https://login.salesforce.com
---

# Can't log in to Salesforce

# Salesforce

## Access
- Primary: **https://salesforce.acme.com**
- Fallback: https://login.salesforce.com

### Can't log in to Salesforce

## Severity:
`S2` — Major degradation; user work significantly impacted. Escalate within same business day.

## Symptoms
- Login fails
- Looping sign-in page
- MFA issues (if enabled)

## Quick checks
- Confirm you can sign in to Microsoft 365 at https://portal.office.com
- Try a private/incognito browser window

## Fix steps
1. Try signing in using a private/incognito window.
2. Clear browser cache for Salesforce and try again.
3. If your password recently changed, retry after a few minutes.

## Escalate if
- All logins fail and you cannot work
- Account appears disabled

## Ticket fields to capture (when escalating)
- Browser: Chrome/Edge/Safari/etc
- Exact error: Copy/paste or screenshot
