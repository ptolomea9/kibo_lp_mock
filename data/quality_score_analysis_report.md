# Kibo Commerce: Quality Score Pre/Post Analysis
## Keyword URL Changes Impact Assessment
### February 10, 2026

---

## Executive Summary

Following keyword-level URL changes implemented across the Kibo Commerce "Search - NonBrand" campaign, we conducted a pre/post analysis comparing historical quality scores (Oct-Dec 2025) with current data (Feb 5-9, 2026 — 5 days since the campaign was unpaused).

**Key Findings:**
- **105 keywords** now have keyword-level Final URLs (up from 0 historically)
- **Impression-weighted QS improved from 3.02 to 5.27 (+2.25)** — but this is driven primarily by one new high-QS keyword (`ecommerce ai search`, QS=7, 295 of 522 total impressions)
- **Simple average QS is flat: 3.10 → 3.06** — the URL changes alone have not yet moved the needle
- **100% of keywords still rated "Below Average" for Landing Page Experience** — this is the primary drag on QS
- **31 problem keywords** across 8 landing pages still have QS ≤ 5 with landing page issues

---

## 1. Change Timeline

| Event | Timing |
|-------|--------|
| Keyword-level URLs applied | ~Late Jan 2026 (change events older than 30 days) |
| Campaign unpaused | ~Feb 3-4, 2026 |
| Data collection window | Feb 5–9, 2026 (5 days) |
| Keywords with URLs set | 105 of 926 total keywords |
| Keywords receiving impressions | 39 unique keywords in last 7 days |

---

## 2. Impression-Weighted Quality Score

| Metric | Historical (Oct-Dec) | Current (Post-Changes) | Delta |
|--------|---------------------|----------------------|-------|
| Keywords with QS | 49 | 32 (18 with impressions) | -17 |
| Total Impressions | 10,745 | 522 | -10,223 |
| Simple Avg QS | 3.10 | 3.06 | -0.04 |
| Impression-Weighted QS | 3.02 | 5.27 | +2.25 |

### Important Caveat on the Weighted QS Improvement
The +2.25 weighted QS improvement is primarily driven by **one new keyword:**
- `ecommerce ai search` — QS=7, 295 impressions (56% of all impressions)
- This keyword was NOT in the historical dataset
- Excluding this keyword, the weighted QS would be approximately 3.2

**Bottom line:** The URL changes established proper keyword-to-page mapping, but the underlying landing pages themselves are still causing "Below Average" ratings across the board.

---

## 3. QS Sub-Component Breakdown

### Landing Page Experience
| Rating | Historical | Current |
|--------|-----------|---------|
| Below Average | 49 (100%) | 32 (100%) |
| Average | 0 (0%) | 0 (0%) |
| Above Average | 0 (0%) | 0 (0%) |

**This is THE core problem.** Every single keyword is rated "Below Average" for landing page experience. URL changes alone cannot fix this — the pages themselves need improvement.

### Expected CTR
| Rating | Historical | Current |
|--------|-----------|---------|
| Below Average | 45 (92%) | 30 (94%) |
| Average | 4 (8%) | 1 (3%) |
| Above Average | 0 (0%) | 1 (3%) |

### Ad Relevance
| Rating | Historical | Current |
|--------|-----------|---------|
| Below Average | 0 (0%) | 0 (0%) |
| Average | 3 (6%) | 4 (13%) |
| Above Average | 46 (94%) | 28 (87%) |

Ad relevance remains strong — the ad copy is well-aligned. The problem is squarely on the landing page side.

---

## 4. Problem Landing Pages

### Ranked by Impression Volume (Keywords with QS ≤ 5 + LP Issues)

| # | Landing Page URL | Keywords | Impressions | Avg QS |
|---|-----------------|----------|-------------|--------|
| 1 | kibocommerce.com/solutions/b2b/ | 9 | 61 | 3.2 |
| 2 | kibocommerce.com/ppc/wholesale/ | 3 | 46 | 3.0 |
| 3 | kibocommerce.com/platform/reverse-logistics/ | 1 | 40 | 3.0 |
| 4 | kibocommerce.com/ (homepage) | 4 | 37 | 2.8 |
| 5 | kibocommerce.com/platform/order-management/ | 8 | 28 | 2.6 |
| 6 | No keyword-level URL | 3 | 13 | 3.0 |
| 7 | kibocommerce.com/platform/inventory-visibility/ | 2 | 2 | 3.0 |
| 8 | kibocommerce.com/ppc/manufacturing/ | 1 | 0 | 3.0 |

---

## 5. Landing Page Diagnosis

After crawling all 5 major landing pages, the following systemic issues were identified:

### Issue #1: Heavy Page Builder (Elementor) — ALL Pages
- All pages use WordPress + Elementor Pro, generating massive DOM trees
- Extensive inline CSS (100KB+) and JavaScript bundles
- Multiple third-party scripts loading: GTM, HubSpot, Facebook SDK, Swiper.js
- **Impact:** Poor Core Web Vitals (LCP, CLS, INP), which Google directly factors into LP quality

### Issue #2: No On-Page Lead Capture — 4 of 5 Pages
- `/solutions/b2b/`, `/platform/order-management/`, `/`, `/platform/reverse-logistics/` all have CTAs that link AWAY to separate pages
- Only `/ppc/wholesale/` has an embedded HubSpot form
- **Impact:** Google sees redirect-based conversion paths as lower-quality experiences

