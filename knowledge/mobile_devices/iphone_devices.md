---
doc_id: KB-D66AF1C789
title: Mobile Devices — iPhone (Email, MFA, OneDrive/Teams)
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
---

# iPhone Mobile Devices

Recommended apps: Outlook, Authenticator, OneDrive.

## Common issues

### Can't add ACME account to Outlook

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Sign-in fails
- MFA loop
- Account won't finish setup

**Quick checks**
- Update Outlook app
- Try setup on Wi‑Fi and then on cellular if possible

**Fix steps**
1. Update Outlook from the App Store.
2. Try adding the account again.
3. If MFA loops, open the Authenticator app and complete the prompt.

**Escalate if**
- You cannot complete setup after multiple tries
- Account appears blocked

**Ticket fields to capture (when escalating)**
- **iOS version:** Optional
- **Exact error:** Copy/paste or screenshot

### Outlook app crashes or freezes

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- App closes unexpectedly
- Freezes on open

**Quick checks**
- Restart phone
- Update app

**Fix steps**
1. Restart your iPhone.
2. Update Outlook.
3. If still crashing, uninstall and reinstall Outlook.

**Escalate if**
- Crashes persist after reinstall and prevents working

**Ticket fields to capture (when escalating)**
- **Steps tried:** Restart/update/reinstall

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
