---
doc_id: KB-G3H4I5J6-battery_drain
title: "Performance — iOS — Battery Draining Fast"
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
- battery
- power
- drain
- health
- performance
urls: []
---

# Battery Draining Fast

# iOS (Power Management)

Use this guide to troubleshoot devices that are rapidly losing battery charge during normal work hours, requiring the user to stay tethered to a charger.

### Battery Draining Fast

## Severity:
`S3` — Minor degradation; user can continue working but mobility is restricted.

## Symptoms
- The device battery drops from 100% to dead halfway through the workday.
- The back of the iPhone feels unusually warm or hot to the touch during basic tasks.
- The battery percentage jumps erratically (e.g., dropping straight from 30% to 5%).

## Quick checks
- Ensure the user's screen brightness isn't manually set to maximum all day.
- Check if the user is using a personal hotspot, which consumes massive amounts of power.

## Fix steps
1. Open the Settings app and scroll down to Battery.
2. Wait a moment for the battery usage graphs to load.
3. Scroll down to the app list to identify which specific application is consuming the highest percentage of battery over the last 24 hours.
4. If a specific app is draining the battery in the background, navigate to Settings > General > Background App Refresh.
5. Find the culprit app in the list and toggle its background refresh off.
6. Check the physical degradation of the battery by going to Settings > Battery > Battery Health & Charging. Look at the Maximum Capacity percentage.

## Escalate if
- The Maximum Capacity in Battery Health is below 80% or displays a "Service" warning (this indicates the physical lithium-ion battery has degraded and the device needs hardware replacement).
- The battery drain is caused by a mandatory corporate security app (like an MDM agent or mobile antivirus) running out of control.
- The phone shuts off completely while still displaying 20% or more charge.

## Ticket fields to capture (when escalating)
- iOS Version: (e.g., iOS 17.4)
- Battery Health Maximum Capacity: (e.g., 78%)
- Top Consuming App: (e.g., Microsoft Teams at 45%)
- Device Age: (Approximate age in years/months)