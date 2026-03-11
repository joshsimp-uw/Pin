---
doc_id: KB-J0K1L2M3N4-high_cpu_memory
title: "Performance — Endpoints — High CPU & Memory Usage"
service: Endpoint Performance
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- cpu
- ram
- memory
- performance
- slow
- crash
- hardware
- fans
urls: []
---

# High CPU & Memory Usage

# Endpoints (Hardware Performance)

Use this guide to troubleshoot performance degradation related to processor (CPU) throttling or Random Access Memory (RAM) exhaustion on corporate endpoints.

### High CPU & Memory Usage

## Severity:
`S3` — Minor degradation; user work impacted but functional. Escalate within 2 business days. (Note: Elevate to `S2` if the device is completely frozen and unusable).

## Symptoms
- Computer is running abnormally slow, lagging, or the mouse cursor is stuttering.
- The laptop fans are spinning at maximum speed constantly, making excessive noise.
- Applications are freezing, crashing, or becoming unresponsive.
- System displays explicit "Out of Memory" or "Your computer is low on memory" error notifications.

## Quick checks
- Confirm how many heavy applications (e.g., Adobe Creative Cloud, Docker, large Excel spreadsheets) are currently running.
- Check if an excessive number of web browser tabs are open (especially Chrome or Edge).
- Verify if a background Windows Update or antivirus scan is currently running.

## Fix steps
1. Save all current work to prevent data loss.
2. Open the Task Manager by pressing Ctrl + Shift + Esc.
3. Click on the CPU column header to sort processes by processor usage, then do the same for the Memory column to identify resource hogs.
4. Right-click any unnecessary applications or browser tabs that are consuming high amounts of CPU/RAM and select End task.
5. If the system is still sluggish, restart the computer to clear the memory cache, release locked resources, and reset runaway background services.

## Escalate if
- Performance issues and "Out of Memory" errors persist immediately after a restart.
- The system resource monitor shows 90%+ RAM or CPU usage even when no user applications are open.
- The `MsMpEng.exe` (Windows Defender) process is permanently stuck at high CPU usage and cannot be resolved.
- The computer fails to boot, blue screens (BSOD), or emits memory error beep codes.

## Ticket fields to capture (when escalating)
- OS Version: (e.g., Windows 11 Enterprise)
- Device Model: (e.g., Dell Latitude 7420)
- Total Installed RAM / CPU Model: (e.g., 16GB / Intel i7)
- Top Consuming App: (The name of the process using the most resources before restart)