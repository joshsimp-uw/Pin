---
doc_id: KB-I9J0K1L2-missing_notifications
title: "Configuration — iOS — Missing App Notifications"
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
- notifications
- focus
- dnd
- alerts
- teams
- outlook
urls: []
---

# Missing App Notifications

# iOS (Notification Configuration)

Use this guide to troubleshoot scenarios where a user is not receiving incoming call rings, banner alerts, or badge icons for crucial corporate applications like Microsoft Teams or Outlook.

### Missing App Notifications

## Severity:
`S3` — Minor degradation; user is missing real-time alerts but can still manually open apps to check for updates.

## Symptoms
- The user completely misses an incoming Teams call because the phone did not ring or wake up.
- New emails arrive in the inbox, but no banner drops down from the top of the screen.
- The red number badge icon is missing from the app on the home screen.

## Quick checks
- Check the physical Ring/Silent switch on the left side of the iPhone to ensure it is not showing orange (Silent mode).
- Press the Volume Up button a few times while on the home screen to ensure the ringer volume is not muted.

## Fix steps
1. Swipe down from the top-right corner of the screen to open the Control Center.
2. Look at the Focus / Do Not Disturb button (the moon icon). If it is highlighted, tap it to turn it off.
3. Open the Settings app and tap Notifications.
4. Scroll down the app list and tap on the affected app (e.g., Teams).
5. Ensure the Allow Notifications toggle at the very top is green.
6. Under Alerts, ensure Lock Screen, Notification Center, and Banners are all checked.
7. Go back to the main Settings menu and tap Focus.
8. If the user has a Mac or iPad, scroll down and toggle Share Across Devices to off, to prevent a laptop's "Do Not Disturb" from silencing their phone.

## Escalate if
- All notification settings are correct, but the app still remains silent.
- The issue persists even after uninstalling and reinstalling the affected application.
- The user is missing notifications for a Multi-Factor Authentication (MFA) app, completely blocking their ability to log into their computer.

## Ticket fields to capture (when escalating)
- iOS Version: (e.g., iOS 17.4)
- Affected App: (e.g., Microsoft Teams)
- Focus Mode Status: (Was Focus or DND turned on? Yes/No)