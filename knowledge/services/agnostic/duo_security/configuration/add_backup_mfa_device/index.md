---
doc_id: KB-A1B2C3D4-backup_mfa
title: "Configuration — Duo Security — Add Backup MFA Device"
service: Identity and Access Management
audience:
- End Users
- Helpdesk
owner: Identity Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- duo
- mfa
- backup
- device
- token
- yubikey
- portal
urls: []
---

# Add Backup MFA Device

# Duo Security (Device Management)

Use this guide to assist users who want to register a secondary authentication method, such as a backup smartphone, a tablet, or a physical hardware token (like a YubiKey), to prevent lockouts if their primary phone is lost or broken.

### Add Backup MFA Device

## Severity:
`S4` — Proactive request; user is currently able to log in but wants to establish a backup method.

## Symptoms
- The user is logged into a portal but cannot find the settings to add a new phone.
- The user wants to register a YubiKey but does not have the "My Settings & Devices" option visible.

## Quick checks
- Verify the user still has access to their primary Duo device (they must authenticate with an existing device to add a new one).
- Ensure the organization's Duo policy allows end-users to manage their own devices via the self-service portal.

## Fix steps
1. Instruct the user to navigate to a corporate application that triggers the traditional Duo prompt (e.g., a webmail login or a VPN portal).
2. Stop at the Duo authentication screen. Do not approve the push yet.
3. Click the link on the left side of the prompt that says Add a new device or My Settings & Devices.
4. The user will be prompted to authenticate using their current primary device to verify their identity.
5. Once authenticated, the device management portal will load. Select Add another device.
6. Choose the type of device being added (Mobile phone, Tablet, or Security Key).
7. Follow the on-screen prompts to scan the QR code with the new tablet/phone, or insert and tap the security key.
8. Scroll down to "Default Device" and ensure the user's preferred primary device is selected, then click Save.


## Escalate if
- The "My Settings & Devices" link is completely hidden or disabled on the Duo prompt (indicating a global policy restriction).
- The user attempts to register a security key, but the browser throws an immediate WebAuthn failure error.
- The user has already lost their primary device and cannot access the self-service portal to add the backup.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Browser Used: (e.g., Google Chrome)
- Backup Device Type: (e.g., YubiKey 5 NFC)