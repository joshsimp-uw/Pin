---
doc_id: KB-H4I5J6K7-stuck_queue
title: "General — Printers — Stuck Print Queue"
service: Printer Software
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- hp
- laserjet
- printer
- queue
- spooler
- stuck
- delete
- cancel
urls: []
---

# Stuck Print Queue

# Printers (Spooler Service)

Use this guide to resolve software bottlenecks where a corrupted print job locks up the Windows Print Spooler, preventing the user from cancelling the job or sending new ones to the HP LaserJet.

### Stuck Print Queue

## Severity:
`S3` — Minor degradation; user cannot print from their computer until the local cache is forcefully cleared.

## Symptoms
- A document sits in the Windows print queue with a status of "Spooling" or "Deleting" indefinitely.
- Right-clicking the document and selecting "Cancel" does nothing.
- Sending new documents simply stacks them up behind the stuck job.

## Quick checks
- Check the physical printer screen. If it says "Printing" but nothing is happening, reboot the printer itself first. If the printer screen is on the normal home menu, the issue is entirely on the Windows side.

## Fix steps
1. Open the Windows Start menu, type cmd, right-click Command Prompt, and select Run as administrator.
2. In the black window, type `net stop spooler` and press Enter. Wait for the message saying the service stopped successfully.
3. Leave the command prompt window open.
4. Press the Windows Key + R to open the Run dialog, type `C:\Windows\System32\spool\PRINTERS` and hit Enter.
5. If prompted, click Continue to gain permanent access to this folder.
6. Delete every single file inside this folder (these are the corrupted temporary `.SHD` and `.SPL` files). Do not delete the PRINTERS folder itself, just the contents.
7. Go back to the command prompt window, type `net start spooler` and press Enter.
8. The print queue will now be completely empty, and the user can attempt to print their document again.

## Escalate if
- The command prompt throws an "Access Denied" error when trying to stop the spooler service due to local group policy restrictions.
- The `net stop spooler` command hangs indefinitely and never successfully stops.
- The queue immediately gets stuck on "Spooling" again the very next time the user tries to print the same PDF (indicating the PDF itself is too complex or corrupted, requiring it to be "Printed as Image" in Adobe).

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Printer Model: (e.g., HP LaserJet Pro MFP M428fdw)
- Affected Application: (e.g., Google Chrome PDF Viewer)
- Error Message: (Any access denied errors encountered)