### Issue #3: Content Overload (3,500-4,200 words)
- Pages like `/solutions/b2b/` and `/platform/order-management/` have 3,500+ words
- Too much content dilutes keyword relevance and increases load time
- **Impact:** Users land and see walls of content that don't immediately match their query intent

### Issue #4: Generic CTAs
- "Watch a Demo" and "Talk to Sales" appear on every page regardless of keyword intent
- No dynamic messaging matched to search intent
- **Impact:** Lower engagement signals (bounce rate, time on page)

### Issue #5: Homepage as Landing Page
- 4 keywords (`unified commerce platform`, `digital commerce solutions`, `b2b trade portal`, `b2b dealer portal`) land on the homepage
- Homepage is inherently generalist and cannot serve keyword-specific intent well
- **Impact:** Poor keyword-to-content alignment

---

## 6. Recommendations: Ideal Landing Page Architecture

Based on best practices for **composable B2B SaaS companies** (BigCommerce, commercetools, Salesforce Commerce Cloud, Sana Commerce approach):

### The "Solution Cluster" Approach
Instead of 8+ separate landing pages, create **3-4 templated PPC landing pages** that can be parameterized to serve clusters of related keywords:

| Landing Page | Keyword Cluster | Est. Keywords Served |
|--------------|----------------|---------------------|
| **B2B Commerce PPC** | b2b commerce platform, b2b ecommerce platforms, best b2b ecommerce platforms, b2b commerce software, b2b ecommerce solution, b2b order portal, b2b vendor/buyer/dealer/trade portal | 15-20 |
| **OMS PPC** | best order management systems, ecommerce oms, enterprise order management system, order management system ecommerce, b2b order management system, manufacturing/distribution OMS | 10-12 |
| **Wholesale/Distribution PPC** | wholesale ecommerce platform, wholesale b2b portal, wholesale distribution platform, wholesale order management system | 5-8 |
| **Inventory/Fulfillment PPC** | multi-location inventory management, vendor managed inventory, rma software, reverse logistics | 5-6 |

### Landing Page Requirements
1. **Lightweight code** — NO Elementor. Static HTML/CSS or lightweight React. Target < 200KB total page weight
2. **Embedded form** — HubSpot form directly on page, visible above the fold on desktop
3. **Focused content** — 800-1,200 words max, keyword-dense in H1/H2/first paragraph
4. **Fast load** — Target LCP < 2.5s, INP < 200ms, CLS < 0.1
5. **Social proof block** — 3-4 customer logos + 1 stat + 1 analyst badge above the fold
6. **Mobile-first** — Form and CTA accessible without scrolling on mobile
7. **Schema markup** — SoftwareApplication + FAQ schema
8. **Minimal navigation** — Sticky header with logo + phone + CTA only (no full site nav to reduce bounce paths)

### Content Structure for Each PPC Page
```
[Sticky Header: Logo | Phone | CTA Button]

[Hero]
  H1: Keyword-aligned headline
  Subhead: Value proposition (1 sentence)
  2-3 bullet points of key differentiators
  [Embedded Form]
  Trust bar: 4-5 customer logos

[Social Proof]
  Stat block: "296% revenue increase" | "67% fewer returns" | "<6mo payback"
  Forrester/Gartner badge

[How It Works]
  3 steps with icons (not images)
  Each step: 20-30 words

[Key Capabilities]
  4-6 capability cards (icon + headline + 1 sentence)

[Customer Quote]
  Single testimonial with photo + company + title

[FAQ Section]
  3-4 questions using schema markup

[Final CTA]
  Repeated form or strong CTA button

[Minimal Footer]
  Company info | Privacy | Trust Center
```

---

## 7. Projected Impact

With properly optimized PPC landing pages, we expect:

| Metric | Current | Target (90 days) | Basis |
|--------|---------|-------------------|-------|
| Avg QS | 3.06 | 5-6 | Industry benchmark for optimized B2B SaaS |
| Landing Page Exp. | 100% Below Avg | 50%+ Average | Fixing CWV + content relevance |
| Impression-Weighted QS | 3.02 (excl. outlier) | 5.0+ | Weighted toward high-volume KWs |
| Estimated CPC Reduction | Baseline | 15-25% | QS 3→6 typically reduces CPC ~20% |
| Estimated IS Improvement | Baseline | +10-15pp | Better Ad Rank from higher QS |

---

## 8. Priority Action Items

1. **IMMEDIATE:** Design and deploy the B2B Commerce PPC landing page (covers 15-20 keywords, highest impression volume)
2. **WEEK 2:** Deploy OMS PPC landing page (covers 10-12 keywords)
3. **WEEK 3:** Deploy Wholesale/Distribution PPC landing page (can iterate on existing `/ppc/wholesale/` which already has a form)
4. **WEEK 4:** Deploy Inventory/Fulfillment PPC landing page
5. **ONGOING:** Monitor QS weekly, iterate on content/speed based on which sub-components improve

---

*Analysis conducted Feb 10, 2026. Data sourced from Google Ads API (account 994-869-7111) and Kibo Commerce website crawls.*
