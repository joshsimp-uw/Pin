---
doc_id: KB-A1B2C3D4-out_of_office
title: "Configuration — Outlook — Out of Office Error"
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
- oof
- out-of-office
- automatic-replies
- error
- exchange
urls: []
---

# Out of Office Error

# Outlook (Automatic Replies)

Use this guide to troubleshoot issues where a user is trying to set their vacation auto-responder, but the feature is unavailable, greyed out, or throwing a server connection error.

### Out of Office Error

## Severity:
`S3` — Minor degradation; user can still send and receive mail, but cannot inform clients of their absence, potentially causing communication gaps.

## Symptoms
- The Automatic Replies (Out of Office) button in the File menu is missing entirely.
- Clicking the Automatic Replies button results in an error stating "Your automatic reply settings cannot be displayed because the server is currently unavailable."
- The user set the Out of Office message, but internal colleagues report they are not receiving the automatic response.

## Quick checks
- Verify the user is connected to the internet and Outlook says "Connected to: Microsoft Exchange" in the bottom right corner.
- Ask the user to log into Outlook on the Web (OWA) via portal.office.com. If they can set their Out of Office there successfully, the issue is isolated to their local desktop application.

## Fix steps
1. If the issue is isolated to the desktop client, instruct the user to close Outlook completely.
2. Press the Windows Key + R to open the Run dialog.
3. Type `outlook.exe /cleanrules` and press Enter. (Warning: This will delete client-side rules, but often fixes corrupted server-side OOF templates).
4. If the server error persists, open Outlook, click File, then Account Settings, and click Account Settings again.
5. Select the email account and click Change.
6. Ensure the Use Cached Exchange Mode box is checked. Sometimes toggling this off, restarting Outlook, toggling it back on, and restarting again forces a fresh sync with the Exchange server.
7. Instruct the user to try setting the Automatic Replies again.

## Escalate if
- The user cannot set their Out of Office even when using the web browser (OWA), indicating a mailbox corruption issue on the Exchange server.
- The user is trying to set an Out of Office message for a Shared Mailbox, which often requires specific administrative permissions or logging in via a separate OWA window.
- The Out of Office is sending to internal users but failing to send to external clients (this is usually a global Exchange Admin Center policy blocking external auto-forwards/replies).

## Ticket fields to capture (when escalating)
- Outlook Version: (e.g., Microsoft 365 Apps for Enterprise)
- OWA Test Result: (Did it work in the web browser? Yes/No)
- Target Audience: (Is it failing for Internal, External, or both?)