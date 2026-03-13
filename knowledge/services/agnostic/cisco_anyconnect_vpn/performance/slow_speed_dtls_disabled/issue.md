---
doc_id: KB-S1S2D3T4-slow_speed_dtls
title: "Performance — Cisco VPN — Slow Speed DTLS Disabled"
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
- performance
- slow
- dtls
- tls
- lag
- video
urls: []
---

# Slow Speed DTLS Disabled

# Cisco AnyConnect (Tunnel Protocol Optimization)

Use this guide to resolve performance issues where the VPN connection is slow or "choppy," often caused by the client failing to establish a DTLS (UDP) tunnel and falling back to a slower TLS (TCP) tunnel.

### Slow Speed DTLS Disabled

## Severity:
`S3` — Minor degradation; the connection works for basic web browsing but is unsuitable for high-bandwidth tasks like video conferencing or large file transfers.

## Symptoms
- The user complains that Teams or Zoom calls are robotic or laggy while on VPN.
- Opening a file from a network share takes significantly longer than usual.
- The user's speed test results on VPN are less than 10 percent of their non-VPN speed.

## Quick checks
- Open the Cisco AnyConnect window and click the Graph icon (Statistics).
- Look for the "Protocol" field. If it says "TLS" instead of "DTLS," the connection is using a slower, less efficient protocol.
- Ask the user if they are on a restrictive network (like a public library or a high-security guest Wi-Fi) that might be blocking UDP traffic.


## Fix steps
1. Disconnect the VPN.
2. Check the user's local firewall software (like Norton or McAfee) to ensure it is not blocking outgoing UDP traffic on port 443.
3. If the user is at home, suggest a quick reboot of their home router to clear the NAT table.
4. Re-connect the VPN. Check the Statistics window again.
5. If it still says TLS, instruct the user to try a different network (like a mobile hotspot) to confirm if the local ISP or router is the bottleneck.
6. Explain to the user that "TCP-over-TCP" (which happens during TLS fallback) creates a performance penalty known as "TCP Meltdown" which causes the perceived slowness.

## Escalate if
- The user is on a high-speed wired connection and the client still refuses to use DTLS.
- The head-end firewall logs show "DTLS handshake failed" for a large group of users.
- The user's throughput is extremely low even when DTLS is active.

## Ticket fields to capture (when escalating)
- Protocol Shown: (TLS or DTLS)
- Speed Test (Non-VPN): (e.g., 300 Mbps)
- Speed Test (VPN): (e.g., 15 Mbps)