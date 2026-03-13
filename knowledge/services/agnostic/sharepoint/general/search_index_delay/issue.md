---
doc_id: KB-S1I2D3L4-search_delay
title: "General — SharePoint — Search Index Delay"
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
- search
- index
- missing-results
- crawl
- find
urls: []
---

# Search Index Delay

# SharePoint (Search Functionality)

Use this guide to resolve issues where a user recently uploaded or renamed a file, but the SharePoint search bar fails to find it, even when the user types the exact file name.

### Search Index Delay

## Severity:
`S3` — Minor degradation; the user can still navigate to the file manually, but the search productivity tool is temporarily inaccurate.

## Symptoms
- The user searches for "Budget_2026" which was uploaded 10 minutes ago, but receives "No results found."
- Search results show the old name of a file that was renamed earlier that day.
- Results are consistent for old files but highly inconsistent for newly created content.

## Quick checks
- Verify the user actually has permissions to view the file. SharePoint search only shows results the user is authorized to see ("security trimming").
- Confirm the user is searching at the correct level (e.g., searching the specific site vs. searching the entire organization).

## Fix steps
1. Explain to the user that SharePoint search is not instantaneous. The "Search Crawler" must visit the site and index new content, which can take anywhere from 15 minutes to several hours.
2. Instruct the user to wait at least 1 hour and try again.
3. (Site Owner Action): To force a re-index of a library, go to Library settings > More library settings.
4. Click Advanced settings.
5. Scroll down to the Reindex Document Library button and click it. (Note: This puts the library in a queue to be crawled; it is not an immediate fix).
6. Click OK to confirm the re-index request.
7. Encourage the user to use the "Filters" pane in the library as a workaround until the index catches up.

## Escalate if
- Content uploaded more than 24 hours ago is still not appearing in search results for any user.
- The search bar returns a "Something went wrong" error instead of results.
- The search results are showing content that the user should NOT have permission to see.

## Ticket fields to capture (when escalating)
- Site URL: (The full web link)
- Affected File Name: (e.g., Salary_Review.pdf)
- Time Since Upload: (e.g., 6 hours ago)