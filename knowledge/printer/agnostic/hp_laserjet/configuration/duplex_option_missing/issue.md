---
doc_id: KB-A1B2C3D4-duplex_missing
title: "Configuration — Printers — Duplex Option Missing"
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
- duplex
- double-sided
- print
urls: []
---

# Duplex Option Missing

# Printers (Driver Configuration)

Use this guide to resolve issues where a user wants to print on both sides of the page (double-sided/duplex), but the option is greyed out or completely missing from the Windows print dialog.

### Duplex Option Missing

## Severity:
`S3` — Minor degradation; user can still print single-sided, but it wastes paper and disrupts formatted booklets or manuals.

## Symptoms
- The "Print on both sides" dropdown in Word or Acrobat is greyed out.
- The user selects "Print on both sides", but the printer still outputs single-sided pages.
- The printer properties menu shows the duplexer unit as "Not Installed".

## Quick checks
- Verify the specific physical model of the HP LaserJet actually supports automatic duplexing (usually denoted by a "d" in the model name, like M404dn).
- Check if the user is printing from a web browser, which sometimes uses a simplified print dialog that hides advanced driver features.

## Fix steps
1. Open the Windows Start menu, type Printers & scanners, and press Enter.
2. Click on the affected HP LaserJet printer and select Manage, then click Printer properties.
3. Navigate to the Device Settings tab at the top.
4. Scroll down to the Installable Options section.
5. Find the setting for Duplex Unit (for 2-Sided Printing) and change the dropdown from Not Installed to Installed.
6. Click Apply and then OK.
7. Instruct the user to completely close their document, reopen it, and attempt to print double-sided again.

## Escalate if
- The "Device Settings" tab is completely missing from the printer properties (indicating a generic Windows driver is installed instead of the HP specific driver).
- The Duplex Unit is set to Installed, but the printer still refuses to print double-sided.
- The option reverts to "Not Installed" every time the computer reboots due to a corrupted print server group policy.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Printer Model: (e.g., HP LaserJet Pro M404dn)
- Application: (The app the user is trying to print from, e.g., Adobe Acrobat)