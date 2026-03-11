---
doc_id: KB-E5F6G7H8-paper_size
title: "Configuration — Printers — Paper Size Mismatch"
service: Printer Configuration
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
- paper
- size
- a4
- letter
- tray
urls: []
---

# Paper Size Mismatch

# Printers (Hardware Configuration)

Use this guide to troubleshoot issues where the printer pauses every print job and waits for manual intervention because the document's digital paper size does not match the physical paper loaded in the trays.

### Paper Size Mismatch

## Severity:
`S3` — Minor degradation; user can force the print by pressing a button on the printer, but it halts automated bulk printing.

## Symptoms
- The HP LaserJet screen displays a prompt saying "Unexpected Paper Size" or "Load Tray 1 with Plain A4".
- The printer beeps and flashes an orange error light until the user presses the "OK" or "Continue" button on the physical control panel.
- Print jobs from specific applications (like downloaded PDFs) trigger the error, while blank Word documents print fine.

## Quick checks
- Pull open the physical paper tray (usually Tray 2) and verify the blue plastic guides are snapped snugly against the paper, ensuring the printer sensors detect it as Letter (8.5x11) size.
- Ask the user if the document originated from an international source (which often defaults to A4 size).

## Fix steps
1. In the application the user is printing from (e.g., Microsoft Word), click the Layout tab and click Size to ensure it is set to Letter (8.5" x 11").
2. In Adobe Acrobat, click Print, then click Page Setup at the bottom left, and ensure the size is set to Letter.
3. Open the Windows Start menu, type Printers & scanners, and open the menu.
4. Click the HP LaserJet, select Manage, then click Printing preferences.
5. Look for the Paper/Quality tab and ensure the Paper Size dropdown is set to Letter, not A4.
6. Look for an option that says "Scale to fit paper size" or "Print document on" and ensure it is targeting Letter. Click Apply and OK.

## Escalate if
- The physical tray sensors are broken, causing the printer to constantly think the tray is loaded with A4 regardless of the guide positions.
- The printer ignores all driver settings and continues to demand manual feed from Tray 1 for every single job.

## Ticket fields to capture (when escalating)
- Printer Model: (e.g., HP LaserJet Enterprise M507)
- Application: (The app triggering the mismatch)
- Exact Error Message: (The specific text on the printer's LCD screen)