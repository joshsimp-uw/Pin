---
doc_id: KB-C1D2E3F4-app_access_denied
title: "Permissions — Duo Security — App Access Denied"
service: Identity and Access Management
audience:
- End Users
- Helpdesk
owner: Identity Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- duo
- access
- denied
- permissions
- group
- vendor
- contractor
- policy
urls: []
---

# App Access Denied

# Duo Security (Application Permissions)

Use this guide to troubleshoot scenarios where a user successfully enters their primary password, but the Duo prompt blocks them from accessing a specific application because they lack the required security group memberships.

### App Access Denied

## Severity:
`S3` — Minor degradation; user is blocked from a specific application, halting their workflow for that system.

## Symptoms
- The user logs in with their correct username and password, but the Duo prompt displays a red banner stating "Access denied. You are not authorized to access this application."
- The user is a vendor, contractor, or recent internal transfer trying to access a restricted tool like a VPN portal or a financial system.
- The user can successfully use Duo to log into basic corporate apps (like webmail), but fails on this specific application.

## Quick checks
- Verify the user's employment status and job role to confirm they are actually supposed to have access to this restricted system.
- Check the Duo Admin Panel's Authentication Logs. If the result says "Denied by Policy", it confirms Duo is intentionally blocking them based on group rules.

## Fix steps
1. Open the corporate Active Directory, Azure AD, or Identity Management portal.
2. Search for the affected user's identity profile.
3. Identify the specific security group required to pass the Duo application policy (e.g., "VPN-Contractors" or "Finance-App-Users").
4. Add the user's account to the required security group.
5. Wait up to 15 to 30 minutes for the directory sync tool to push the new group membership to the Duo Security cloud environment.
6. Instruct the user to completely close their web browser or VPN client, reopen it, and attempt the login again.

## Escalate if
- The user is confirmed to be in the correct security group, the directory has successfully synced, but Duo still blocks the login.
- The red "Access denied" banner specifically mentions a "Device Health" or "Location" policy violation instead of a general authorization error.
- The required security group is strictly managed by a different department and requires the user to submit a formal access request ticket through an approval workflow.

## Ticket fields to capture (when escalating)
- Target Application: (e.g., Cisco AnyConnect VPN)
- User Type: (e.g., Contractor vs. Full-Time Employee)
- Missing Group: (The specific Active Directory group required)
- Exact Error Message: (The text shown inside the red Duo banner)