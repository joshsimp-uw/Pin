---
doc_id: KB-U1V2W3X4-accidental_deny
title: "General — Duo Security — Accidental Deny Lockout"
service: Identity and Access Management
audience:
- End Users
- Helpdesk
owner: Identity Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- duo
- deny
- lockout
- push
- mistake
- unlock
urls: []
---

# Accidental Deny Lockout

# Duo Security (Account Lockout)

Use this guide to assist users who are locked out of their Duo account because they accidentally tapped the red "Deny" button on a legitimate login attempt and subsequently reported it as fraudulent.

### Accidental Deny Lockout

## Severity:
`S3` — Minor degradation; user is temporarily completely blocked from authenticating to any corporate resource.

## Symptoms
- The Duo prompt on the computer screen immediately displays "Your account has been locked out" when the user attempts to log in.
- The user admits they accidentally tapped Deny on a push notification they triggered, and then tapped "It was a mistake" or "Report fraud".
- The user is unable to receive new push notifications or use passcodes.

## Quick checks
- Verify the identity of the user calling or messaging the helpdesk to ensure it is actually them.
- Ask the user to explicitly confirm they were the one who triggered the original login attempt that they denied. If they did not trigger the login, their primary Active Directory password has been compromised and must be reset immediately.

## Fix steps
1. (Self-Service) Inform the user that the accidental deny lockout is temporary. They can simply wait for the automatic lockout timer to expire (usually 15 to 30 minutes, depending on your organization's security policy).
2. Once the timer expires, they can attempt to log in again and must tap Approve.
3. (Helpdesk) If the user cannot wait, an administrator must log into the Duo Admin Panel.
4. Search for the user's name or username in the top search bar.
5. On the user's profile page, scroll down to the Status section.
6. Change the status from Locked Out back to Active.
7. Click Save Changes and have the user try logging in again immediately.

## Escalate if
- The user states they definitely did not trigger the login attempt (this is an active security incident).
- The user's status in the Duo Admin Panel shows as "Disabled" rather than "Locked Out" (indicating an active directory sync issue or HR offboarding script).
- The lockout persists even after an administrator manually sets the account to Active.

## Ticket fields to capture (when escalating)
- Target Application: (The app the user was trying to access when they denied the prompt)
- Lockout Time: (When the accidental deny occurred)
- Password Reset Required: (Yes/No, if fraud was suspected)