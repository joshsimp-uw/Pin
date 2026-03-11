---
doc_id: KB-V2W3X4Y5-black_streaks
title: "General — Printers — Black Streaks on Page"
service: Printer Hardware
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
- streaks
- lines
- toner
- drum
- quality
urls: []
---

# Black Streaks on Page

# Printers (Print Quality)

Use this guide to troubleshoot physical print quality issues where the HP LaserJet is outputting pages with vertical black lines, repeating ghost images, or loose toner powder.

### Black Streaks on Page

## Severity:
`S3` — Minor degradation; the printer functions, but documents are unprofessional and unusable for external clients or presentations.

## Symptoms
- Printed pages have a distinct, solid black vertical line running from top to bottom.
- Previous lines of text repeat faintly further down the page (ghosting).
- The paper feels gritty, and the black marks can be smudged or wiped off with a finger.

## Quick checks
- Print a Configuration Page from the printer's physical control panel to verify if the streaks occur on internal test pages (this rules out a bad driver or corrupted PDF).
- Open the toner door and look for obvious piles of spilled black powder inside the chassis.

## Fix steps
1. Use the printer's built-in cleaning cycle. On the physical screen, navigate to Settings > General > Print Quality > Calibration/Cleaning, and select Print Cleaning Page. 
2. The printer will slowly pull a page through the fuser to melt off residual toner. Repeat this process up to three times.
3. If streaks persist, open the front door and pull out the toner cartridge.
4. Examine the green or blue cylindrical roller (the imaging drum) on the cartridge. If there is a visible scratch or a solid ring of toner stuck to it, the drum is ruined.
5. Replace the combined toner/drum cartridge with a new OEM HP unit.

## Escalate if
- A brand new toner cartridge does not resolve the vertical lines.
- The streaks only appear when making copies or scanning from the top document feeder, but not when printing from a computer (this indicates a dirty scanner glass slit, not a printer hardware issue).
- The printer makes a loud grinding noise while printing the streaked pages.

## Ticket fields to capture (when escalating)
- Printer Model: (e.g., HP LaserJet Pro M404dn)
- Defect Type: (e.g., Vertical streak vs. Repeating ghost image)
- Cartridge Status: (Was a new toner tested? Yes/No)