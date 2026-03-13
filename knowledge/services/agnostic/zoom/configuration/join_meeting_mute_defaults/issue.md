---
doc_id: KB-Z9M0D1E2-mute_defaults
title: "Configuration — Zoom — Join Meeting Mute Defaults"
service: Unified Communications
audience:
- End Users
- Helpdesk
owner: Collaboration Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- zoom
- mute
- microphone
- video
- privacy
- join-meeting
- settings
urls: []
---

# Join Meeting Mute Defaults

# Zoom (User Privacy)

Use this guide to help users configure their Zoom client so that their microphone and camera are automatically disabled every time they join a meeting, preventing accidental audio or video transmission.

### Join Meeting Mute Defaults

## Severity:
`S4` — Proactive request; the user wants to ensure privacy and avoid disruptions when joining large calls or webinars.

## Symptoms
- The user complains that their dog was barking or their camera was on before they were ready when joining a call.
- The user wants a "push-to-talk" style experience where they only unmute when necessary.

## Quick checks
- Verify the user knows how to use the Spacebar for temporary unmuting, which is a helpful companion to these settings.

## Fix steps
1. Open the Zoom desktop app and click the Gear icon (Settings).
2. To default the microphone to off: Click the Audio tab.
3. Check the box for Mute my mic when joining a meeting.
4. To default the camera to off: Click the Video tab.
5. Check the box for Turn off my video when joining a meeting.
6. (Optional) In the Video tab, check the box for Always show video preview dialog when joining a video meeting. This gives the user a final look at their feed before they are visible to others.
7. These settings will now persist across all future meetings on this specific device.

## Escalate if
- The user checks these boxes but they are unchecked automatically the next time they open Zoom.
- The user is muted by default but cannot unmute themselves (indicating the host has disabled participant unmuting).
- The "Mute on join" setting is being overridden by a corporate policy forced via an MSI installer.

## Ticket fields to capture (when escalating)
- App Version: (e.g., v5.17.x)
- Operating System: (Windows or macOS)
- Setting Status: (Does it stay checked after a restart? Yes/No)