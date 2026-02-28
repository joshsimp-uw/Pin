---
doc_id: KB-311AEFCBFF-driver_or_
title: "Printers \u2014 HP LaserJet (USB Connected, Non\u2011MFP) \u2014 Driver or\
  \ install problems"
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
- driver_or_install_problems
---

# Driver or install problems

# HP LaserJet USB Printer (Non‑MFP)

ACME remote users connect printers directly via **USB**.

### Driver or install problems

## Severity:
`S2` — Major degradation; user work significantly impacted. Escalate within same business day.

## Symptoms
- Printer cannot be added
- Driver install errors
- Device not recognized

## Quick checks
- Try a different USB cable/port if available
- Confirm you have permission to install software (company device)

## Fix steps
1. Disconnect the printer USB cable.
2. Reboot the computer.
3. Reconnect the printer and follow Windows prompts.
4. If it still fails, contact IT with the exact error.

## Escalate if
- Install requires admin rights you don't have
- Repeated install failures

## Ticket fields to capture (when escalating)
- Exact error: Copy/paste or screenshot
- Is this a company device?: Yes/No


## Escalation logic (for chatbot / help desk)
- Hardware error indicators or driver failures without admin rights → **S2**
- Simple offline/USB issues → **S3**
