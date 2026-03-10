---
doc_id: KB-BCB80295BF-email_not_
title: "Mobile Devices \u2014 Android (Email, MFA, OneDrive/Teams) \u2014 Email not\
  \ syncing in Outlook app"
service: Mobile (Android)
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- mobile
- android
- mfa
- outlook
- onedrive
- email_not_syncing_in_outlook_app
---

# Email not syncing in Outlook app

# Android Mobile Devices

Common setups: Outlook app, Authenticator app, OneDrive app.

### Email not syncing in Outlook app

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- New mail not arriving
- Sync errors
- App stuck loading

**Quick checks**
- Confirm phone has internet
- Update Outlook app

**Fix steps**
1. Force close Outlook and reopen it.
2. Update Outlook from the app store.
3. Remove the ACME account from Outlook and add it again if sync remains broken.

**Escalate if**
- You cannot add the account back
- MFA cannot be completed

**Ticket fields to capture (when escalating)**
- **Phone model:** Optional
- **Android version:** Optional
