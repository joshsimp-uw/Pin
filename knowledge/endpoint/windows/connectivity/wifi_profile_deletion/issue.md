---
doc_id: KB-G7H8I9J0K1-wifi_forget
title: "Connectivity — Endpoints — Forget Wi-Fi Network"
service: Endpoint Connectivity
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- wifi
- wireless
- network
- profile
- password
urls: []
---

# Forget Wi-Fi Network

# Endpoints (Wireless Configuration)

Use this guide to clear cached wireless credentials. This is usually necessary after a user changes their corporate password, causing the saved Wi-Fi profile to repeatedly fail authentication.

### Wi-Fi Profile Deletion

## Severity:
`S3` — Minor degradation; user cannot connect to wireless, but can often use a wired connection as a workaround.

## Symptoms
- Windows repeatedly prompts for the Wi-Fi password, even when entered correctly.
- A "Can't connect to this network" error appears immediately after clicking connect.
- The device connects to the Wi-Fi but shows "No Internet" while other devices work fine.

## Quick checks
- Ensure the laptop's physical Wi-Fi switch (if applicable) is turned on and Airplane mode is disabled.
- Confirm the user recently changed their Active Directory/SSO password.

## Fix steps
1. Click the Start menu and open Settings (the gear icon).
2. Click on Network & internet, then select Wi-Fi.
3. Click on Manage known networks.
4. Scroll through the list to find the problematic network (e.g., the corporate office Wi-Fi).
5. Click the Forget button next to that network name.
6. Click the Wi-Fi icon in the system tray, select the network again, click Connect, and enter the latest login credentials.

## Escalate if
- The Wi-Fi toggle is entirely missing from Settings and the system tray (indicating a missing or failed network adapter).
- The "Forget" button is greyed out or the network profile immediately reappears due to an Intune/MDM policy conflict.
- The user enters the correct new credentials but is continually locked out of their Active Directory account.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Network Name (SSID): (e.g., Corp-Secure-5G)
- Location: (Which office or branch the user is in)
- Recent Password Change: (Yes/No)