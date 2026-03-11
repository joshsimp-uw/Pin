---
doc_id: KB-B2C3D4E5F6-monitor_layout
title: "Configuration — Endpoints — Monitor Orientation & Layout"
service: Endpoint Hardware
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- monitor
- display
- screen
- orientation
- desktop
urls: []
---

# Monitor Orientation & Layout

# Endpoints (Display Configuration)

Use this guide to troubleshoot physical-to-digital alignment issues where the mouse moves to the wrong screen or the display is upside down/sideways.

### Dual Monitor Orientation

## Severity:
`S3` — Minor degradation; user can still work but navigation is difficult.

## Symptoms
- Moving the mouse to the right causes it to appear on the left monitor.
- One monitor is displaying in "Portrait" mode while physically in "Landscape."
- The main taskbar is appearing on the secondary monitor instead of the primary.

## Quick checks
- Confirm all video cables (HDMI, DisplayPort, USB-C) are securely seated in the dock or laptop.
- Check if the monitor is physically rotated.

## Fix steps
1. Right-click on an empty space on the Desktop and select Display settings.
2. Under Rearrange your displays, click Identify to see which number corresponds to which physical screen.
3. Click and drag the numbered boxes to match the physical layout on your desk. Click Apply.
4. To fix rotation: Select the specific monitor, scroll to Display orientation, and ensure it is set to Landscape.
5. To set the main screen: Select the preferred monitor box and check Make this my main display.

## Escalate if
- The system does not detect the second monitor at all (`lsblk` or Display settings shows only one).
- Display settings are "greyed out" and cannot be changed.
- Screen flickering or extreme "ghosting" occurs on one specific panel.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Connection Type: (e.g., Dell WD19 Dock via USB-C)
- Monitor Model: (e.g., Dell P2419H)
- GPU Driver Version: (Found in Device Manager)