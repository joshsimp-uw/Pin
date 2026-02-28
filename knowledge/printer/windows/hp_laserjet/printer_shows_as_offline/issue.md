---
doc_id: KB-311AEFCBFF-printer_sh
title: "Printers \u2014 HP LaserJet (USB Connected, Non\u2011MFP) \u2014 Printer shows\
  \ as Offline"
service: USB Printing (HP LaserJet)
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- printer
- hp
- laserjet
- usb
- printer_shows_as_offline
---

# Printer shows as Offline

# HP LaserJet USB Printer (Non‑MFP)

ACME remote users connect printers directly via **USB**.

### Printer shows as Offline

## Severity:
`S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

## Symptoms
- Windows shows 'Offline'
- Cannot set as default
- Queue errors

## Quick checks
- Check USB connection
- Ensure the correct printer is selected

## Fix steps
1. In Windows printer settings, set the HP printer as default.
2. Remove the printer and re-add it if it remains offline.
3. Restart both printer and computer.

## Escalate if
- Offline status returns immediately after re-adding
- Driver install fails

## Ticket fields to capture (when escalating)
- Screenshot: Printer status screen
