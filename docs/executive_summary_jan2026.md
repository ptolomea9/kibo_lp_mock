# Kibo Commerce Google Ads Account Review
## Executive Summary | January 2026

---

## Overview

This document summarizes the optimization work completed on Kibo Commerce's Google Ads account (994-869-7111), focusing on the Search - NonBrand campaign and a comprehensive conversion tracking audit.

---

## Changes Made (Summary)

| Optimization Type | Count |
|-------------------|-------|
| New RSA ads written | 20 |
| Ad group sitelinks created | 30 |
| Keywords mapped to landing pages | 49 |
| Negative keywords added | 11 |
| Audience segments layered | 31 |
| Conversion actions audited | 102 |

---

## 1. Search Campaign Optimizations

### 1.1 Keyword-Level URL Mapping

**What we did:** Implemented granular landing page assignments at the keyword level to improve relevance and Quality Score.

**Example:**
| Keyword | Previous URL | New URL |
|---------|--------------|---------|
| order management software | /platform/ | /platform/order-management/ |
| ecommerce platform | /platform/ | /platform/commerce/ |
| inventory management system | /platform/ | /platform/inventory-visibility/ |

**Impact:** Better alignment between search intent and landing page content improves Quality Score, Ad Rank, and conversion rates.

---

### 1.2 New RSA Ad Copy

**What we did:** Created new Responsive Search Ads with improved headline and description combinations, including Dynamic Keyword Insertion (DKI) where appropriate.

**DKI Example:**
```
Headline: {KeyWord:Enterprise Commerce Platform}
```
This dynamically inserts the user's search term (properly capitalized) into the ad, falling back to "Enterprise Commerce Platform" if the term is too long.

**Ad Structure:**
- 15 headlines (mix of brand, benefit, feature, and CTA variations)
- 4 descriptions (value props, differentiators, social proof)
- Pinned headlines for brand consistency in positions 1-2

---

### 1.3 Ad Group Sitelinks

**What we did:** Created ad group-level sitelinks to provide more relevant deep links based on ad group theme.

**Example - OMS Ad Group:**
| Sitelink | URL |
|----------|-----|
| Real-Time Inventory | /platform/inventory-visibility/ |
| Order Orchestration | /platform/inventory-promising/ |
| Reverse Logistics | /platform/reverse-logistics/ |
| Customer Stories | /customer-stories/ |

**Why ad group level:** More specific than campaign-level sitelinks, allowing OMS searches to see OMS-related links rather than generic platform links.

---

### 1.4 Audience Layering

**What we did:** Added observation audiences to the Search - NonBrand campaign for bid optimization signals.

**Audiences Added:**
- In-Market: Business Software, Enterprise Software
- Custom Segments: OMS Competitor Keywords, OMS Competitor URLs
- Remarketing: Website Visitors (if available)

**Note:** Set as "Observation" not "Targeting" - ads still show to all searchers, but we can adjust bids for high-value audiences.

---

### 1.5 Search Term Analysis & Negatives

**What we did:** Analyzed search term reports to identify:
- Irrelevant queries to negate
- Traffic routing issues (queries going to wrong ad groups)
- New keyword opportunities

**Sample Negatives Added:**
- "free" (low intent)
- "jobs" / "careers" (wrong intent)
- Competitor names (should go to separate campaign if targeted)

---

## 2. Conversion Tracking Audit

### 2.1 Audit Summary

We audited all **102 conversion actions** in the account:

| Category | Count | Status |
|----------|-------|--------|
| Healthy (working) | 8 | Keep |
| Legacy UA Goals | 34 | Remove |
| Broken (0 conversions) | 31 | Investigate/Remove |
| Unused (Hidden/Removed) | 29 | Clean up |

**Critical Finding:** Only 8% of conversion actions are actively tracking data.

---

### 2.2 Working Conversions (Keep These)

| Conversion Action | Type | 90-Day Conv | Value | Primary |
|-------------------|------|-------------|-------|---------|
| Request a Demo - Directive | Webpage Pixel | 5 | $500 | Yes |
| HubSpot - Lead | Offline Upload | 6 | $6 | Yes |
| HubSpot - MQL | Offline Upload | 1 | $10 | Yes |
| All but Demo Conversions | Webpage Pixel | 5 | $125 | No |
| Kibo - GA4 request_a_demo | GA4 Event | ~1 | $1 | No |
| Lead Forms 12-4-25 | Webpage Pixel | 9 | $0 | No |

---

### 2.3 Legacy UA Goals (Remove)

**34 Universal Analytics goals** remain in the account. UA sunset on July 1, 2023 - these will never fire again.

Examples:
- Demo Request Formfill (All Web Site Data)
- Contact Us Formfill (All Web Site Data)
- Form Submit Conversions (All Web Site Data)

**Action Required:** Remove all 34 UA-based conversion actions.

---

### 2.4 Salesforce Integration (Broken)

**13 Salesforce conversion actions** show 0 conversions in 180 days.

**Diagnosis:** No Salesforce connector is linked to this Google Ads account. The integration was either never completed or was disconnected.

**Recommendation:** Remove all Salesforce conversion actions. HubSpot is the active CRM integration.

---

### 2.5 HubSpot Integration (Partially Working)

**Native Integration (Working):**
- HubSpot - Lead: 6 conversions in 90 days ✓
- HubSpot - MQL: 1 conversion in 90 days ✓

**Google Sheets Integration (Not Working):**
- HubSpot Lead - Manual: 0 conversions
- Imports 4 rows daily from Google Sheet, but GCLIDs don't match any clicks
- Likely test data from setup, never connected to live HubSpot data

