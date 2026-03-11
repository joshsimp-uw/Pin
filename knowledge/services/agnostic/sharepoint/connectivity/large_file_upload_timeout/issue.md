---
doc_id: KB-L1F2U3T4-upload_timeout
title: "Connectivity — SharePoint — Large File Upload Timeout"
service: Content Management
audience:
- End Users
- Helpdesk
owner: Cloud Engineering
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- sharepoint
- upload
- timeout
- large-file
- network
- size-limit
urls: []
---

# Large File Upload Timeout

# SharePoint (Network & Performance)

Use this guide to troubleshoot scenarios where a user is attempting to upload a very large file (e.g., a high-resolution video or a database export) and the progress bar stalls or returns a network error.

### Large File Upload Timeout

## Severity:
`S3` — Minor degradation; the user is unable to share specific large assets, though the rest of the site remains operational.

## Symptoms
- The upload progress stays at 99% for several minutes before displaying "The connection was reset" or "Upload failed."
- The browser window becomes unresponsive during the upload process.
- Small files (under 10MB) upload instantly, but files over 500MB fail consistently.

## Quick checks
- Verify the file size. SharePoint has a 250GB file size limit, but local network timeouts usually occur long before that.
- Check the user's upload speed via a speed test. A slow home Wi-Fi connection is the most common cause of timeouts.


## Fix steps
1. Instruct the user to use the Sync button in the SharePoint library to map the folder to their Windows File Explorer.
2. Once the folder appears in File Explorer, have the user drag and drop the large file into that local folder. 
3. The OneDrive sync engine will handle the upload in the background. Unlike the browser, the sync engine can resume if the connection is interrupted and is much more resilient to timeouts.
4. If the user must use the browser, ensure they are using a wired Ethernet connection rather than Wi-Fi.
5. Advise the user to avoid "bulk" uploading (uploading 1,000 files at once). Instead, zip the files into a single compressed archive before uploading.

## Escalate if
- The upload fails even when using a wired connection and the OneDrive sync client.
- The organization has a third-party firewall or proxy (like Zscaler) that is forcibly terminating long-running HTTP POST requests.
- The site has reached its total storage quota, preventing any new data from being added.

## Ticket fields to capture (when escalating)
- File Size: (e.g., 4.5 GB)
- Upload Method: (Browser Drag-and-drop vs. OneDrive Sync)
- Network Environment: (Home Wi-Fi, Office Wired, VPN)