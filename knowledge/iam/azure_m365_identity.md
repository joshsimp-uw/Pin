---
doc_id: KB-D07430F365
title: Identity & Access — Azure AD / Microsoft 365 (Remote Users)
service: IAM (Azure AD / Microsoft 365)
audience:
  - End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
  - iam
  - azure_ad
  - m365
  - mfa
  - password
urls:
  - https://login.microsoftonline.com
  - https://portal.office.com
---

# Identity & Access (Azure AD / Microsoft 365)

**Who this is for:** Remote ACME employees who sign in with `@acme.com`.

## What you need
- Your ACME email address (example: `firstname.lastname@acme.com`)
- Your password
- MFA approval (Authenticator app)

## Common issues

### Can't sign in (wrong password / expired password)

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Sign-in fails on Microsoft login page
- Password prompts repeat
- Message mentions password is incorrect/expired

**Quick checks**
- Confirm you are signing in with your ACME email address
- Make sure Caps Lock is off
- Try signing in at https://portal.office.com

**Fix steps**
1. Try again carefully (type password manually).
2. If you recently changed your password, wait 5 minutes and try again.
3. Restart your device, then try again.
4. If you still can’t sign in, request a password reset from IT.

**Escalate if**
- You are locked out and cannot self-recover
- You suspect someone else has your password

**Ticket fields to capture (when escalating)**
- **User impact:** Cannot access Microsoft 365 or related services
- **When it started:** Approx time/date
- **Any error text:** Copy/paste or screenshot

### MFA prompt not showing up

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- No push prompt appears
- Authenticator shows no request
- Sign-in hangs waiting for approval

**Quick checks**
- Make sure your phone has internet
- Open Authenticator app manually
- Check notifications are enabled for Authenticator

**Fix steps**
1. On your phone, open the Authenticator app and look for a pending request.
2. If nothing appears, choose 'Sign in another way' and try an alternate method if available.
3. Restart your phone and try again.

**Escalate if**
- You changed phones and can’t approve MFA
- You lost access to your MFA device

**Ticket fields to capture (when escalating)**
- **MFA method:** Authenticator/SMS/etc (if known)
- **Phone change?:** Yes/No

### Suspicious sign-in alert

**Severity:** `S1` — Service down or security risk; user blocked and/or potential compromise. Immediate escalation.

**Symptoms**
- You received a sign-in alert you did not initiate
- Unexpected MFA prompts
- Microsoft reports unusual activity

**Quick checks**
- Do not approve unexpected MFA prompts
- Change your password immediately if you can

**Fix steps**
1. If you can sign in: change your password immediately.
2. Do not approve any MFA prompts you did not start.
3. Report the alert to IT right away.

**Escalate if**
- Any sign-in you did not initiate
- Repeated unexpected MFA prompts

**Ticket fields to capture (when escalating)**
- **Alert details:** Time/location/device shown in alert
- **Did you approve?:** Yes/No


## Escalation logic (for chatbot / help desk)
- If the user **cannot sign in at all** → start as **S2**.
- If there is **suspected compromise** or **unexpected MFA prompts** → **S1** immediately.
- If user has a workaround (already signed in elsewhere) → **S3** and guide cleanup.
