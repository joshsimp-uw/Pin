---
doc_id: KB-C1V2P3N4-cert_failure
title: "General — Cisco VPN — Certificate Validation Failure"
service: Network Access
audience:
- End Users
- Helpdesk
owner: Network Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- cisco
- anyconnect
- vpn
- certificate
- validation
- trust
- security
urls: []
---

# Certificate Validation Failure

# Cisco AnyConnect (Security Certificates)

Use this guide to troubleshoot the Security Warning that appears when the AnyConnect client cannot verify the identity of the VPN gateway, usually due to an expired server certificate or a missing local root CA.

### Certificate Validation Failure

## Severity:
`S3` — Minor degradation; the user can often bypass the warning (if allowed by policy), but the connection is technically insecure until resolved.

## Symptoms
- A popup window titled Security Warning: Untrusted VPN Server! appears immediately after clicking Connect.
- The message states "The certificate is not issued by a trusted certificate authority" or "The certificate has expired."
- The Connect anyway button is either greyed out or results in a secondary connection failure.

## Quick checks
- Verify the user has not manually changed the Gateway address to a non-production or test URL.
- Check the date and time on the user's computer; if the local clock is in the past or future, the certificate will appear invalid.

## Fix steps
1. Ensure the Windows/macOS system clock is synchronized with internet time.
2. If the clock is correct, the issue likely resides with the corporate Root Certificate.
3. Instruct the user to connect to the corporate network via Ethernet (if in-office) to allow Group Policy to push the updated certificate bundle.
4. If working remotely, a helpdesk agent must manually install the corporate Root CA into the "Trusted Root Certification Authorities" store via the Certificates MMC snap-in.
5. Restart the Cisco Secure Client and attempt the connection again.

## Escalate if
- The warning is occurring for all users globally (indicating the server-side SSL certificate on the Cisco ASA has expired).
- The user is blocked by a "Strict Certificate Check" policy that prevents any connection to untrusted gateways.
- The certificate details show the name of a different company, suggesting a DNS hijacking or man-in-the-middle scenario.

## Ticket fields to capture (when escalating)
- Certificate Subject: (e.g., vpn.company.com)
- Expiration Date: (Found in the certificate details)
- Root CA: (Who issued the certificate?)