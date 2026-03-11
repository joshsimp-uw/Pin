---
doc_id: KB-I9J0K1L2-printing_gibberish
title: "Configuration — Printers — Printing Gibberish Symbols"
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
- driver
- gibberish
- symbols
- code
- pcl6
urls: []
---

# Printing Gibberish Symbols

# Printers (Driver Troubleshooting)

Use this guide to resolve a critical driver translation issue where the computer sends data the printer cannot understand, resulting in endless pages of random characters, smiley faces, and machine code.

### Printing Gibberish Symbols

## Severity:
`S2` — High impact; the printer is rapidly wasting a massive amount of paper and toner, and the user cannot print legitimate documents.

## Symptoms
- The printer outputs dozens of pages containing just one or two lines of random wingdings, numbers, or ascii characters at the top of the page.
- The issue continues even if the user cancels the job on their computer, as the bad data is already loaded into the printer's memory.
- The printer name in Windows ends in "Class Driver" or "Generic Text".

## Quick checks
- Immediately power off the physical printer using the hard switch to stop the endless printing and save paper.
- Verify if the user recently mapped this printer themselves without using the official corporate print server deployment.

## Fix steps
1. Keep the physical printer turned off.
2. On the user's computer, open the Start menu, type Printers & scanners, and press Enter.
3. Click on the affected HP LaserJet and select Remove device.
4. Press the Windows Key + R, type `control printers`, and hit Enter to open the old Control Panel view.
5. Click on any remaining printer, then click Print server properties at the top of the window.
6. Go to the Drivers tab, locate any HP generic or incorrect drivers associated with that model, and click Remove (select Remove driver and driver package).
7. Download and install the correct "HP PCL-6" or "HP PostScript" driver from the corporate software center or the HP support site.
8. Turn the printer back on. If it immediately starts printing gibberish again, you must cancel the job from the printer's physical control panel.

## Escalate if
- The driver refuses to uninstall, claiming it is currently in use by the system.
- The correct PCL-6 driver is installed, but the gibberish printing persists (indicating a possible corrupted firmware or a severe network spooler issue).

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Printer Model: (e.g., HP Color LaserJet Pro M454)
- Previous Driver Name: (e.g., Microsoft IPP Class Driver)
- Connection Type: (Network IP vs. USB)