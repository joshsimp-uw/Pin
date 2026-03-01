---
doc_id: KB-D07430F365-can_t_sign
title: "Identity & Access \u2014 Azure AD / Microsoft 365 (Remote Users) \u2014 Can't\
  \ sign in (wrong password / expired password)"
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
- can_t_sign_in_wrong_password_expired_password
urls:
- https://login.microsoftonline.com
- https://portal.office.com
---

# Can't sign in (wrong password / expired password)

# Identity & Access (Azure AD / Microsoft 365)

**Who this is for:** Remote ACME employees who sign in with `@acme.com`.

## What you need
- Your ACME email address (example: `firstname.lastname@acme.com`)
- Your password
- MFA approval (Authenticator app)

### Can't sign in (wrong password / expired password)

## Severity:
`S2` — Major degradation; user work significantly impacted. Escalate within same business day.

## Symptoms
- Sign-in fails on Microsoft login page
- Password prompts repeat
- Message mentions password is incorrect/expired

## Quick checks
- Confirm you are signing in with your ACME email address
- Make sure Caps Lock is off
- Try signing in at https://portal.office.com

## Fix steps
1. Try again carefully (type password manually).
2. If you recently changed your password, wait 5 minutes and try again.
3. Restart your device, then try again.
4. If you still can’t sign in, request a password reset from IT.

## Escalate if
- You are locked out and cannot self-recover
- You suspect someone else has your password

## Ticket fields to capture (when escalating)
- User impact: Cannot access Microsoft 365 or related services
- When it started: Approx time/date
- Any error text: Copy/paste or screenshot
