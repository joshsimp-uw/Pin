---
doc_id: KB-D4E5F6G7H8-dns_flush
title: "Connectivity — Endpoints — DNS Cache Flush"
service: Endpoint Connectivity
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- dns
- internet
- browser
- connection
- intranet
urls: []
---

# DNS Cache Flush

# Endpoints (Network Configuration)

Use this guide to resolve issues where specific internal or external websites fail to load, display outdated content, or return "Server IP address could not be found" errors while the rest of the internet works fine.

### DNS Flush

## Severity:
`S3` — Minor degradation; user is blocked from specific web resources but has general connectivity.

## Symptoms
- Corporate intranet portals refuse to load.
- Browser displays "DNS_PROBE_FINISHED_NXDOMAIN" errors.
- A recently migrated website is loading the old version of the page.

## Quick checks
- Verify the device is connected to the internet by testing a common public site.
- Check if other users in the same office or on the same VPN are experiencing the same issue (which would indicate a broader server issue, not an endpoint issue).

## Fix steps
1. Click the Start menu, type cmd, right-click Command Prompt, and select Run as administrator.
2. If prompted by User Account Control, click Yes.
3. In the command prompt window, type `ipconfig /flushdns` and press Enter.
4. Wait for the message: "Successfully flushed the DNS Resolver Cache."
5. Close the command prompt.
6. Close all instances of the web browser, reopen it, and attempt to access the site again.

## Escalate if
- The issue persists after a flush and a full system reboot.
- The command prompt returns an error stating the DNS Client service is not running.
- Multiple users report the exact same URL failing simultaneously.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 10 Pro)
- Failing URL: (The exact web address the user is trying to reach)
- Network Location: (e.g., In-office via Wi-Fi, or Remote via VPN)
- Error Message: (The exact error code shown in the browser)