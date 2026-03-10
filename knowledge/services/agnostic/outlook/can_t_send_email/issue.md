---
doc_id: KB-6379EC8570-can_t_send
title: "Email \u2014 Microsoft 365 (Outlook) for Remote Users \u2014 Can't send email"
service: Microsoft 365 Email (Exchange Online)
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- email
- outlook
- m365
- exchange_online
- can_t_send_email
urls:
- https://outlook.office.com
- https://portal.office.com
---

# Can't send email

# Microsoft 365 Email (Outlook)

## Access
- Outlook on the web: https://outlook.office.com
- Outlook desktop (if installed)

### Can't send email

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Messages stay in Outbox
- Send fails with an error
- Recipients say they never received it

**Quick checks**
- Confirm you're online
- Try sending from Outlook on the web to isolate the issue

**Fix steps**
1. Restart Outlook.
2. Try sending the same message from https://outlook.office.com.
3. If sending works on the web but not desktop, sign out of Outlook desktop and sign back in.

**Escalate if**
- Sending fails on both web and desktop
- Error mentions account disabled or blocked

**Ticket fields to capture (when escalating)**
- **Where failing:** Outlook desktop / Web / Both
- **Error message:** Exact text or screenshot
