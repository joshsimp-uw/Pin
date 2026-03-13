---
doc_id: KB-U1V2W3X4-outlook_disconnected
title: "Connectivity — Outlook — Outlook Disconnected"
service: Messaging & Collaboration
audience:
- End Users
- Helpdesk
owner: Cloud Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- outlook
- disconnected
- offline
- network
- exchange
- outbox
urls: []
---

# Outlook Disconnected

# Outlook (Server Connection)

Use this guide to troubleshoot scenarios where the Outlook desktop client loses its connection to the Microsoft Exchange server, halting all incoming and outgoing mail.

### Outlook Disconnected

## Severity:
`S2` — High impact; the user cannot send or receive any communications via the desktop client, severely impacting productivity.

## Symptoms
- The status bar at the very bottom right of the Outlook window says "Disconnected", "Trying to connect...", or "Working Offline" with a red X over the icon.
- Emails sent by the user remain permanently stuck in the Outbox folder.
- No new emails have arrived in the inbox for several hours.

## Quick checks
- Open a web browser and verify the computer has a working internet connection.
- Instruct the user to log into Outlook on the Web (OWA) via portal.office.com. If they can access their mail there, it confirms their account is fine and the issue is purely the local desktop client.

## Fix steps
1. Click the Send / Receive tab at the top of the Outlook ribbon.
2. Look for the Work Offline button. If the button is highlighted in grey, click it once to toggle it off. The status bar should change to "Trying to connect..." and then "Connected".
3. If the button was not highlighted, completely close Outlook.
4. Open the Windows Start menu, type Credential Manager, and press Enter.
5. Click Windows Credentials.
6. Scroll down to the Generic Credentials section and locate any entries starting with "MicrosoftOffice16" or "msteams_adalsso".
7. Click the drop-down arrow next to those entries and select Remove. 
8. Restart the computer, open Outlook, and allow it to prompt the user for their password and MFA approval to rebuild the connection token.

## Escalate if
- Outlook still says "Disconnected" after clearing credentials and restarting the PC.
- The user is also unable to log into Outlook on the Web (indicating a locked Active Directory account or a global Microsoft 365 outage).
- Outlook repeatedly prompts for a password but never actually connects, even when the correct password is provided.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- OWA Test Result: (Did webmail work? Yes/No)
- Connection Status: (Exact wording from the bottom right corner)