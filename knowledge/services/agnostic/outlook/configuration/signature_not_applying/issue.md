---
doc_id: KB-E5F6G7H8-signature_error
title: "Configuration — Outlook — Signature Not Applying"
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
- signature
- missing
- formatting
- html
- default
urls: []
---

# Signature Not Applying

# Outlook (Mail Formatting)

Use this guide to assist users whose corporate email signature is not automatically appearing on new messages, or looks visually broken after copying and pasting it from a template.

### Signature Not Applying

## Severity:
`S4` — Proactive request; the user can still email normally, but lacks standardized corporate branding.

## Symptoms
- The user clicks New Email, but the body of the message is completely blank.
- The user created a signature, but has to manually click the Signature button to insert it every single time.
- A newly pasted HTML signature (containing company logos and formatted text) looks scrambled, excessively large, or turns into plain text.

## Quick checks
- Ensure the user is actually drafting an HTML email. If the format is set to Plain Text, all images and formatting in the signature will be stripped out automatically.
- Check if your organization utilizes a third-party centralized signature management tool (like Exclaimer or CodeTwo) that automatically injects signatures at the server level after the email is sent.

## Fix steps
1. Open Outlook and click File, then Options.
2. Select Mail from the left navigation pane, then click the Signatures... button.
3. In the top right corner under Choose default signature, verify that the correct email account is selected in the dropdown.
4. Set the New messages dropdown to the desired signature name.
5. Set the Replies/forwards dropdown to the desired signature name (often a shorter version without logos).
6. Click OK twice to save.
7. If the user's HTML signature looks broken, delete the entire contents of the Edit signature box.
8. Open the corporate signature template in a web browser (not Microsoft Word). Highlight the template, right-click, and select Copy.
9. Go back to the Outlook signature box, right-click, and select the Keep Source Formatting paste option. Click OK.

## Escalate if
- The Signatures button in the Outlook Options menu is completely frozen and does nothing when clicked (this is a known Windows registry bug requiring a repair of the Office installation).
- The user's signatures randomly delete themselves every time they close and reopen Outlook (often related to the "Store my Outlook settings in the cloud" roaming signatures feature conflicting with local files).

## Ticket fields to capture (when escalating)
- Outlook Version: (e.g., Microsoft 365 Apps for Enterprise)
- Issue Type: (Not applying automatically vs. Visually broken)
- Roaming Signatures Enabled: (Yes/No)