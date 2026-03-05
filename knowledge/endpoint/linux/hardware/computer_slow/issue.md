---
doc_id: KB-99B1029C4D-ram_usage
title: "Hardware — Endpoints — High Memory/RAM Usage"
service: Endpoint Hardware
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-04
version: 1.0
security: end_user_safe
tags:
- ram
- memory
- performance
- slow
- crash
- hardware
urls: []
---

# High Memory/RAM Usage

# Endpoints (Hardware Performance)

Use this guide to troubleshoot performance degradation related to Random Access Memory (RAM) exhaustion on corporate endpoints (Windows/macOS).

### High Memory/RAM Usage

## Severity:
`S3` — Minor degradation; user work impacted but functional. Escalate within 2 business days. (Note: Elevate to `S2` if the device is completely frozen and unusable).

## Symptoms
- Computer is running abnormally slow or lagging.
- Applications are freezing, crashing, or becoming unresponsive.
- System displays explicit "Out of Memory" or "Your computer is low on memory" error notifications.

## Quick checks
- Confirm how many heavy applications (e.g., Adobe Creative Cloud, Docker, large Excel spreadsheets) are currently running.
- Check if an excessive number of web browser tabs are open (especially Chrome or Edge).

## Fix steps
1. Save all current work to prevent data loss.
2. Open your system's resource monitor (Task Manager on Windows via `Ctrl + Shift + Esc`, or Activity Monitor on macOS via Spotlight).
3. Sort the processes by "Memory" to identify which applications are consuming the most RAM.
4. Close any unnecessary applications or browser tabs that are consuming high amounts of memory.
5. Restart your computer to clear the memory cache and release locked resources.

## Escalate if
- Performance issues and "Out of Memory" errors persist immediately after a restart.
- The system resource monitor shows 90%+ RAM usage even when no user applications are open (indicating a potential memory leak).
- The computer fails to boot and emits memory error beep codes.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Device Model: (e.g., Dell Latitude 7420)
- Total Installed RAM: (e.g., 16GB)
- Top Consuming App: (The name of the process using the most memory before restart)
