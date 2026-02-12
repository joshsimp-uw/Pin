---
doc_id: KB-8D8E1A02E9
title: Business Application — Salesforce (Remote Users)
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
dns:
  - salesforce.acme.com
urls:
  - https://salesforce.acme.com
  - https://login.salesforce.com
---

# Salesforce

## Access
- Primary: **https://salesforce.acme.com**
- Fallback: https://login.salesforce.com

## Common issues

### Can't log in to Salesforce

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Login fails
- Looping sign-in page
- MFA issues (if enabled)

**Quick checks**
- Confirm you can sign in to Microsoft 365 at https://portal.office.com
- Try a private/incognito browser window

**Fix steps**
1. Try signing in using a private/incognito window.
2. Clear browser cache for Salesforce and try again.
3. If your password recently changed, retry after a few minutes.

**Escalate if**
- All logins fail and you cannot work
- Account appears disabled

**Ticket fields to capture (when escalating)**
- **Browser:** Chrome/Edge/Safari/etc
- **Exact error:** Copy/paste or screenshot

### Pages are slow or not loading

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- Salesforce pages take a long time
- Spinning loader
- Some pages never load

**Quick checks**
- Check your internet speed/connection stability
- Try a different browser

**Fix steps**
1. Refresh the page.
2. Try a different browser.
3. Disable browser extensions for the session if possible.

**Escalate if**
- Multiple users report outage
- Salesforce is unusable for business-critical tasks

**Ticket fields to capture (when escalating)**
- **Time observed:** Approx time/date
- **Is it only you?:** Yes/No

### Missing data or insufficient permissions

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- You can't see records you expect
- Buttons/features missing
- Permission denied messages

**Quick checks**
- Confirm you're in the correct Salesforce app/workspace
- Check filters and views

**Fix steps**
1. Verify the record isn't filtered out (views/filters).
2. If you still cannot access, request permission changes via IT/CRM admin.

**Escalate if**
- You need access for business-critical workflow and cannot proceed
- Multiple users affected

**Ticket fields to capture (when escalating)**
- **What access is needed:** Object/record type
- **Example record:** ID or name if known


## Escalation logic (for chatbot / help desk)
- Business-critical login failure/outage → **S2** (or **S1** if suspected compromise)
- Performance issue with workaround → **S3**
- Permissions blocking core work → **S2**
