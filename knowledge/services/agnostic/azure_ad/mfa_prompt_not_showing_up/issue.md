---
doc_id: KB-D07430F365-mfa_prompt
title: "Identity & Access \u2014 Azure AD / Microsoft 365 (Remote Users) \u2014 MFA\
  \ prompt not showing up"
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
- mfa_prompt_not_showing_up
urls:
- https://login.microsoftonline.com
- https://portal.office.com
---

# MFA prompt not showing up

# Identity & Access (Azure AD / Microsoft 365)

**Who this is for:** Remote ACME employees who sign in with `@acme.com`.

## What you need
- Your ACME email address (example: `firstname.lastname@acme.com`)
- Your password
- MFA approval (Authenticator app)

### MFA prompt not showing up

## Severity:
`S2` — Major degradation; user work significantly impacted. Escalate within same business day.

## Symptoms
- No push prompt appears
- Authenticator shows no request
- Sign-in hangs waiting for approval

## Quick checks
- Make sure your phone has internet
- Open Authenticator app manually
- Check notifications are enabled for Authenticator

## Fix steps
1. On your phone, open the Authenticator app and look for a pending request.
2. If nothing appears, choose 'Sign in another way' and try an alternate method if available.
3. Restart your phone and try again.

## Escalate if
- You changed phones and can’t approve MFA
- You lost access to your MFA device

## Ticket fields to capture (when escalating)
- MFA method: Authenticator/SMS/etc (if known)
- Phone change?: Yes/No
