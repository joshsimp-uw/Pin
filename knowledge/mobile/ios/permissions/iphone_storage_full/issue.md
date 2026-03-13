---
doc_id: KB-P1Q2R3S4-storage_full
title: "Performance — iOS — iPhone Storage Full"
service: Mobile Performance
audience:
- End Users
- Helpdesk
owner: Client Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- ios
- storage
- space
- full
- offload
- capacity
urls: []
---

# iPhone Storage Full

# iOS (Storage Management)

Use this guide to troubleshoot devices that have run out of local storage capacity, which often prevents users from taking photos, receiving emails, or downloading necessary work files.

### iPhone Storage Full

## Severity:
`S3` — Minor degradation; device functions are severely limited, and applications may randomly crash on launch due to zero cache space.

## Symptoms
- A persistent "iPhone Storage Full" popup appears on the screen.
- Applications crash immediately upon opening.
- The user cannot take photos or download PDF attachments from emails.

## Quick checks
- Open Settings > General > iPhone Storage and look at the color-coded graph at the top to see what category is consuming the most space (Apps, Photos, Media, or System Data).

## Fix steps
1. In the iPhone Storage menu, look at the Recommendations list provided by Apple right below the graph.
2. Tap Enable next to Offload Unused Apps. This deletes the application files for rarely used apps but keeps the user's data and documents intact.
3. Review Large Attachments in the Messages app via the recommendations list to bulk-delete old videos or photos sent via text.
4. Scroll down the app list to find specific heavy hitters (often Spotify, Podcasts, or Netflix) and instruct the user to delete downloaded offline media within those apps.
5. Open the Photos app, tap Albums, scroll to the bottom, tap Recently Deleted, and empty the folder (iOS normally keeps deleted photos for 30 days).

## Escalate if
- The grey "System Data" or "Other" category at the bottom of the storage list is consuming a massive amount of space (e.g., 40GB+) and does not clear out after a device restart.
- The storage shows as 100% full, but the math of the installed apps and photos doesn't add up to the total device capacity (indicating file system corruption).
- The device is a corporate-owned 64GB model and the required enterprise apps take up all available space, requiring a hardware upgrade request.

## Ticket fields to capture (when escalating)
- iOS Version: (e.g., iOS 17.4)
- Total Capacity: (e.g., 64GB)
- Top Consuming Category: (e.g., Photos, System Data, Apps)
- Hardware Upgrade Request: (Yes/No)