---
doc_id: KB-BCB80295BF
title: Mobile Devices — Android (Email, MFA, OneDrive/Teams)
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
---

# Android Mobile Devices

Common setups: Outlook app, Authenticator app, OneDrive app.

## Common issues

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

### MFA prompts not arriving

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- No push notifications
- Authenticator shows no request

**Quick checks**
- Enable notifications for Authenticator
- Open Authenticator manually

**Fix steps**
1. Open Authenticator and check for pending approvals.
2. Enable notifications for the app.
3. Restart the phone and try again.

**Escalate if**
- Lost phone or replaced phone
- Repeated unexpected prompts (possible compromise)

**Ticket fields to capture (when escalating)**
- **Unexpected prompts:** Yes/No

### Device lost or stolen

**Severity:** `S1` — Service down or security risk; user blocked and/or potential compromise. Immediate escalation.

**Symptoms**
- You no longer have the phone
- You think someone else has access to your apps

**Quick checks**
- Do not approve any MFA prompts
- Change your password immediately from another device if possible

**Fix steps**
1. From another device, change your ACME password immediately (if you can).
2. Contact IT right away to secure your account.

**Escalate if**
- Always (this is a security event)

**Ticket fields to capture (when escalating)**
- **Last known time:** Approx time/date
- **Phone number:** Optional


## Escalation logic (for chatbot / help desk)
- Lost/stolen device or suspicious prompts → **S1**
- Email/MFA broken with work impact → **S2**
- Minor app guidance → **S3**
