---
doc_id: KB-P1Q2R3S4-not_signed_in
title: "Connectivity — OneDrive — OneDrive Not Signed In"
service: Cloud Storage
audience:
- End Users
- Helpdesk
owner: Cloud Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- onedrive
- login
- sign-in
- offline
- grey
- token
- credentials
urls: []
---

# OneDrive Not Signed In

# OneDrive (Authentication & Connectivity)

Use this guide to assist users whose OneDrive application has silently logged out, usually indicated by a grey cloud icon, stopping all background file backups.

### OneDrive Not Signed In

## Severity:
`S3` — Minor degradation; local files are accessible but are no longer backing up to the cloud, creating a risk of data loss if the device experiences hardware failure.

## Symptoms
- The OneDrive cloud icon in the Windows taskbar system tray is completely grey with a diagonal line through it.
- Hovering over the grey icon displays "OneDrive - Not signed in".
- Newly created or saved documents on the desktop do not show the blue syncing arrows or green checkmarks.

## Quick checks
- Verify the computer has an active internet connection.
- Check if the user recently changed their Active Directory or Microsoft 365 password, which immediately invalidates the local authentication token.

## Fix steps
1. Click the grey OneDrive cloud icon in the system tray.
2. A prompt should appear asking the user to Sign in. Click it.
3. Enter the user's full corporate email address and click Next.
4. Enter the current corporate password and approve any Duo or Microsoft Authenticator MFA prompts.
5. The app will usually say "Your OneDrive folder is already here". Click Use this folder to re-establish the connection without re-downloading everything.
6. Proceed through the rest of the setup wizard until you reach the "Your OneDrive is ready for you" screen.
7. Verify the cloud icon in the system tray has turned blue and is actively processing changes.

## Escalate if
- Entering the correct email address results in a "There was a problem looking up your account" error.
- The user signs in, the icon turns blue, but silently reverts to grey within a few minutes (indicating a corrupted credential cache in the Windows Credential Manager).
- The sign-in window is completely blank or fails to load the authentication page.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Enterprise)
- Error Code: (Any specific 0x error code shown during sign in)
- Password Recently Changed: (Yes/No)