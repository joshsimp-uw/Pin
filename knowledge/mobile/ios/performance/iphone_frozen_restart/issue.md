---
doc_id: KB-C9D0E1F2-iphone_frozen
title: "General — iOS — iPhone Frozen or Unresponsive"
service: Mobile General
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- ios
- frozen
- crash
- reboot
- restart
- screen
- hardware
urls: []
---

# iPhone Frozen or Unresponsive

# iOS (Hardware Troubleshooting)

Use this guide to assist a user whose iPhone has completely locked up, will not respond to screen taps, or is stuck on a black screen despite vibrating or ringing.

### iPhone Frozen Restart

## Severity:
`S2` — High impact; the user's mobile device is entirely unusable for communication or MFA authentication.

## Symptoms
- The screen is frozen on a specific app and swiping up to go home does nothing.
- The phone screen is completely black, but the phone still makes notification sounds or vibrates when the mute switch is toggled.
- The device feels unusually hot to the touch and is unresponsive.

## Quick checks
- Ensure it is the entire phone that is frozen, not just one specific app. If the user can swipe up to go home, they just need to force-close that single app, not restart the whole phone.
- Plug the phone into a known working charger to rule out a completely dead battery.

## Fix steps
1. Instruct the user to perform a "Force Restart" (this sequence must be done relatively quickly).
2. Press and quickly release the Volume Up button on the left side.
3. Press and quickly release the Volume Down button on the left side.
4. Press and hold the Side button (the power button on the right side).
5. Keep holding the Side button for about 10-15 seconds. Ignore the "slide to power off" slider if it appears.
6. Release the Side button only when the white Apple logo appears on the screen.
7. Wait for the phone to boot up and prompt for the lock screen passcode.

## Escalate if
- The phone is stuck in a "boot loop" (the Apple logo flashes on and off repeatedly but never reaches the lock screen).
- The device shows an icon of a laptop and a cable, indicating it needs to be restored via Apple Configurator or iTunes (Recovery Mode).
- The phone remains completely black and unresponsive even after 30 minutes on a charger and multiple Force Restart attempts.

## Ticket fields to capture (when escalating)
- iOS Version: (If known before freezing)
- Device Model: (e.g., iPhone 13 Pro)
- Physical Condition: (Any recent drops or liquid exposure?)
- Boot Status: (Black screen vs. Boot loop vs. Recovery Mode)