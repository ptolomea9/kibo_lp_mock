# Kibo Commerce Conversion Cleanup Recommendations

**Date:** January 25, 2026
**Account ID:** 994-869-7111
**Total Conversion Actions:** 102

---

## Executive Summary

Kibo Commerce's Google Ads account has **102 conversion actions**, but only **8 are actively tracking conversions**. This audit identified 94 conversion actions that should be removed, investigated, or consolidated.

### Quick Stats
| Category | Count | Action Required |
|----------|-------|-----------------|
| HEALTHY | 8 | None - Working correctly |
| LEGACY_UA | 34 | Remove immediately |
| BROKEN_PRIMARY | 1 | Critical - Investigate |
| BROKEN_SECONDARY | 30 | Investigate or remove |
| UNUSED | 29 | Clean up |

---

## Priority 1: Critical Issues (Immediate Action)

### 1.1 BROKEN_PRIMARY - Included in Bidding but Not Firing

**This is the highest priority issue.** One conversion action is included in the "Conversions" column (used for Smart Bidding) but has zero conversions in 90 days:

| Conversion Action | Type | Issue |
|-------------------|------|-------|
| HubSpot Lead - Manual | UPLOAD_CLICKS | Enabled + include_in_conversions=True but 0 conversions |

**Recommended Action:**
1. Check if HubSpot upload integration is configured correctly
2. Verify GCLID capture on forms
3. If not fixable, set `include_in_conversions=False` to prevent bid optimization issues

### 1.2 LEGACY_UA - Universal Analytics Goals (34 total)

**Universal Analytics sunset on July 1, 2023.** These 34 conversion actions will NEVER fire again:

| Sample Actions | Status |
|----------------|--------|
| Sign Up Newsletter (All Web Site Data) | HIDDEN |
| Contact Us Formfill (All Web Site Data) | HIDDEN |
| Demo Request Formfill (All Web Site Data) | ENABLED |
| Form Submit Conversions (All Web Site Data) | ENABLED |
| ALL GOALS EXCEPT (Live Chat) | ENABLED |

**Impact:** Several still have `include_in_conversions=True`, which means they're counted toward your conversion metrics (contributing $0 and 0 conversions).

**Recommended Action:**
1. Remove all 34 UA goal-based conversion actions
2. These cannot be recovered and serve no purpose
3. Audit script provides full list in `conversion_audit_report.csv`

---

## Priority 2: Broken Integrations (30 Actions)

These conversion actions are ENABLED but recorded zero conversions in 90 days:

### 2.1 Salesforce Integration (10 actions)

| Conversion Action | Type | Default Value |
|-------------------|------|---------------|
| SF: Closed Won | SALESFORCE | $0 |
| SF: Closed Lost | SALESFORCE | $0 |
| SF: MQL | SALESFORCE | $0 |
| SF: SQL | SALESFORCE | $0 |
| SF: SAL | SALESFORCE | $0 |
| SF: New Lead | SALESFORCE | $0 |
| SF: Lead Rejected | SALESFORCE | $0 |
| SF: Opportunity | SALESFORCE | $0 |
| SF: Opportunity Created | SALESFORCE | $0 |
| Lead Converted (salesforce) | SALESFORCE | $1,000 |
| Won Opportunity (salesforce) | SALESFORCE | $10 |
| Working Lead (Salesforce) | SALESFORCE | $200 |
| Working Opportunity (salesforce) | SALESFORCE | $5 |

**Diagnosis:** Salesforce integration appears broken or disconnected.

**Recommended Actions:**
1. Verify Salesforce connector is active in Google Ads
2. Check GCLID is being captured and stored in Salesforce
3. If integration is abandoned, remove these actions
4. If fixing, consolidate to key stages: Lead, MQL, SQL, Opportunity, Closed Won

### 2.2 GA4 Events Not Firing (6 actions)

| Conversion Action | Category |
|-------------------|----------|
| Kibo - GA4 (web) TalkToSales | PAGE_VIEW |
| Kibo - GA4 (web) ecom_sub_demo_registration | SUBMIT_LEAD_FORM |
| Kibo - GA4 (web) ewebinar_click | CONTACT |
| Kibo - GA4 (web) kibo_order_mngmt_demo_registration | SUBMIT_LEAD_FORM |
| Kibo - GA4 (web) order_mngmt_demo_registration | PURCHASE |
| Kibo - GA4 (web) purchase | PURCHASE |

**Note:** Live testing found these GA4 events ARE firing: `request_a_demo`, `thank_you_for_your_request`, `Speak_to_Expert`. The above may be legacy event names.

**Recommended Actions:**
1. Verify event names in GA4 match conversion action names
2. Events are case-sensitive - check exact match
3. Remove duplicate/legacy event tracking

### 2.3 Local & Call Actions (6 actions)

