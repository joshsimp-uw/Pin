---
doc_id: KB-Z1O2O3M4-camera_background
title: "Configuration — Zoom — Camera and Background Settings"
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
- camera
- video
- background
- virtual-background
- mirror
- blurry
urls: []
---

# Camera and Background Settings

# Zoom (Video Configuration)

Use this guide to assist users whose video appears mirrored, upside down, or blurry, as well as users struggling to apply corporate virtual backgrounds correctly.

### Camera and Background Settings

## Severity:
`S4` — Proactive request; the user is able to participate in the meeting, but their professional presentation is hindered by visual settings.

## Symptoms
- The user's video feed looks backwards (text on their shirt or a whiteboard is unreadable).
- The user tries to apply a virtual background, but their face blends into the background or the image flickers.
- The video appears grainy or significantly darker than the actual room lighting.

## Quick checks
- Ensure the user has removed any physical privacy sliders or stickers from their webcam lens.
- Verify the user is not sitting directly in front of a bright window, which causes backlighting issues that interfere with virtual backgrounds.

## Fix steps
1. Open the Zoom desktop client and click the Gear icon in the top right to open Settings.
2. Click the Video tab in the left sidebar.
3. Under the preview window, check or uncheck Mirror my video. Note: Zoom mirrors your view by default so it feels like a mirror, but participants see you correctly.
4. If the image is dark, check the box for Adjust for low light and set it to Manual or Auto.
5. Navigate to the Background and Effects tab.
6. Select a virtual background. If the image is bleeding into the user's clothes, click the color picker under I have a green screen (even if they do not) and select the most solid color behind them.
7. If the background option is missing, ensure the user has a computer with a supported processor (Core i5 or higher generally required for background removal without a physical green screen).

## Escalate if
- The camera preview is completely black even after selecting the correct hardware device from the dropdown.
- The Virtual Background menu is missing entirely (indicating it has been disabled at the account level by a Zoom admin).
- The user's video flickers or shows green bars (suggesting a failing hardware driver or GPU issue).

## Ticket fields to capture (when escalating)
- Camera Model: (e.g., Integrated Webcam or Logitech C920)
- CPU Model: (e.g., Intel i7-12700H)
- Virtual Background Status: (Enabled/Disabled/Missing)