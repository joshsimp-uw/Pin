---
doc_id: KB-N4O5P6Q7-printer_offline
title: "Connectivity — Printers — Printer Shows Offline"
service: Printer Connectivity
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
- offline
- network
- ip
- snmp
urls: []
---

# Printer Shows Offline

# Printers (Network Connection)

Use this guide to troubleshoot scenarios where a network-attached HP LaserJet is powered on and awake, but Windows claims the device is "Offline" and refuses to send print jobs.

### Printer Shows Offline

## Severity:
`S3` — Minor degradation; user cannot print to their primary device, halting paper-based workflows.

## Symptoms
- The printer icon is greyed out in the Windows "Printers & scanners" menu with a status of "Offline".
- Print jobs stack up in the queue and do not process.
- The physical printer screen is on, awake, and shows no error messages.

## Quick checks
- Walk over to the physical printer and press the "Information" or "Network" button on the screen to view its current IPv4 address.
- Open Command Prompt on the user's PC and type `ping [printer IP address]`. If it replies, the network connection is fine, and it is a Windows configuration issue.

## Fix steps
1. Open the Windows Start menu, type Printers & scanners, and press Enter.
2. Click the affected HP LaserJet, select Manage, then click Printer properties.
3. Navigate to the Ports tab at the top.
4. Expand the Port column to see the IP address Windows is currently trying to use.
5. If the IP address does not match what the physical printer screen showed, click Add Port, select Standard TCP/IP Port, click New Port, and type the correct new IP address.
6. If the IP address does match, select the port and click Configure Port.
7. Uncheck the box for SNMP Status Enabled at the bottom. (HP printers often fail to reply to SNMP polls correctly, which tricks Windows into thinking the printer is offline). Click OK.

## Escalate if
- The printer's IP address cannot be pinged at all, indicating a dead ethernet port, a bad network cable, or a disconnected Wi-Fi profile.
- The printer's IP address changes every single day (requires an escalation to Network Engineering to assign a DHCP reservation or static IP).
- Unchecking SNMP and updating the IP does not force the printer back online after a computer reboot.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Printer Model: (e.g., HP LaserJet Pro MFP M428fdw)
- Current Printer IP: (Found on the physical printer screen)
- Old Windows IP: (Found in the Ports tab)