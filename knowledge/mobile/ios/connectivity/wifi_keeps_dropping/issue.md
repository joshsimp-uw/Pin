---
doc_id: KB-U1V2W3X4-wifi_dropping
title: "Connectivity — iOS — Wi-Fi Keeps Dropping"
service: Mobile Connectivity
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- ios
- wifi
- network
- cellular
- disconnect
- wireless
urls: []
---

# Wi-Fi Keeps Dropping

# iOS (Wireless Configuration)

Use this guide to resolve issues where an iPhone continuously disconnects from the corporate office Wi-Fi, switches to cellular data unexpectedly, or repeatedly prompts for a password the user has already entered.

### Wi-Fi Keeps Dropping

## Severity:
`S3` — Minor degradation; user can usually rely on cellular data as a backup, but may face slow speeds or data caps.

## Symptoms
- The iPhone randomly drops the Wi-Fi icon and displays 5G or LTE while the user is sitting at their office desk.
- The user is prompted with an "Incorrect Password" popup for the corporate network, even though they have not changed their credentials.
- The phone connects to the network but says "No Internet Connection" underneath the Wi-Fi name.

## Quick checks
- Ensure Airplane mode is not accidentally toggled on in the Control Center.
- Confirm if the user recently updated their Active Directory password on their laptop, as the phone is likely still trying to use the old cached password.

## Fix steps
1. Open the Settings app and tap Wi-Fi.
2. Tap the blue "i" icon next to the problematic corporate network.
3. Tap Forget This Network and confirm.
4. Go back to the main Settings menu and tap Cellular.
5. Scroll all the way to the very bottom of the Cellular page (past the list of apps).
6. Look for Wi-Fi Assist and toggle it Off. (This feature forces the phone to drop Wi-Fi if it thinks the cellular signal is faster, which often causes drops in large office buildings).
7. Go back to the Wi-Fi menu, tap the corporate network, and enter the latest login credentials.

## Escalate if
- The Wi-Fi toggle in Settings is greyed out and cannot be turned on (indicating hardware failure).
- The user enters the correct password, but the phone continues to reject it immediately (could indicate an expired security certificate or an Intune policy block).
- Every iOS user in a specific section of the office is experiencing the same dropping behavior simultaneously (indicating a physical wireless access point issue).

## Ticket fields to capture (when escalating)
- iOS Version: (e.g., iOS 17.4)
- Network Name (SSID): (e.g., Corp-Secure-5G)
- Physical Location: (Which office floor or room the drops occur in)
- Recent Password Change: (Yes/No)