---
doc_id: KB-S5B6L7F8-sbl_disabled
title: "Configuration — Cisco VPN — SBL Feature Disabled"
service: Network Access
audience:
- Helpdesk
- Desktop Support
owner: Network Engineering
last_reviewed: 2026-03-10
version: 1.0
security: internal_only
tags:
- cisco
- anyconnect
- vpn
- sbl
- login
- windows
- password-reset
urls: []
---

# SBL Feature Disabled

# Cisco AnyConnect (Start Before Login)

Use this guide to troubleshoot issues where the "Start Before Login" (SBL) module is missing, preventing users from establishing a VPN tunnel at the Windows login screen. This is critical for users who need to sync a newly reset password with their local machine.

### SBL Feature Disabled

## Severity:
`S2` — High impact; users working remotely with expired or reset passwords are "locked out" of their laptops because they cannot reach the Domain Controller to verify the new credentials.

## Symptoms
- The small VPN icon is missing from the bottom right corner of the Windows Ctrl+Alt+Del login screen.
- The user resets their password via a web portal but cannot log into their laptop because it is "offline" and doesn't know the new password.
- Desktop support is unable to push group policy updates to remote machines that aren't logged in.

## Quick checks
- Verify if the SBL module was selected during the initial installation of the Cisco Secure Client.
- Check the local machine path `C:\Program Data\Cisco\Cisco AnyConnect Secure Client\Start Before Login` to see if the required .xml and .dll files exist.


## Fix steps
1. (Helpdesk) If the user is currently logged in but SBL is missing, a re-installation of the client is required.
2. Run the Cisco Secure Client installer.
3. Ensure the Start Before Login or SBL module is explicitly checked in the customization list.
4. Complete the installation and restart the computer.
5. If the module is installed but not appearing, a System Admin must update the VPN Profile on the Cisco ASA/Firewall.
6. In the VPN Profile XML, ensure the `<UseStartBeforeLogin>` tag is set to `true`.
7. Once the user connects to the VPN once successfully, the new XML profile will download, and SBL will be available on the next reboot.

## Escalate if
- SBL is installed and enabled in the profile, but still does not appear on the Windows login screen (suggesting a conflict with a third-party credential provider like Windows Hello or Duo for Windows).
- Clicking the SBL icon crashes the Windows login interface (lsass.exe error).

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Client Version: (e.g., 5.1.2.x)
- XML Profile Name: (The profile being used by the user)