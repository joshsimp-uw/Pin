---
doc_id: KB-6379EC8570-phishing_o
title: "Email \u2014 Microsoft 365 (Outlook) for Remote Users \u2014 Phishing or suspicious\
  \ email"
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
- phishing_or_suspicious_email
urls:
- https://outlook.office.com
- https://portal.office.com
---

# Phishing or suspicious email

# Microsoft 365 Email (Outlook)

## Access
- Outlook on the web: https://outlook.office.com
- Outlook desktop (if installed)

### Phishing or suspicious email

**Severity:** `S1` — Service down or security risk; user blocked and/or potential compromise. Immediate escalation.

**Symptoms**
- Message asks for password/payment
- Unexpected attachments
- Urgent threats or strange links

**Quick checks**
- Do not click links or open attachments
- Do not reply with personal information

**Fix steps**
1. If you clicked a link or entered your password, change your password immediately (if possible).
2. Report the email to IT (include sender, subject, and time received).
3. Delete the email after reporting.

**Escalate if**
- You clicked a link or entered credentials
- You opened an attachment and something unexpected happened

**Ticket fields to capture (when escalating)**
- **Did you click?:** Yes/No
- **Did you enter credentials?:** Yes/No
- **Sender/subject:** Copy/paste


## Escalation logic (for chatbot / help desk)
- Suspected phishing or credential entry → **S1**
- Mail send/receive broken across web + desktop → **S2**
- Single device/app issue with workaround (web works) → **S3**