| Conversion Action | Type | Notes |
|-------------------|------|-------|
| Calls from ads | AD_CALL | No call extensions? |
| Clicks to call | GOOGLE_HOSTED | No click-to-call on site? |
| Local actions - Directions | GOOGLE_HOSTED | No Google Business Profile? |
| Local actions - Other engagements | GOOGLE_HOSTED | No local presence? |
| Local actions - Website visits | GOOGLE_HOSTED | Requires Business Profile |
| Android installs | ANDROID_INSTALLS_ALL_OTHER_APPS | No app? |

**Recommended Actions:**
1. If no call tracking - remove call actions
2. If no Google Business Profile - remove local actions
3. If no Android app - remove install tracking

### 2.4 Webpage Pixels with Zero Conversions

| Conversion Action | Issue |
|-------------------|-------|
| HubSpot - Forrester Wave B2C Commerce | Likely campaign-specific, expired |

**Recommended Action:** Remove campaign-specific pixels that are no longer relevant.

---

## Priority 3: Cleanup Unused (29 Actions)

These have status REMOVED or HIDDEN but still clutter the account:

### Webpage Pixels (REMOVED)
- AdWords
- Building a Business Case Download
- Buy Online Pickup In-Store Download
- Consumer Trends Report Download
- Download Resource
- General Conversion Tracking
- Leads
- Lets Get Started Click
- Magento Button
- Order Management Content Download Pixel
- Personalization Content Download Pixel
- Request a Demo
- Thank You - UX
- Thank You Inbound Request
- Thank You Newsletter
- Thank You Ungated
- Unify Retail Customer Experience Download

### GA4 Events (HIDDEN)
- Kibo - GA4 (web) Speak_to_Expert
- Kibo - GA4 (web) become_a_partner
- Kibo - GA4 (web) call_click
- Kibo - GA4 (web) email_click
- Kibo - GA4 (web) file_download
- Kibo - GA4 (web) free_trial_submission
- Kibo - GA4 (web) login_click
- Kibo - GA4 (web) partners_thank_you

**Recommended Action:** Bulk remove all REMOVED/HIDDEN conversion actions to clean up the account.

---

## Healthy Conversions (Keep)

These 8 conversion actions are working correctly:

| Conversion Action | Type | 90-Day Conv | Value | Primary |
|-------------------|------|-------------|-------|---------|
| Request a Demo - Directive | WEBPAGE | 5 | $500 | Yes |
| HubSpot - Lead | UPLOAD_CLICKS | 6 | $6 | Yes |
| All but Demo Conversions | WEBPAGE | 5 | $125 | No |
| HubSpot - MQL | UPLOAD_CLICKS | 1 | $10 | Yes |
| Kibo - GA4 (web) request_a_demo | GA4_CUSTOM | ~1.2 | $1.17 | No |
| Kibo - GA4 (web) thank_you_for_your_request | GA4_CUSTOM | ~1.2 | $1.17 | No |
| Lead Forms 12-4-25 | WEBPAGE | 9 (all_conv) | $0 | No |
| Free Trial Submission | WEBPAGE | 1 (all_conv) | $100 | No |

---

## Recommended Conversion Structure

After cleanup, target this simplified structure:

### Primary Conversions (include_in_conversions=True)
| Action | Type | Purpose | Value |
|--------|------|---------|-------|
| Request a Demo | WEBPAGE | Demo form submit | $100 |
| HubSpot - Lead | UPLOAD_CLICKS | Lead creation | $50 |
| HubSpot - MQL | UPLOAD_CLICKS | Marketing qualified | $200 |

### Secondary Conversions (include_in_conversions=False)
| Action | Type | Purpose | Value |
|--------|------|---------|-------|
| Content Downloads | WEBPAGE | Engagement | $25 |
| Free Trial | WEBPAGE | High intent | $150 |
| GA4 Events | GA4_CUSTOM | Backup tracking | $1 |

---

## Implementation Checklist

### Week 1: Critical Cleanup
- [ ] Remove all 34 LEGACY_UA conversion actions
- [ ] Investigate HubSpot Lead - Manual (BROKEN_PRIMARY)
- [ ] Set broken Salesforce actions to HIDDEN or REMOVED

### Week 2: Integration Audit
- [ ] Verify Salesforce integration status
- [ ] Audit GA4 event names vs. conversion action names
- [ ] Remove unused local/call actions if not applicable

### Week 3: Consolidation
- [ ] Remove all REMOVED/HIDDEN webpage pixels
- [ ] Consolidate duplicate GA4 event tracking
- [ ] Set appropriate include_in_conversions flags

### Week 4: Optimization
- [ ] Add conversion values to all primary conversions
- [ ] Consider enhanced conversions setup
- [ ] Document final conversion structure

---

## Appendix: Full Audit Data

See `conversion_audit_report.csv` for complete details on all 102 conversion actions including:
- Conversion ID
- Name
- Type
- Status
- Category (audit classification)
- Include in conversions setting
- 90-day conversion count
- 90-day conversion value
- Attribution model
- Lookback windows
