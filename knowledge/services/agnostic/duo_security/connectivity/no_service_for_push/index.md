---
doc_id: KB-Q7R8S9T0-no_service_push
title: "Connectivity — Duo Security — No Cell Service for Push"
service: Identity and Access Management
audience:
- End Users
- Helpdesk
owner: Identity Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- duo
- push
- offline
- passcode
- airplane-mode
- service
urls: []
---

# No Cell Service for Push

# Duo Security (Offline Authentication)

Use this guide to assist users who are in an area with poor or no cellular reception (like an airplane, a basement server room, or an international location without roaming) and therefore cannot receive the standard Duo Push notification.

### No Service for Push

## Severity:
`S3` — Minor degradation; user assumes they are blocked, but an offline workaround exists within the app.

## Symptoms
- The user triggers a login on their laptop, but the Duo Push notification never arrives on their phone.
- The user's smartphone shows "No Service", "SOS Only", or is in Airplane Mode without Wi-Fi.
- The Duo prompt on the computer eventually times out and says "Authentication timed out".

## Quick checks
- Verify the phone actually has no internet connection.
- Ensure the user actually has the Duo Mobile app installed on their smartphone, rather than relying solely on SMS text messages or automated phone calls (which will absolutely fail without cell service).

## Fix steps
1. Tell the user to leave the Duo prompt open on their computer screen. Do not cancel the login.
2. If the computer automatically sent a Push, click Cancel in the blue bar at the bottom of the prompt.
3. Click the Enter a Passcode button on the computer screen.
4. Pick up the smartphone and manually open the Duo Mobile app. (The app does not need cellular service or Wi-Fi to open or function).
5. Tap on the corporate account listed inside the app (e.g., "Company Name - Duo").
6. A 6-digit numerical code will appear.
7. Type this 6-digit code into the box on the computer screen and click Log In.

## Escalate if
- The 6-digit offline code is repeatedly rejected as "Incorrect" (this usually means the phone's internal hardware clock has drifted and the app needs to be resynced).
- The user's phone is completely dead or lost, meaning they have no access to the offline codes.
- The Enter a Passcode button is missing from the computer's Duo prompt due to a strict organizational policy requiring push-only authentication.

## Ticket fields to capture (when escalating)
- Mobile OS: (e.g., iOS 17.4)
- Network Status: (e.g., Airplane mode, International travel)
- Error Message: (Was the offline code rejected, or was the button missing?)