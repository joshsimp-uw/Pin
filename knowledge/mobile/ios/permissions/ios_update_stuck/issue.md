---
doc_id: KB-K7L8M9N0-update_stuck
title: "Performance — iOS — iOS Update Stuck"
service: Mobile Performance
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- ios
- update
- upgrade
- stuck
- software
- firmware
urls: []
---

# iOS Update Stuck

# iOS (Software Updates)

Use this guide to assist users who are trying to update their device OS to comply with corporate security baselines, but the download or installation is frozen.

### iOS Update Stuck

## Severity:
`S3` — Minor degradation; user can work normally, but might be locked out of corporate apps if they miss the compliance deadline for the update.

## Symptoms
- The Software Update screen is permanently stuck on "Preparing Update..." or "Estimating Time Remaining..."
- The Download and Install button is greyed out.
- The update downloads completely but fails to install, throwing an error message.

## Quick checks
- Verify the iPhone is plugged into a power source and connected to Wi-Fi. (iOS will often pause updates if the battery is below 50% or if it's relying on a cellular connection).
- Check if the device has enough free storage space to unpack the update (usually requires at least 5GB).

## Fix steps
1. Force close the Settings app by swiping up from the bottom of the screen to open the app switcher, then swiping the Settings card away.
2. Open Settings again, tap General, and select iPhone Storage.
3. Scroll down the list of apps and look for the downloaded iOS update file (it will have a gear icon and the iOS version number).
4. Tap the iOS update file and select Delete Update. Confirm the deletion.
5. Restart the iPhone (Volume Up, Volume Down, hold Side button).
6. Once rebooted, go back to Settings > General > Software Update to re-download a fresh copy of the update.

## Escalate if
- The update repeatedly fails with a specific error code (e.g., Error 4000).
- The phone is stuck on the black screen with the Apple logo and a progress bar that hasn't moved in over an hour.
- The MDM profile is actively blocking the user from updating the software, displaying a "Your organization manages this update" message when it shouldn't be.

## Ticket fields to capture (when escalating)
- Current iOS Version: (e.g., iOS 16.5)
- Target iOS Version: (e.g., iOS 17.4)
- Available Storage: (e.g., 12GB Free)
- Error Message: (Any specific text shown during the failure)