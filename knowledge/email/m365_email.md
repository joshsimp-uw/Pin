---
doc_id: KB-6379EC8570
title: Email — Microsoft 365 (Outlook) for Remote Users
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
urls:
  - https://outlook.office.com
  - https://portal.office.com
---

# Microsoft 365 Email (Outlook)

## Access
- Outlook on the web: https://outlook.office.com
- Outlook desktop (if installed)

## Common issues

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

### Not receiving email

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Expected messages never arrive
- Only some senders affected

**Quick checks**
- Check Junk Email folder
- Check Focused/Other tabs
- Search for the sender or subject

**Fix steps**
1. Check Junk Email and move any legitimate messages to Inbox.
2. Search your mailbox for the sender or subject keywords.
3. Ask the sender to confirm the address is correct.

**Escalate if**
- Multiple external senders report bounces
- Mailbox appears full and you can’t delete items

**Ticket fields to capture (when escalating)**
- **Sender address:** Who is sending
- **Approx time:** When you expected the email

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
