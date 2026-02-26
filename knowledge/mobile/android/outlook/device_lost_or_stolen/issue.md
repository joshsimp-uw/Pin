---
doc_id: KB-BCB80295BF-device_los
title: "Mobile Devices \u2014 Android (Email, MFA, OneDrive/Teams) \u2014 Device lost\
  \ or stolen"
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
- device_lost_or_stolen
---

# Device lost or stolen

# Android Mobile Devices

Common setups: Outlook app, Authenticator app, OneDrive app.

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
