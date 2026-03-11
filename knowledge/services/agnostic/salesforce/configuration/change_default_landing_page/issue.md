---
doc_id: KB-S1A2L3F4-landing_page
title: "Configuration — Salesforce — Change Default Landing Page"
service: CRM Operations
audience:
- End Users
- Helpdesk
owner: Sales Operations
last_reviewed: 2026-03-10
version: 1.0
security: end_user_safe
tags:
- salesforce
- landing-page
- home
- dashboard
- tab
- navigation
- personalize
urls: []
---

# Change Default Landing Page

# Salesforce (User Personalization)

Use this guide to assist users who want to change the initial screen they see upon logging into Salesforce, such as defaulting to a specific Dashboard or the Leads tab instead of the standard Home page.

### Change Default Landing Page

## Severity:
`S4` — Proactive request; the system is functioning correctly, but the user wants to optimize their personal workflow.

## Symptoms
- The user complains that they have to click three times every morning just to see their sales metrics.
- The user is a specialized agent (e.g., Support) but the system keeps landing them on the Sales home page.

## Quick checks
- Verify which Salesforce App the user is currently using (e.g., Sales, Service, or a custom Lighting App), as landing pages are often tied to the App level.
- Confirm the user has the "Customize Application" or "Personalize Navigation" permission enabled in their profile.

## Fix steps
1. Instruct the user to log into Salesforce and look at the navigation bar at the top.
2. If they want a specific tab to be their "home," they can click and drag that tab to the far left position in the navigation bar.
3. To set a specific Dashboard as the landing page, click the Home tab. 
4. Look for the gear icon or the "Customize Page" button in the top right of the Home section.
5. Select the option to change the Dashboard component and pick the desired report.
6. For a more permanent change, click the user's Avatar in the top right and select Settings.
7. Navigate to Display & Layout > Customize My Tabs.
8. Ensure the desired starting tab is at the top of the Selected Tabs list. Click Save.

## Escalate if
- The user's navigation bar is locked by an administrator, preventing them from dragging or reordering tabs.
- The user wants a landing page that is completely different from the standard corporate layout (requires a Salesforce Admin to create a custom Lightning Home Page for that user's profile).

## Ticket fields to capture (when escalating)
- Salesforce Edition: (e.g., Enterprise or Unlimited)
- Current App: (e.g., Sales Lightning)
- Target Landing Tab: (e.g., Dashboards)