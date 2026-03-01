---
doc_id: KB-72E6780D9F-sharing_li
title: "File Storage \u2014 OneDrive (Personal Files) \u2014 Sharing link not working"
service: OneDrive for Business
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- onedrive
- files
- sync
- m365
- sharing_link_not_working
urls:
- https://portal.office.com
---

# Sharing link not working

# OneDrive (Personal Files)

Use OneDrive for your personal work files. Access via https://portal.office.com → OneDrive.

### Sharing link not working

## Severity:
`S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

## Symptoms
- Recipient can't open link
- Permission denied

## Quick checks
- Confirm the recipient email is correct
- Try generating a new link

## Fix steps
1. Create a new share link and ensure it is set to the correct permission (View/Edit).
2. If sharing to an external recipient is required, follow company policy and request IT approval if needed.

## Escalate if
- Sharing is business-critical and blocked
- You need external sharing and it fails consistently

## Ticket fields to capture (when escalating)
- Recipient: Internal or external
- Permission needed: View/Edit


## Escalation logic (for chatbot / help desk)
- Sync broken with work impact → **S2**
- Single file restore / how-to → **S3**
- Suspected data loss across many files → **S1**
