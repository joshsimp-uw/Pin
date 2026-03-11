---
doc_id: KB-Z3S4P5S6-blurry_screenshare
title: "General — Zoom — Blurry Screen Share Performance"
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
- screenshare
- blurry
- performance
- lag
- quality
- fps
urls: []
---

# Blurry Screen Share Performance

# Zoom (Visual Quality)

Use this guide to troubleshoot scenarios where a user is sharing their screen but other participants report the image is unreadable, blurry, or significantly delayed.

### Blurry Screen Share Performance

## Severity:
`S3` — Minor degradation; the meeting continues, but the primary purpose of the session (collaboration on documents or code) is hindered by poor visibility.

## Symptoms
- Participants state they cannot read the text on the shared screen.
- The shared image only updates every few seconds (low frame rate).
- The presenter sees a notification: Your internet connection is unstable during the share.

## Quick checks
- Verify if the user is sharing a video or an animation. If so, they must check the "Optimize for Video Clip" box in the share window.
- Check the user's monitor resolution. Sharing a 4K monitor over a standard home internet connection often results in heavy compression and blurriness.

## Fix steps
1. Instruct the user to stop the current screen share.
2. Click the Share Screen button again but do not select a window yet.
3. Look for the checkbox at the bottom left that says Optimize for Video Clip. If they are sharing static text, ensure this is unchecked. If sharing video, ensure it is checked.
4. Go to the Zoom desktop app Settings > Share Screen > Advanced.
5. Under Screen capture mode, change the setting from Auto to Legacy operating system capture or Secure share with window filtering.
6. Ensure the box for Limit your screen share to [X] frames per second is NOT checked, unless the user is on an extremely low-bandwidth connection.
7. If the user has multiple monitors, suggest they share the monitor with the lowest resolution (e.g., the 1080p laptop screen instead of an external 4K display).

## Escalate if
- The screen share quality is poor across all participants and all networks (suggesting a failing integrated graphics card or driver).
- The user receives an error: Screen sharing failed to start.
- The user is on a high-speed wired connection but the blurriness persists.

## Ticket fields to capture (when escalating)
- Monitor Resolution: (e.g., 3840 x 2160)
- Connection Type: (Wi-Fi vs Ethernet)
- Optimize for Video Setting: (Checked/Unchecked)