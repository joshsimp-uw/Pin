---
doc_id: KB-M3N4O5P6-airpods_connect
title: "Connectivity — iOS — AirPods Won't Connect"
service: Mobile Connectivity
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- ios
- bluetooth
- airpods
- headset
- audio
- pairing
urls: []
---

# AirPods Won't Connect

# iOS (Bluetooth Configuration)

Use this guide to troubleshoot issues where a user's AirPods or Bluetooth headset will not pair with their corporate iPhone, or the audio keeps routing through the phone speaker during conference calls.

### AirPods Won't Connect

## Severity:
`S3` — Minor degradation; user can still take calls via the handset or speakerphone, but hands-free workflow is disrupted.

## Symptoms
- The AirPods show as "Not Connected" in the Bluetooth menu and tapping them does nothing.
- The user is on a Teams or Zoom call, but the Bluetooth headset does not appear as an audio option.
- One AirPod is working but the other is silent.

## Quick checks
- Ensure the iPhone's Bluetooth is toggled on in the Control Center.
- Confirm the AirPods are charged by placing them in the case and checking for a green or amber light.

## Fix steps
1. Open the Settings app on the iPhone and tap Bluetooth.
2. Find the AirPods in the list of My Devices and tap the blue "i" icon next to them.
3. Tap Forget This Device and confirm.
4. Place both AirPods in their charging case and keep the lid open.
5. Press and hold the setup button on the back of the case for about 15 seconds, until the status light flashes amber, then white.
6. Hold the AirPods case close to the iPhone and wait for the setup animation to appear on the screen. Tap Connect.

## Escalate if
- The Bluetooth toggle in Settings is completely greyed out and cannot be turned on (indicating a physical hardware failure on the iPhone).
- The AirPods successfully connect to the user's personal iPad or Mac, but permanently refuse to pair with the corporate iPhone.
- Audio heavily distorts or drops out only when using corporate VoIP apps (Teams/Zoom) but works fine for native phone calls.

## Ticket fields to capture (when escalating)
- iOS Version: (e.g., iOS 17.4)
- Headset Model: (e.g., AirPods Pro 2nd Gen)
- Issue Scope: (Does it fail on all calls, or just Teams/Zoom?)