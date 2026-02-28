---
doc_id: KB-BCB80295BF-mfa_prompt
title: "Mobile Devices \u2014 Android (Email, MFA, OneDrive/Teams) \u2014 MFA prompts\
  \ not arriving"
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
- mfa_prompts_not_arriving
---

# MFA prompts not arriving

# Android Mobile Devices

Common setups: Outlook app, Authenticator app, OneDrive app.

### MFA prompts not arriving

## Severity:
`S2` — Major degradation; user work significantly impacted. Escalate within same business day.

## Symptoms
- No push notifications
- Authenticator shows no request

## Quick checks
- Enable notifications for Authenticator
- Open Authenticator manually

## Fix steps
1. Open Authenticator and check for pending approvals.
2. Enable notifications for the app.
3. Restart the phone and try again.

## Escalate if
- Lost phone or replaced phone
- Repeated unexpected prompts (possible compromise)

## Ticket fields to capture (when escalating)
- Unexpected prompts: Yes/No
