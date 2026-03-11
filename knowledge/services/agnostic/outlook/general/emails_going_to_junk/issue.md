---
doc_id: KB-D2E3F4G5-emails_junk
title: "General — Outlook — Emails Going to Junk"
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
- junk
- spam
- whitelist
- block
- filter
- missing-emails
urls: []
---

# Emails Going to Junk

# Outlook (Spam Filtering)

Use this guide to assist users who are missing legitimate external emails because the Outlook Junk Email Filter is incorrectly flagging them as spam and moving them out of the Inbox.

### Emails Going to Junk

## Severity:
`S3` — Minor degradation; the user receives the mail, but it is hidden in a secondary folder, leading to missed deadlines or communication delays.

## Symptoms
- A client claims they sent an email, but the user cannot find it in their Inbox.
- The user checks their Junk Email folder and finds multiple legitimate business communications.
- The user repeatedly moves an email to the Inbox, but the next message from that same sender goes back to Junk.

## Quick checks
- Verify the user hasn't accidentally added the sender's domain to their "Blocked Senders" list.
- Check if the email contains suspicious links, large attachments, or "spammy" keywords that might trigger the server-side Microsoft Defender for Office 365 filter.

## Fix steps
1. Open Outlook and navigate to the Junk Email folder.
2. Right-click the legitimate email that was incorrectly filtered.
3. Select Junk from the context menu, then click Not Junk.
4. In the dialog box that appears, ensure the box for Always trust email from [sender@domain.com] is checked, then click OK.
5. The email will immediately move to the Inbox.
6. To proactively whitelist a sender: Click the Home tab at the top of the ribbon.
7. Click the Junk button in the Delete group and select Junk Email Options.
8. Go to the Safe Senders tab and click Add.
9. Type the email address or the entire domain (e.g., @client-company.com) and click OK, then Apply.


## Escalate if
- The email is being blocked at the gateway level and never even reaches the Junk Email folder (requires a security admin to check the Microsoft 365 Quarantine).
- The user whitelists the sender, but the emails continue to be routed to Junk (indicates a conflicting server-side transport rule).
- The user's entire Inbox is being flooded with actual spam that the filter is failing to catch.

## Ticket fields to capture (when escalating)
- Sender Address: (e.g., vendor@external.com)
- Recipient Address: (The user's email)
- Safe Senders Added: (Yes/No)