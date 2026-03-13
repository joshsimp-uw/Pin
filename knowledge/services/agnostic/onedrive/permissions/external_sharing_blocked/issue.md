---
doc_id: KB-J1K2L3M4-external_sharing
title: "Permissions — OneDrive — External Sharing Blocked"
service: Cloud Storage
audience:
- End Users
- Helpdesk
owner: Cloud Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- onedrive
- share
- external
- guest
- blocked
- policy
- access
urls: []
---

# External Sharing Blocked

# OneDrive (Security Policies)

Use this guide to assist users who are trying to send a file link to an external client, vendor, or contractor outside the organization, but the system actively blocks the action.

### External Sharing Blocked

## Severity:
`S3` — Minor degradation; external communication is delayed, requiring users to find approved alternative methods for file transfer.

## Symptoms
- The user types an external email address (like a @gmail.com or @clientdomain.com address) into the sharing box, and it immediately highlights red.
- An error message appears stating "Your organization's policies do not allow you to share with these users."
- The "Anyone with the link" option is completely greyed out and unclickable in the link settings menu.

## Quick checks
- Verify the recipient's email address is actually external to the company.
- Check if the user is attempting to share highly sensitive data (like financial reports or PII) that triggered an automated Data Loss Prevention (DLP) block.

## Fix steps
1. Explain to the user that the global corporate security policy restricts sharing internal OneDrive files directly with unverified external email addresses to prevent data leaks.
2. If the user is trying to collaborate with a long-term vendor, guide them on how to request a formal Azure AD Guest Account for the vendor through the IT portal.
3. If the user just needs to perform a one-time file transfer, direct them to the organization's officially approved secure file transfer protocol (SFTP) tool or secure email gateway.
4. If your organization utilizes specific SharePoint sites approved for external collaboration, instruct the user to move the file to that designated site and share it from there.

## Escalate if
- The external domain has already been whitelisted by IT, but the user is still being blocked from sharing to it.
- The user is getting this exact same error message when trying to share a file with an internal, full-time employee.

## Ticket fields to capture (when escalating)
- Sender Name: (The internal employee)
- Target External Domain: (e.g., @vendor-domain.com)
- File Sensitivity: (Does the file contain confidential info?)