---

## 3. Live Tag Testing Results

**Site:** kibocommerce.com

| Tag | Status | ID |
|-----|--------|-----|
| Google Tag Manager | ✓ Active | GTM-PD73CHF |
| Google Analytics 4 | ✓ Active | G-21CTWG5W2Y |
| Google Ads Pixel | ✓ Firing | AW-877723722 |
| HubSpot | ✓ Active | 40870578 |
| Facebook Pixel | ✓ Active | 2386873278224987 |

**Conversion Pixel Verification:**
- Visited /thank-you-for-your-request/
- Google Ads conversion pixel fires correctly
- GA4 events fire: `request_a_demo`, `thank_you_for_your_request`, `Speak_to_Expert`

**Conclusion:** Tags are implemented correctly. Issues are in Google Ads conversion action configuration, not website tracking.

---

## 4. Outstanding Questions

### 4.1 HubSpot Lead - Manual Investigation

**Status:** Pending access to Google Sheet

**Question:** The "KIBO HubSpot OFFLINE CONVERSIONS" Google Sheet imports 4 rows daily but none match to Google Ads clicks. Is this:
- Test data from setup that was never replaced?
- Missing automation from HubSpot to sheet?
- Invalid GCLIDs?

**Action Required:**
1. Get access to the Google Sheet
2. Verify if real conversion data is flowing from HubSpot
3. Either fix the pipeline or disconnect and remove

**Interim Fix:** Set "Include in Conversions" to No for this action (must be done in UI).

---

### 4.2 Conversion Value Strategy

**Current State:**
- HubSpot - Lead: $1 (too low)
- HubSpot - MQL: $10 (reasonable)
- Request a Demo - Directive: $100 (good)

**Question:** What are the actual lead values for Smart Bidding optimization?

**Suggested Values:**
| Stage | Suggested Value |
|-------|-----------------|
| Lead | $50-100 |
| MQL | $150-200 |
| SQL | $300-500 |
| Opportunity | $500-1000 |
| Closed Won | Actual deal value |

---

### 4.3 Full Funnel Tracking

**Current:** Only tracking Lead and MQL stages from HubSpot.

**Question:** Should we add downstream funnel stages?
- SQL (Sales Qualified Lead)
- Opportunity Created
- Closed Won

This would enable Value-Based Bidding optimization toward revenue, not just leads.

---

### 4.4 Lookback Window

**Updated:** HubSpot conversion lookback windows have been extended from 30 days to 90 days.

| Conversion Action | Previous | New |
|-------------------|----------|-----|
| HubSpot - Lead | 30 days | 90 days |
| HubSpot - MQL | 30 days | 90 days |

**Why this matters:** B2B sales cycles typically exceed 30 days. With the previous 30-day lookback, conversions from clicks older than 30 days weren't being attributed to Google Ads campaigns. The 90-day window ensures proper attribution for longer sales cycles.

---

## 5. Recommended Action Items

### Immediate (This Week)
- [ ] Set "HubSpot Lead - Manual" to exclude from conversions (UI)
- [ ] Get access to KIBO HubSpot OFFLINE CONVERSIONS sheet
- [ ] Remove 34 UA goal conversion actions

### Short-Term (Next 2 Weeks)
- [ ] Remove 13 Salesforce conversion actions
- [x] ~~Extend HubSpot lookback windows to 90 days~~ **DONE** (Jan 2026)
- [ ] Update conversion values to reflect true lead worth
- [ ] Clean up 29 unused (HIDDEN/REMOVED) conversion actions

### Medium-Term (Next Month)
- [ ] Add SQL/Opportunity/Closed Won conversion tracking
- [ ] Implement Enhanced Conversions for better matching
- [ ] Consider Value-Based Bidding once funnel data flows

---

## 6. Files & Scripts Created

| File | Purpose |
|------|---------|
| `audit_conversions.py` | Reusable script to audit all conversion actions |
| `conversion_audit_report.csv` | Full data on all 102 conversion actions |
| `conversion_cleanup_recommendations.md` | Detailed cleanup recommendations |
| `tag_test_results.md` | Live tag testing documentation |
| `diagnose_salesforce.py` | Salesforce integration diagnostic |
| `diagnose_hubspot.py` | HubSpot integration diagnostic |
| `update_lookback_windows.py` | Extended HubSpot lookback to 90 days |
| `disable_hubspot_manual.py` | Attempted fix (requires UI - see notes) |

---

## Appendix: Conversion Action Cleanup Checklist

### Remove (34 UA Goals)
All conversion actions with type "UNIVERSAL_ANALYTICS_GOAL" - see `conversion_audit_report.csv` for full list.

### Remove (13 Salesforce)
- SF: New Lead
- SF: MQL
- SF: SQL
- SF: SAL
- SF: Opportunity
- SF: Opportunity Created
- SF: Closed Won
- SF: Closed Lost
- SF: Lead Rejected
- Lead Converted (salesforce)
- Working Lead (Salesforce)
- Working Opportunity (salesforce)
- Won Opportunity (salesforce)

### Investigate (1 HubSpot)
- HubSpot Lead - Manual (pending sheet access)

### Keep (8 Working)
- Request a Demo - Directive
- HubSpot - Lead
- HubSpot - MQL
- All but Demo Conversions
- Kibo - GA4 (web) request_a_demo
- Kibo - GA4 (web) thank_you_for_your_request
- Lead Forms 12-4-25
- Free Trial Submission
