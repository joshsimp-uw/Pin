---
doc_id: KB-Z2A3I4V5-meeting_instability
title: "Connectivity — Zoom — Meeting Audio Video Instability"
service: Unified Communications
audience:
- End Users
- Helpdesk
owner: Collaboration Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- zoom
- connectivity
- instability
- lag
- freezing
- network
- unstable
- audio-drop
urls: []
---

# Meeting Audio Video Instability

# Zoom (Network Performance)

Use this guide to troubleshoot issues where a user receives Your internet connection is unstable warnings, or experiences frozen video and robotic audio during active meetings.

### Meeting Audio Video Instability

## Severity:
`S3` — Minor degradation; the user can stay in the meeting, but the quality of communication is significantly compromised.

## Symptoms
- A yellow or red banner appears at the top of the Zoom window warning of an unstable connection.
- Other participants report that the user’s video is frozen or their audio is cutting in and out.
- The user experiences a significant delay (latency) between what is said and when they hear it.

## Quick checks
- Ask the user to check their signal strength if they are on Wi-Fi. A single bar of signal is insufficient for high-definition video conferencing.
- Check if the user is running other high-bandwidth applications in the background, such as file backups, 4K streaming, or large downloads.

## Fix steps
1. Instruct the user to move closer to their Wi-Fi router or, ideally, connect via a wired Ethernet cable.
2. If the connection remains unstable, have the user stop their outgoing video feed by clicking Stop Video. This reduces the bandwidth requirement significantly.
3. In the Zoom desktop client, click the Gear icon > Video and uncheck the box for HD. This forces Zoom to use standard definition, which is more resilient to network fluctuations.
4. Click the Statistics tab in the Zoom settings during a meeting. Look at the Network tab. If Packet Loss is consistently above 2 percent, the local network is the primary cause.
5. Advise the user to disconnect from their corporate VPN if it is not required for the meeting, as some VPNs add unnecessary latency and packet overhead to real-time traffic.
6. Restart the home router and the computer to clear any local network cache or stuck processes.

## Escalate if
- The user has high-speed fiber internet and is on a wired connection, but the instability persists across all meetings.
- The instability only occurs when the user is in the corporate office, suggesting a saturated local access point or a firewall bottleneck.
- Multiple users in the same department or region report the same instability simultaneously.

## Ticket fields to capture (when escalating)
- Network Type: (e.g., Home Wi-Fi, Office Wired, Starlink)
- Bandwidth Speed: (Download and Upload Mbps)
- Packet Loss Percentage: (From the Zoom Statistics window)