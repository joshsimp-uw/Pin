---
doc_id: KB-I9J0K1L2-wrong_inbox_view
title: "Configuration — Outlook — Wrong Inbox View"
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
- view
- focused-inbox
- reading-pane
- layout
- missing-emails
urls: []
---

# Wrong Inbox View

# Outlook (Interface Customization)

Use this guide to resolve issues where the user's Outlook layout has dramatically changed, hiding emails, moving the reading pane, or altering the sort order, usually due to an accidental click or a software update.

### Wrong Inbox View

## Severity:
`S3` — Minor degradation; no data is lost, but the user is highly confused and struggling to locate their daily emails.

## Symptoms
- The user complains they are missing emails, but they are actually hidden behind the "Other" tab at the top of the inbox.
- The reading pane (where the email body is displayed) has moved from the right side of the screen to the bottom, or disappeared entirely.
- The inbox is grouping emails by conversation (threaded view) instead of a simple chronological list, confusing the user.

## Quick checks
- Look at the top of the user's email list. If it says "Focused" and "Other", the Focused Inbox feature is enabled.
- Check the bottom left corner of Outlook to ensure the user is actually in the Mail view (envelope icon) and didn't accidentally click into the Tasks or Calendar view.

## Fix steps
1. To fix the missing emails issue: Click the View tab at the very top of the Outlook ribbon.
2. Click the Show Focused Inbox button to toggle it off. This merges all mail back into a single chronological "All" list.
3. To fix the reading pane: On the same View tab, locate the Layout group and click Reading Pane.
4. Select Right, Bottom, or Off depending on the user's preference (Right is the standard default).
5. To fix conversation grouping: On the View tab, check or uncheck the box for Show as Conversations.
6. If the inbox is completely scrambled beyond recognition (missing columns, weird sorting), simply click the View tab, click View Settings, and click the Reset Current View button.

## Escalate if
- The Reset Current View button is greyed out.
- The user resets the view, but it reverts back to the broken layout every time they restart their computer (indicating a corrupted customized view profile).
- The user is missing folders entirely from the left-hand navigation pane, which may indicate accidental deletion or a collapsed archive rather than a simple view setting.

## Ticket fields to capture (when escalating)
- Outlook Version: (e.g., Microsoft 365 Apps for Enterprise)
- Specific View Issue: (e.g., Reading pane stuck, columns missing)
- Reset View Attempted: (Did Reset Current View fix it temporarily? Yes/No)