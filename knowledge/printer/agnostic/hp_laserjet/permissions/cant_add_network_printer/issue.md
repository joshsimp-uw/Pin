---
doc_id: KB-P2Q3R4S5-network_printer_access
title: "Permissions — Printers — Cannot Add Network Printer"
service: Printer Permissions
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
- network
- add
- share
- access
- denied
- active-directory
urls: []
---

# Cannot Add Network Printer

# Printers (Network & Permissions)

Use this guide to troubleshoot issues where a user is attempting to map a shared corporate HP LaserJet from the print server, but is blocked by security restrictions or directory errors.

### Cannot Add Network Printer

## Severity:
`S3` — Minor degradation; user cannot access a specific shared department printer and must print to an alternate device.

## Symptoms
- The user tries to add a printer via the Windows directory but receives an "Access Denied" or "0x0000011b" error code.
- The specific HP LaserJet does not appear when searching the Active Directory list.
- Windows prompts the user for an Administrator username and password when trying to install the shared print driver.

## Quick checks
- Verify the user is connected to the corporate internal network or an active VPN tunnel.
- Confirm the exact name of the print server and the shared printer queue (e.g., \\corp-print-01\Marketing-HP-M404).

## Fix steps
1. Open the Windows Start menu, type Printers & scanners, and press Enter.
2. Click Add device or Add a printer or scanner.
3. If the printer does not automatically populate, click Add manually next to "The printer that I want isn't listed".
4. Select Select a shared printer by name and type the exact network path provided by the department head. Click Next.
5. If an "Access Denied" message appears, it means the user's Active Directory account is not a member of the security group allowed to use this printer.
6. Instruct the user to submit an access request ticket through the IT portal to be added to the appropriate printer security group.
7. Once IT confirms the group membership is updated, have the user log out of Windows and log back in to refresh their access token, then try adding the printer again.

## Escalate if
- The user is confirmed to be in the correct Active Directory security group but still receives an "Access Denied" error.
- The printer maps successfully, but every test page sent to it immediately disappears from the queue without printing.
- A recent Windows Update is blocking the installation of shared network drivers across the domain.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Print Server Path: (e.g., \\Server\ShareName)
- Exact Error Code: (e.g., Error 0x00000005)
- Verified AD Group: (Yes/No)