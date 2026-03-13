---
doc_id: KB-Z6A7B8C9-faded_print
title: "Performance — Printers — Faded Print Quality"
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
- faded
- light
- toner
- economode
urls: []
---

# Faded Print Quality

# Printers (Print Quality)

Use this guide to resolve issues where the text and images printed by the HP LaserJet are incredibly light, washed out, or only printing on one half of the page.

### Faded Print Quality

## Severity:
`S3` — Minor degradation; documents are legible but difficult to read, prompting user frustration.

## Symptoms
- The entire page is uniformly light grey instead of crisp black.
- The left or right margin of the page is completely blank or faded, while the rest of the page is dark.
- The printer screen displays a "Toner Low" or "Very Low" warning.

## Quick checks
- Check the physical printer screen for the current Supply Levels to see the estimated toner percentage remaining.
- Ask the user if they recently shook the printer or moved it to a new desk, which can cause toner powder to shift to one side.

## Fix steps
1. Open the front door of the LaserJet and carefully pull out the toner cartridge.
2. Hold the cartridge by both ends and gently rock it side-to-side five or six times to redistribute the toner powder inside the hopper.
3. Reinsert the cartridge and print a test page.
4. If the page is still uniformly light, the user may have accidentally enabled draft mode. Open the Windows Start menu, type Printers & scanners, and open the menu.
5. Click the HP LaserJet, select Manage, then click Printing preferences.
6. Navigate to the Paper/Quality tab and ensure EconoMode is unchecked.
7. If EconoMode was already off and shaking the cartridge only temporarily fixed the issue, the toner is completely depleted and must be replaced.

## Escalate if
- A brand new, official HP toner cartridge produces the exact same faded results.
- The fade occurs in distinct horizontal bands across the page, which points to an electrical transfer roller failure.

## Ticket fields to capture (when escalating)
- Printer Model: (e.g., HP LaserJet Enterprise M507)
- Toner Level: (Current percentage shown on the printer)
- EconoMode Status: (Was it checked? Yes/No)