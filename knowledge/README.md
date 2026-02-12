---
doc_id: KB-8EC9A00BFD
title: KB Ingest Package (ACME Remote Users)
service: Knowledge Base Ingestion
audience:
  - End Users
  - Tier 0/1 Help Desk
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
  - kb_ingest
  - acme
  - remote
  - rag_ready
---

# kb_ingest — ACME Remote User Knowledge Base

This folder is designed for **RAG ingestion** and **end-user self-service**. Content is intentionally limited to facts and steps required to get users working.

## Severity tags
- **S1:** Service down / security risk / user fully blocked → escalate immediately
- **S2:** Major degradation / significant work impact → escalate same business day
- **S3:** Minor issue / how-to / workaround exists → resolve via KB or standard queue

## DNS and URLs policy
- End users are given **DNS names and HTTPS URLs only** (no IP addresses).
- Root domain: **acme.com**
- For ACME-hosted services that require a DNS name, use: `{service}.acme.com` (example: `vpn.acme.com`).

## Remote work note
ACME IT does **not** troubleshoot home ISP/Wi‑Fi. These KBs include only checks users can do on their device.

## Directory map
- `iam/` — identity, password, MFA, sign-in
- `email/` — Outlook & webmail
- `endpoint_devices/` — Dell Windows devices
- `remote_access/` — Cisco Secure Client / AnyConnect VPN
- `endpoint_security/` — Microsoft Endpoint Protection
- `file_storage/` — OneDrive & SharePoint
- `business_applications/` — Salesforce
- `printers/` — HP LaserJet USB printers
- `mobile_devices/` — Android & iPhone
- `_reference/` — shared reference facts (DNS endpoints, severity guide)
