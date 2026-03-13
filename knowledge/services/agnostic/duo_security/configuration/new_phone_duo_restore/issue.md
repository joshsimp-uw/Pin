---
doc_id: KB-E5F6G7H8-duo_restore
title: "Configuration — Duo Security — New Phone Duo Restore"
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
- phone
- upgrade
- restore
- reactivate
- mobile
urls: []
---

# New Phone Duo Restore

# Duo Security (Device Migration)

Use this guide to assist users who have purchased a new smartphone and transferred their old phone number, but are no longer receiving Duo Push notifications because the physical hardware changed.

### New Phone Duo Restore

## Severity:
`S3` — Minor degradation; user is blocked from logging in via Push, but can often use SMS passcodes as a temporary workaround.

## Symptoms
- The user triggers a login, the screen says "Pushed a login request to your device", but the new phone receives nothing.
- Opening the Duo Mobile app on the new phone shows the corporate account, but it says "Reconnect" or is greyed out.
- The user recently visited an Apple Store or carrier store to upgrade their hardware.

## Quick checks
- Ask the user if they still have the old phone in their possession and connected to Wi-Fi (if yes, they can just use the old phone to authenticate into the device management portal).
- Confirm the new phone has the exact same phone number as the old one.

## Fix steps
1. Instruct the user to navigate to a corporate application that triggers the Duo prompt on their computer.
2. Click the link for My Settings & Devices or Add a new device on the prompt.
3. Since they cannot receive a Push, click Enter a Passcode instead.
4. A blue banner will appear at the bottom. Click the Text me new codes button.
5. The user's new phone will receive an SMS text message containing a 6-digit code.
6. Type that code into the Duo prompt and click Log In to access the management portal.
7. Locate the user's phone number in the device list and click the gear icon (Device Options).
8. Click Reactivate Duo Mobile.
9. Open the Duo Mobile app on the new phone, tap Add Account, and scan the QR code displayed on the computer screen.

## Escalate if
- The organization has SMS passcodes disabled globally, meaning the user has no way to authenticate into the self-service portal.
- The user got a new phone and a completely new phone number simultaneously.
- Scanning the QR code results in an "Invalid Barcode" error.

## Ticket fields to capture (when escalating)
- Mobile OS: (e.g., iOS 17 or Android 14)
- Phone Number: (Last 4 digits only to verify match)
- SMS Capability: (Did the user receive the text code? Yes/No)
