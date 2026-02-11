# Kibo Commerce Live Tag Testing Results

**Date:** January 25, 2026
**Tester:** Automated via Playwright
**Site:** kibocommerce.com

---

## Executive Summary

Live tag testing confirms that **core tracking infrastructure is healthy**. GTM, GA4, and Google Ads conversion pixels are properly implemented and firing. However, the audit reveals significant issues with conversion action configuration in Google Ads that prevent proper attribution.

---

## Tag Infrastructure Status

### Google Tag Manager (GTM)
| Property | Value | Status |
|----------|-------|--------|
| Container ID | GTM-PD73CHF | ACTIVE |
| Load Status | Fires on page load | OK |
| dataLayer Events | gtm.js, gtm.dom, gtm.load | OK |

### Google Analytics 4 (GA4)
| Property | Value | Status |
|----------|-------|--------|
| Measurement ID | G-21CTWG5W2Y | ACTIVE |
| Page View Tracking | Fires on navigation | OK |
| Debug Mode | Enabled | OK |

### Google Ads Conversion Tracking
| Property | Value | Status |
|----------|-------|--------|
| Conversion ID | AW-877723722 | ACTIVE |
| Conversion Label | cJy_CKzvi3MQyoDEogM | ACTIVE |
| Fires On | /thank-you-for-your-request/ | OK |
| Conversion Value | $0 (no value passed) | WARNING |

### HubSpot Tracking
| Property | Value | Status |
|----------|-------|--------|
| Portal ID | 40870578 | ACTIVE |
| Analytics Tracking | hs-analytics.net | OK |
| Form Tracking | collectedforms.js | OK |
| Chat Widget | conversations-embed.js | OK |

### Additional Tracking
| Platform | Status | Notes |
|----------|--------|-------|
| Facebook Pixel | ACTIVE | ID: 2386873278224987 |
| DemandBase | ACTIVE | B2B intent data |
| Microsoft Clarity | ACTIVE | Session recording |
| Usercentrics CMP | ACTIVE | GDPR consent management |

---

## Page-by-Page Test Results

### Homepage (kibocommerce.com)
- GTM container loads: YES
- GA4 pageview fires: YES
- Consent banner present: YES (Usercentrics)
- All core scripts load successfully

### Demo Request Page (/request-a-demo/)
- Page loads: YES
- Form present: YES (1 HTML form detected)
- HubSpot form tracking: ACTIVE
- GTM tracking: ACTIVE

### Thank You Page (/thank-you-for-your-request/)
**This is the critical conversion page**

**Events Fired:**
1. `page_view` - GA4 pageview
2. `Speak_to_Expert` - Custom GA4 event
3. `thank_you_for_your_request` - Custom GA4 event
4. `request_a_demo` - Custom GA4 event
5. `scroll` - Engagement tracking (90%, 100%)

**Google Ads Conversion Pixel:**
```
URL: googleadservices.com/pagead/conversion/877723722/
Label: cJy_CKzvi3MQyoDEogM
Type: purchase
Value: 0
```

**Verification:** Google Ads conversion pixel IS firing correctly on the thank you page.

---

## Network Request Analysis

### GA4 Requests (Thank You Page)
| Endpoint | Events | Status |
|----------|--------|--------|
| analytics.google.com/g/collect | page_view, user_engagement | 200/204 |
| google-analytics.com/g/collect | Speak_to_Expert, request_a_demo, thank_you_for_your_request | 204 |
| pagead2.googlesyndication.com/measurement/conversion | GA4 events to Ads | 200 |
| google.com/measurement/conversion | GA4 event attribution | 200 |
| googleadservices.com/pagead/conversion | Direct Ads pixel | 200 |
| stats.g.doubleclick.net/g/collect | Cross-device tracking | 204 |

---

## Critical Findings

### 1. Google Ads Conversion Pixel is Firing
**Status:** WORKING
The pixel with ID AW-877723722 fires on the thank you page. However, the audit shows only 8 of 102 conversion actions are receiving data, suggesting:
- The pixel IS firing
- But many conversion actions in Google Ads are misconfigured or orphaned

### 2. GA4-to-Ads Integration Working
Multiple GA4 events are being sent to Google Ads via the measurement/conversion endpoints:
- `Speak_to_Expert`
- `thank_you_for_your_request`
- `request_a_demo`

### 3. Conversion Value Not Passed
The Google Ads conversion pixel fires with `value=0`. Consider passing a conversion value for ROAS optimization:
```javascript
gtag('event', 'conversion', {
  'send_to': 'AW-877723722/cJy_CKzvi3MQyoDEogM',
  'value': 100.0,  // Example: $100 lead value
  'currency': 'USD'
});
```

### 4. Consent Mode Active
Usercentrics CMP is managing consent. When consent is denied:
- GA4 fires with `gcs=G100` (consent denied)
- Some tracking may be blocked based on user consent preferences

---

## Recommendations from Tag Testing

1. **Verify Google Ads Conversion Linking:**
   - The pixel fires but check if conversion actions in Google Ads are properly linked to this pixel
   - AW-877723722 should match the conversion action configuration

2. **Add Conversion Value:**
   - Pass dynamic or static conversion values for ROAS optimization
   - Consider: $100 for demo requests, $25 for content downloads

3. **Review GA4 Event Naming:**
   - `Speak_to_Expert` vs `thank_you_for_your_request` - consolidate similar events
   - Ensure event names match conversion actions in Google Ads

4. **Verify Enhanced Conversions:**
   - Consider implementing enhanced conversions for better attribution
   - Pass hashed email on form submission

---

## Tag Testing Conclusion

**Site tracking infrastructure is healthy.** The core issue is not tag implementation but rather Google Ads conversion action configuration:

- 34 Legacy UA goals still in account (non-functional since July 2023)
- 30+ enabled conversion actions with 0 conversions
- Only 8 conversion actions receiving data

The tags ARE firing correctly - the problem is on the Google Ads configuration side.
