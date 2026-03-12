---
doc_id: KB-D07430F365-suspicious
title: "Identity & Access \u2014 Azure AD / Microsoft 365 (Remote Users) \u2014 Suspicious\
  \ sign-in alert"
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
- suspicious_sign_in_alert
urls:
- https://login.microsoftonline.com
- https://portal.office.com
---

# Suspicious sign-in alert

# Identity & Access (Azure AD / Microsoft 365)

**Who this is for:** Remote ACME employees who sign in with `@acme.com`.

## What you need
- Your ACME email address (example: `firstname.lastname@acme.com`)
- Your password
- MFA approval (Authenticator app)

### Suspicious sign-in alert

## Severity:
`S1` — Service down or security risk; user blocked and/or potential compromise. Immediate escalation.

## Symptoms
- You received a sign-in alert you did not initiate
- Unexpected MFA prompts
- Microsoft reports unusual activity

## Quick checks
- Do not approve unexpected MFA prompts
- Change your password immediately if you can

## Fix steps
1. If you can sign in: change your password immediately.
2. Do not approve any MFA prompts you did not start.
3. Report the alert to IT right away.

## Escalate if
- Any sign-in you did not initiate
- Repeated unexpected MFA prompts

## Ticket fields to capture (when escalating)
- Alert details: Time/location/device shown in alert
- Did you approve?: Yes/No


## Escalation logic (for chatbot / help desk)
- If the user cannot sign in at all → start as S2.
- If there is suspected compromise or unexpected MFA prompts → S1 immediately.
- If user has a workaround (already signed in elsewhere) → S3 and guide cleanup.
