# VPN Troubleshooting (Tier 1)

## Scope
This procedure covers basic VPN connectivity and sign-in issues for supported company devices.

## Symptoms
- VPN fails to connect
- Repeated MFA prompts
- Error codes such as 809, 412, "authentication failed"

## Quick checks
1. Confirm the user can browse the internet without VPN.
2. Confirm date/time is correct (auto-sync recommended).
3. Confirm the user is on a stable network (avoid captive portals / hotel Wi-Fi sign-in pages).

## Procedure
1. **Collect details**
   - OS/version, device type, network type (home Wi-Fi/hotspot/on-site)
   - Exact error message or code
   - Whether MFA works for other sign-ins
2. **Restart network stack**
   - Windows: toggle Wi-Fi off/on, then reboot if quick toggle fails
   - macOS: disconnect/reconnect Wi-Fi; consider reboot if persistent
3. **Check captive portal**
   - Open a browser and visit a plain HTTP site to trigger sign-in (if applicable)
4. **Retry VPN**
   - Attempt connection once after steps above

## Escalation criteria
Escalate to Tier 2 if any of the following occur:
- The error persists after the procedure above
- The user reports widespread impact (multiple users)
- The device appears unmanaged or non-standard
- The issue indicates account lockout or suspicious sign-in activity

## What to include in the ticket
- OS and device type
- Network type
- Exact error message/code
- Steps attempted
