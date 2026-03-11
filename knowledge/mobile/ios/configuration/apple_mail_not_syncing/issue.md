---
doc_id: KB-A1B2C3D4-apple_mail_sync
title: "Configuration — iOS — Apple Mail Not Syncing"
service: Mobile Configuration
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- ios
- mail
- email
- sync
- exchange
- 365
urls: []
---

# Apple Mail Not Syncing

# iOS (Email Configuration)

Use this guide to troubleshoot issues where the native Apple Mail app stops receiving or sending corporate emails, usually due to an expired authentication token or a recent password change.

### Apple Mail Not Syncing

## Severity:
`S3` — Minor degradation; user cannot check mail on mobile but can still access it via desktop or webmail.

## Symptoms
- Pulling down to refresh the inbox results in a "Cannot Get Mail" error at the bottom of the screen.
- Emails sent from the device remain stuck in the Outbox folder.
- The inbox has not updated with new messages for several hours or days.

## Quick checks
- Open Safari to verify the device has a working cellular data or Wi-Fi connection.
- Ask the user if they recently changed their corporate Active Directory password.

## Fix steps
1. Open the Settings app on the iPhone.
2. Scroll down and tap on Mail, then tap on Accounts.
3. Tap on the corporate Exchange or Microsoft 365 account.
4. Look for a prompt that says Re-enter Password or Account Error and tap it to authenticate.
5. If no prompt exists, toggle the Mail switch off, wait ten seconds, and toggle it back on.
6. Force close the Mail app by swiping up from the bottom of the screen to open the app switcher, then swiping the Mail app away. Reopen the app.

## Escalate if
- The user enters their correct new password but is repeatedly asked to enter it again (an authentication loop).
- The corporate account is entirely missing from the Accounts list and cannot be added manually due to MDM restrictions.
- The device requires the Microsoft Outlook app for corporate email instead of native Apple Mail per company policy.

## Ticket fields to capture (when escalating)
- iOS Version: (e.g., iOS 17.4)
- Mail App Used: (Native Apple Mail vs. Microsoft Outlook)
- Error Message: (The exact text shown when refreshing)
- Last Successful Sync: (Date and time of the last received email)