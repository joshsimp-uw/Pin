---
doc_id: KB-D66AF1C789-device_los
title: "Mobile Devices \u2014 iPhone (Email, MFA, OneDrive/Teams) \u2014 Device lost\
  \ or stolen"
service: Mobile (iPhone)
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- mobile
- iphone
- ios
- mfa
- outlook
- onedrive
- device_lost_or_stolen
---

# Device lost or stolen

# iPhone Mobile Devices

Recommended apps: Outlook, Authenticator, OneDrive.

### Device lost or stolen

**Severity:** `S1` — Service down or security risk; user blocked and/or potential compromise. Immediate escalation.

**Symptoms**
- You no longer have the phone
- Concern about account access

**Quick checks**
- Do not approve MFA prompts
- Change password immediately if possible

**Fix steps**
1. Change your ACME password from another device (if possible).
2. Contact IT immediately to secure your account.

**Escalate if**
- Always (security event)

**Ticket fields to capture (when escalating)**
- **Last known time:** Approx time/date


## Escalation logic (for chatbot / help desk)
- Lost/stolen device or suspicious prompts → **S1**
- Account setup blocked with work impact → **S2**
- App stability/how-to with workaround → **S3**
