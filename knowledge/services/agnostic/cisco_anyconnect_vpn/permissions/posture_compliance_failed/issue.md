---
doc_id: KB-P1O2S3T4-posture_failed
title: "Permissions — Cisco VPN — Posture Compliance Failed"
service: Network Access
audience:
- End Users
- Helpdesk
owner: Security Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- cisco
- anyconnect
- vpn
- posture
- compliance
- security-scan
- ise
- antivirus
urls: []
---

# Posture Compliance Failed

# Cisco AnyConnect (Security Compliance)

Use this guide to troubleshoot scenarios where the VPN client successfully authenticates the user but denies the connection because the computer fails the mandatory security health check (posture scan).

### Posture Compliance Failed

## Severity:
`S2` — High impact; the user is denied access to the corporate network because their device is deemed a security risk.

## Symptoms
- After entering credentials, a "Cisco AnyConnect Posture Module" window appears and runs a scan.
- The scan ends with a red message: "System scan was unable to find all required software" or "Your device does not meet the security requirements."
- The VPN disconnects immediately after the scan fails.

## Quick checks
- Ensure the user's antivirus software is currently enabled and the virus definitions are up to date.
- Verify if there are pending Windows Updates that require a system restart.

## Fix steps
1. Open the antivirus or endpoint security software installed on the machine (e.g., Microsoft Defender or CrowdStrike).
2. Verify that Real-time protection is turned on.
3. Check for updates within the antivirus app and install any available definition files.
4. Open Windows Settings > Windows Update and click Check for updates. If updates were recently installed, restart the computer.
5. Ensure the "Cisco Secure Desktop" or "ISE Posture" service is running in the Windows Services menu (services.msc).
6. Attempt to reconnect the VPN. The posture module will re-scan the device.

## Escalate if
- The device is fully updated and the antivirus is active, but the posture scan continues to fail.
- The error message specifically mentions a "missing patch" that the user cannot install due to a lack of administrative rights.
- The posture module fails to initialize or hangs at 0 percent during the scan.

## Ticket fields to capture (when escalating)
- Antivirus Version: (e.g., Windows Defender v4.18)
- Compliance Error: (Exact text shown in the Posture window)
- Last Windows Update: (Date of last successful update)