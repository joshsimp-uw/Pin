---
doc_id: KB-L1R2P3I4-ip_restricted_login
title: "Permissions — Salesforce — IP Restricted Login"
service: CRM Operations
audience:
- Helpdesk
- Security Team
owner: Identity Engineering
last_reviewed: 2026-03-10
version: 1.0
security: internal_only
tags:
- salesforce
- login
- ip-restriction
- security
- vpn
- blocked
- whitelist
urls: []
---

# IP Restricted Login

# Salesforce (Network Security)

Use this guide to resolve login failures where a user is blocked from Salesforce because they are attempting to connect from an IP address that has not been whitelisted in the corporate security policy.

### IP Restricted Login

## Severity:
`S2` — High impact; the user is completely unable to log into the CRM, usually while working remotely or from a new office branch.

## Symptoms
- The user enters their correct username and password, but the screen says "Please check your username and password. If you still can't log in, contact your Salesforce administrator."
- The administrator checks the user's "Login History" related list and sees a Status of "Restricted IP".
- The user is working from home, a hotel, or a client site and is not connected to the corporate VPN.

## Quick checks
- Ask the user to visit a site like "whatsmyip.com" and provide their current IPv4 address.
- Verify if the user is supposed to be able to work from outside the corporate network according to HR policy.

## Fix steps
1. Instruct the user to connect to the corporate VPN. This will route their traffic through a whitelisted corporate IP, allowing the login to proceed.
2. If the user is at a permanent new office location, a System Admin must add the new IP range to the system.
3. Navigate to Setup > Network Access.
4. Click New and enter the Start IP Address and End IP Address provided by the network team. 
5. Alternatively, if the restriction is only for a specific team, navigate to Setup > Profiles > [Target Profile] > IP Ranges and add the range there.
6. Once the range is added, the user should clear their browser cache and attempt the login again.

## Escalate if
- The user's IP is already in the whitelisted range in "Network Access" but they are still being blocked with the "Restricted IP" status.
- The organization uses a "Login Flow" that performs additional security checks and is failing.
- The user is on the VPN but their public IP is showing as a different, non-whitelisted address.

## Ticket fields to capture (when escalating)
- User's Public IP: (e.g., 192.168.1.50)
- Login History Status: (Confirm it says "Restricted IP")
- VPN Connection Status: (Connected/Disconnected)