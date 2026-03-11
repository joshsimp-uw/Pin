---
doc_id: KB-Y5Z6A7B8-excessive_failures
title: "General — Duo Security — Excessive MFA Failures"
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
- lockout
- passcode
- failures
- incorrect
- offline
urls: []
---

# Excessive MFA Failures

# Duo Security (Account Lockout)

Use this guide to resolve issues where a user is locked out of the Duo authentication system because they entered an incorrect 6-digit passcode too many times in a row.

### Excessive MFA Failures

## Severity:
`S3` — Minor degradation; user is entirely blocked from logging into corporate applications.

## Symptoms
- The Duo authentication prompt displays an error stating the account is locked due to excessive consecutive authentication failures.
- The user was trying to use a physical hardware token or the offline codes from the Duo Mobile app, and kept guessing or mistyping the numbers.
- The user ignored several Push notifications in a row, causing the system to register them as timed-out failures.

## Quick checks
- Ensure the user is not looking at the passcode for a personal account (like a personal email or social media) stored inside their Duo Mobile app.
- Ask the user if they were letting the push notifications time out repeatedly without answering them.

## Fix steps
1. (Self-Service) Instruct the user that this lockout is temporary. They must wait for the automatic timeout period to expire (usually 15 to 30 minutes) before trying again.
2. (Helpdesk) To immediately bypass the timer, an administrator must log into the Duo Admin Panel.
3. Search for the affected user and open their profile.
4. Locate the Status section and change the dropdown from Locked Out to Active. Click Save Changes.
5. Crucially, before the user tries to log in again, you must fix the root cause of the failures. If they are using the Duo Mobile app offline codes, instruct them to go into the app settings and tap Sync Passcodes to fix clock drift.
6. Have the user attempt a new login and carefully type the fresh passcode.

## Escalate if
- The user is using a physical hardware token (like a YubiKey or Duo token) and the codes are still failing after the account is unlocked (the token itself needs to be resynced in the Admin panel).
- The account immediately locks itself again the second it is unlocked, indicating an automated script or stale cached credential is hammering the login portal.

## Ticket fields to capture (when escalating)
- Authentication Method: (e.g., App Passcode, Hardware Token, Ignored Push)
- Token Serial Number: (If using a physical hardware token)
- Application: (The portal throwing the lockout error)