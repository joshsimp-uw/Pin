---
doc_id: KB-5796127801-windows_wo
title: "Endpoint Devices \u2014 Dell Windows Laptops & Desktops (Remote Users) \u2014\
  \ Windows won't update / stuck updating"
service: Endpoint Devices (Dell / Windows)
audience:
- End Users
owner: Systems & Network Administrator
last_reviewed: 2026-02-11
version: 1.0
security: end_user_safe
tags:
- endpoint
- dell
- windows
- remote_work
- windows_won_t_update_stuck_updating
---

# Windows won't update / stuck updating

# Dell Windows Laptops & Desktops (Remote Users)

This article covers common remote-user issues for ACME-managed Windows devices.

### Windows won't update / stuck updating

## Severity:
`S2` — Major degradation; user work significantly impacted. Escalate within same business day.

## Symptoms
- Updates fail repeatedly
- Update stuck for hours
- Error code shown

## Quick checks
- Keep device plugged into power
- Confirm stable internet connection

## Fix steps
1. Restart the device once.
2. Try Windows Update again.
3. If it fails, capture the update error code and send it to IT.

## Escalate if
- Update failure repeats with the same error code
- Device cannot boot after updates

## Ticket fields to capture (when escalating)
- Error code: As shown in Windows Update
- Screenshot: If possible


## Escalation logic (for chatbot / help desk)
- Blue screen, boot failure, or data-loss risk → **S1**
- Core hardware (camera/mic) broken with no workaround → **S2**
- Performance issues with workaround → **S3**
