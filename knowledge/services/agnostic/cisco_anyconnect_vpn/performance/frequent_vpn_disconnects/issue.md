---
doc_id: KB-F1D2V3P4-frequent_disconnects
title: "Performance — Cisco VPN — Frequent VPN Disconnects"
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
- disconnect
- drop
- stability
- timeout
- dpd
urls: []
---

# Frequent VPN Disconnects

# Cisco AnyConnect (Connection Stability)

Use this guide to troubleshoot scenarios where the VPN tunnel successfully establishes but drops and reconnects repeatedly every few minutes, disrupting the user's workflow.

### Frequent VPN Disconnects

## Severity:
`S3` — Minor degradation; the user is technically able to connect, but the intermittent drops prevent stable use of corporate applications and meetings.

## Symptoms
- The AnyConnect icon in the system tray frequently changes to the "reconnecting" circular arrows.
- The user receives a notification: "The VPN connection was terminated due to a loss of communication with the secure gateway."
- Active Teams calls or remote desktop sessions freeze and then recover after 30 to 60 seconds.

## Quick checks
- Ask the user if they are using a Wi-Fi connection with a weak signal. A single dropped packet on an unstable connection can trigger a VPN timeout.
- Check if the user is moving between different Wi-Fi access points (roaming) within their home or office.

## Fix steps
1. Instruct the user to switch to a wired Ethernet connection if possible to rule out Wi-Fi interference.
2. If Wi-Fi is the only option, have the user move closer to their router to improve signal strength.
3. Open the Cisco AnyConnect / Secure Client window. Click the gear icon > Preferences.
4. Ensure the box for Minimize on connection is the only one checked unless specific others were requested.
5. (Advanced) If the user has access to their home router settings, suggest disabling "SIP ALG" or "Stateful Packet Inspection" (SPI) which can sometimes misidentify VPN traffic as a flood attack.
6. Restart the computer to clear any stuck network driver states.

## Escalate if
- The disconnects occur at exactly the same interval every time (e.g., every 30 minutes), suggesting a re-keying or session timeout policy on the firewall.
- DART logs show "Dead Peer Detection" (DPD) failure messages consistently.
- Multiple users in the same geographic region are experiencing drops simultaneously.

## Ticket fields to capture (when escalating)
- Frequency of Drops: (e.g., every 5 minutes)
- Network Type: (e.g., Starlink, Comcast, Fiber)
- DART Log Attached: (Yes/No)