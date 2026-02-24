---
doc_id: KB-982E4A9480
title: Endpoint Security — Microsoft Endpoint Protection
service: Microsoft Endpoint Protection
audience:
  - End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
  - security
  - defender
  - endpoint_protection
---

# Microsoft Endpoint Protection

Protection runs automatically on ACME devices. Do not disable security features.

## Common issues

### Security alert or threat detected

**Severity:** `S1` — Service down or security risk; user blocked and/or potential compromise. Immediate escalation.

**Symptoms**
- Pop-up indicates malware/threat found
- Files quarantined
- Browser warns of unsafe download

**Quick checks**
- Disconnect from VPN (if connected) unless IT instructs otherwise
- Do not continue downloading/opening the file

**Fix steps**
1. Do not open or run the flagged file.
2. Take a screenshot of the alert.
3. Contact IT immediately with the alert details.

**Escalate if**
- Any confirmed malware message
- Repeated alerts after restart

**Ticket fields to capture (when escalating)**
- **Alert name:** As shown
- **Did you run/open anything?:** Yes/No

### Real-time protection is off

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- Windows Security shows protection turned off
- Warnings persist after reboot

**Quick checks**
- Restart device
- Install Windows updates

**Fix steps**
1. Restart your device.
2. Install pending Windows updates and restart again.
3. If protection remains off, contact IT.

**Escalate if**
- Protection cannot be re-enabled
- You see messages about 'managed by your organization' and it still shows off

**Ticket fields to capture (when escalating)**
- **Screenshot:** Windows Security page

### Blocked website or download

**Severity:** `S3` — Minor issue or how-to; workaround exists. Resolve via KB or standard ticket queue.

**Symptoms**
- Website blocked
- Download prevented
- Message says content is unsafe

**Quick checks**
- Confirm the site is required for work
- Try a different official source if available

**Fix steps**
1. If the site/download is work-related, capture the URL and the block message.
2. Submit a request to IT for review.

**Escalate if**
- You believe your account/device is compromised
- You cannot perform your job due to required site block

**Ticket fields to capture (when escalating)**
- **Blocked URL:** Copy/paste
- **Business justification:** What task requires it


## Escalation logic (for chatbot / help desk)
- Malware/threat detected → **S1**
- Protection disabled and cannot be enabled → **S2**
- Benign blocks with a workaround → **S3**
