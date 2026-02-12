---
doc_id: KB-311AEFCBFF
title: Printers — HP LaserJet (USB Connected, Non‑MFP)
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
---

# HP LaserJet USB Printer (Non‑MFP)

ACME remote users connect printers directly via **USB**.

## Common issues

### Printer not printing (nothing happens)

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- Print job disappears
- Print queue stuck
- No output from printer

**Quick checks**
- Confirm printer is powered on
- Confirm USB cable is connected firmly
- Try printing a test page

**Fix steps**
1. Turn the printer off, wait 10 seconds, turn it back on.
2. Unplug and reconnect the USB cable (try a different USB port if available).
3. On Windows: open Printer settings and print a test page.
4. Restart your computer if it still won't print.

**Escalate if**
- Printer shows hardware error lights
- You must print for a business-critical deadline and cannot

**Ticket fields to capture (when escalating)**
- **Printer model:** As printed on device
- **Windows version:** Windows 11 (confirm)

### Printer shows as Offline

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- Windows shows 'Offline'
- Cannot set as default
- Queue errors

**Quick checks**
- Check USB connection
- Ensure the correct printer is selected

**Fix steps**
1. In Windows printer settings, set the HP printer as default.
2. Remove the printer and re-add it if it remains offline.
3. Restart both printer and computer.

**Escalate if**
- Offline status returns immediately after re-adding
- Driver install fails

**Ticket fields to capture (when escalating)**
- **Screenshot:** Printer status screen

### Driver or install problems

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Printer cannot be added
- Driver install errors
- Device not recognized

**Quick checks**
- Try a different USB cable/port if available
- Confirm you have permission to install software (company device)

**Fix steps**
1. Disconnect the printer USB cable.
2. Reboot the computer.
3. Reconnect the printer and follow Windows prompts.
4. If it still fails, contact IT with the exact error.

**Escalate if**
- Install requires admin rights you don't have
- Repeated install failures

**Ticket fields to capture (when escalating)**
- **Exact error:** Copy/paste or screenshot
- **Is this a company device?:** Yes/No


## Escalation logic (for chatbot / help desk)
- Hardware error indicators or driver failures without admin rights → **S2**
- Simple offline/USB issues → **S3**
