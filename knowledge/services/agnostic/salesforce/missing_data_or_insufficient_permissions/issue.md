---
doc_id: KB-8D8E1A02E9-missing_da
title: "Business Application \u2014 Salesforce (Remote Users) \u2014 Missing data\
  \ or insufficient permissions"
service: Salesforce
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- salesforce
- crm
- business_app
- missing_data_or_insufficient_permissions
dns:
- salesforce.acme.com
urls:
- https://salesforce.acme.com
- https://login.salesforce.com
---

# Missing data or insufficient permissions

# Salesforce

## Access
- Primary: **https://salesforce.acme.com**
- Fallback: https://login.salesforce.com

### Missing data or insufficient permissions

**Severity:** `S2` — Major degradation; user work significantly impacted. Escalate within same business day.

**Symptoms**
- You can't see records you expect
- Buttons/features missing
- Permission denied messages

**Quick checks**
- Confirm you're in the correct Salesforce app/workspace
- Check filters and views

**Fix steps**
1. Verify the record isn't filtered out (views/filters).
2. If you still cannot access, request permission changes via IT/CRM admin.

**Escalate if**
- You need access for business-critical workflow and cannot proceed
- Multiple users affected

**Ticket fields to capture (when escalating)**
- **What access is needed:** Object/record type
- **Example record:** ID or name if known


## Escalation logic (for chatbot / help desk)
- Business-critical login failure/outage → **S2** (or **S1** if suspected compromise)
- Performance issue with workaround → **S3**
- Permissions blocking core work → **S2**
