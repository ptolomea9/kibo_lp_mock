# Kibo Commerce: New PPC Landing Page vs. Existing Subfolder Pages
## Competitive Comparison & Gap Analysis
### February 10, 2026

---

## 1. Current State — Existing Kibo Pages We're Driving NB Traffic To

These are the 6 URLs currently receiving non-brand paid search traffic:

| URL | Type | Keywords Served | QS | LP Experience |
|-----|------|----------------|-----|---------------|
| `/solutions/b2b/` | Subfolder (Elementor) | 9 keywords (b2b commerce platform, b2b ecommerce platforms, etc.) | 3.0-3.2 | 100% Below Average |
| `/platform/order-management/` | Subfolder (Elementor) | 8 keywords (best order management systems, ecommerce oms, etc.) | 2.0-3.0 | 100% Below Average |
| `/ppc/wholesale/` | Dedicated PPC page (Elementor) | 3 keywords (wholesale ecommerce platform, etc.) | 3.0 | Below Average |
| `/ppc/manufacturing/` | Dedicated PPC page (Elementor) | 1 keyword | 3.0 | Below Average |
| `/platform/reverse-logistics/` | Subfolder (Elementor) | 1 keyword (rma software) | 3.0 | Below Average |
| `/` (Homepage) | Homepage (Elementor) | 4 keywords (unified commerce, digital commerce, b2b trade portal, b2b dealer portal) | 2.0-3.0 | Below Average |

**Common thread: 100% of keywords rated "Below Average" for Landing Page Experience.**

---

## 2. What the Existing Kibo Pages Do WELL

Credit where due — several things are strong on the current site:

### Ad Relevance is Excellent
- **94% of keywords rated "Above Average" for Ad Relevance** historically
- **87% currently still Above Average**
- The ad copy is well-matched to search intent — the copywriting team is doing their job

### Comprehensive Feature Content
- Pages like `/solutions/b2b/` and `/platform/order-management/` are thorough
- They cover the full breadth of capabilities (contract pricing, portals, inventory, etc.)
- This depth is good for organic SEO and mid-funnel education

### PPC Subfolder Concept Exists
- Kibo already has `/ppc/wholesale/`, `/ppc/distributor/`, `/ppc/manufacturing/`
- This shows awareness that PPC traffic needs dedicated pages
- `/ppc/wholesale/` even has an embedded HubSpot form — the ONLY current page that does

### Trust Signals Are Present
- Customer logos appear across the site
- Forrester Wave and Gartner recognition are referenced
- Case study data (Ace Hardware, Fortis Life Sciences) is available

### Clear Product Positioning
- "Unified Commerce + OMS on one data model" is a genuinely strong differentiator
- B2B-specific messaging (contract pricing, approval workflows, buyer portals)
- The messaging IS good — the delivery vehicle (heavy Elementor pages) is the problem

---

## 3. What's WRONG with the Existing Pages (Why QS = 3)

### Issue #1: Elementor Page Builder on ALL Pages
- Every page uses WordPress + Elementor Pro
- Generates massive DOM trees (3,000+ DOM nodes)
- Inline CSS: 100KB+ on every page
- JavaScript bundles: GTM, HubSpot, Facebook SDK, Swiper.js, Elementor runtime
- **Result:** Poor Core Web Vitals → Google rates LP Experience "Below Average"
- **Our new page:** ~109KB total (HTML + CSS + JS inline). Zero external dependencies except Google Fonts.

### Issue #2: No Embedded Forms on 5 of 6 Pages
- `/solutions/b2b/` → "Watch a Demo" links to `/request-a-demo/`
- `/platform/order-management/` → "Talk to Sales" links to `/speak-with-an-expert/`
- Homepage → Generic "Watch a Demo" link
- `/platform/reverse-logistics/` → "Learn More" link
- `/ppc/manufacturing/` → Links to separate form page
- Only `/ppc/wholesale/` has an embedded HubSpot form
- **Result:** Google penalizes redirect-heavy conversion paths. User lands, sees no form, bounces or follows a link chain.
- **Our new page:** Embedded form above the fold in hero. Second form in final CTA. Zero redirects for conversion.

### Issue #3: Content Overload (3,500-4,200 Words)
- `/solutions/b2b/`: ~3,800 words
- `/platform/order-management/`: ~4,200 words
- Users searching "b2b ecommerce platform" need to find relevance in 3 seconds
- Walls of text dilute keyword density and increase load time
- **Our new page:** ~1,800 words focused on the keyword cluster. H1, H2s, and first paragraph all keyword-dense.

### Issue #4: Full Site Navigation on Every Page
- Full header: Platform dropdown, Solutions dropdown, Resources, Customer Stories, Demo, etc.
- 15+ exit paths before the user even sees the main content
- PPC best practice: minimize navigation to funnel toward one action
- **Our new page:** Minimal sticky header — Logo, phone number, single CTA button. Zero dropdown menus.

### Issue #5: Homepage as Landing Page (4 Keywords)
- `unified commerce platform`, `digital commerce solutions`, `b2b trade portal`, `b2b dealer portal` all point to the homepage
- Homepage serves EVERY audience (B2B, B2C, retail, wholesale, manufacturing)
- Impossible to optimize for any single keyword cluster
- **Our new page:** Purpose-built for the B2B commerce keyword cluster. Every section speaks to B2B buyers.

### Issue #6: Generic CTAs Across All Pages
- "Watch a Demo" and "Talk to Sales" are the same CTAs on every page
- No urgency, no specificity, no intent-matching
- **Our new page:** "Request Your Demo" with context-specific subtext, urgency cues, and benefit bullets next to the form.

---

## 4. What's NET NEW in Our Landing Page (Didn't Exist on Any Kibo Page)

| Feature | Exists on Current Kibo Site? | Our New Page |
|---------|------------------------------|--------------|
| **Embedded lead capture form in hero** | Only on `/ppc/wholesale/` | Yes — 2 forms (hero + final CTA) |
| **ROI Calculator** | No | Interactive with 5 sliders, real-time savings estimate based on Forrester TEI methodology |
| **Comparison Table (Kibo vs. alternatives)** | No | 8-row capability matrix: Kibo vs. Multi-Vendor Stack vs. Pure-Play Commerce |
| **FAQ with Schema Markup** | No | 6 FAQs with JSON-LD schema for rich snippets in SERP |
| **"Without Kibo / With Kibo" before/after** | No | Side-by-side problem/solution contrast with pain points vs. benefits |
| **Minimal PPC navigation** | Partially (on `/ppc/` pages) | Logo + phone + CTA only. Zero dropdowns, zero exit paths. |
| **Customer testimonials with attribution** | Partial (no direct quotes on product pages) | 4 attributed testimonials with role, company, and quantified result per quote |
| **Stats bar with animated counters** | No | 296% revenue increase, 167% ROI, <6mo payback, 67% fewer returns — animated on scroll |
| **Industry vertical cards** | Partial (separate `/solutions/` pages) | 4 verticals inline: Manufacturing, Wholesale, Multi-Brand, Hybrid B2B/B2C |
| **Architecture diagram** | No | 3-layer interactive diagram: Experience Layer → Kibo Platform → Connect Hub |
| **4-step "How It Works" flow** | No | Discover → Quote → Route → Self-Serve with keyword-rich descriptions |
| **Integration ecosystem grid** | Partial (Connect Hub page exists separately) | ERP, Fulfillment, Payments grouped with named partners (SAP, Oracle, Stripe, etc.) |
| **Lightweight page weight** | No (all pages 500KB-1.5MB+) | ~109KB total. Zero external JS dependencies. |
| **Mobile-first design** | Not optimized for PPC mobile | Form accessible without scrolling. Touch-optimized. |
| **Forrester TEI methodology link** | Report exists in resource center | Linked directly from ROI calculator methodology note |

---

## 5. Competitive Landscape — What Competitors Do for PPC

### BigCommerce B2B
- **Approach:** Hybrid — dedicated `/dm/` demo pages + subfolder product pages
- **Navigation:** Stripped on dedicated landing pages
- **Form:** Links to separate form pages (NOT embedded)
- **Strength:** Native PPC-to-landing-page matching feature
- **Weakness:** Forms not embedded; Makeswift page builder adds weight
- **vs. Our page:** We have embedded forms + lighter code. They have tighter ad-to-LP matching automation.

### Sana Commerce
- **Approach:** Main site pages with full navigation
- **Navigation:** Full site nav maintained
- **Form:** Embedded Marketo forms on demo page
- **Strength:** Quantified social proof ("80% adoption", "30% revenue growth"), named executive testimonials
- **Weakness:** Full navigation = many exit paths; CMS-heavy pages
- **vs. Our page:** We match their social proof approach and beat them on navigation reduction and page weight.

### commercetools
- **Approach:** Product/solution pages from main site
- **Navigation:** Full navigation maintained
- **Form:** Links to separate demo flows
- **Strength:** Composable architecture messaging appeals to technical buyers; massive multi-channel campaign infrastructure (3,000+ ads)
- **Weakness:** Heavy documentation-style pages; no embedded forms on product pages
- **vs. Our page:** We have a cleaner conversion path. They have better multi-channel campaign orchestration.

### Salesforce Commerce Cloud (B2B)
- **Approach:** Dedicated form pages at `/form/commerce/b2b-commerce-demo/`
- **Navigation:** Full enterprise nav
- **Form:** Separate dedicated form pages
- **Strength:** Full CRM ecosystem leverage; AI/Agentforce positioning; regional variants
- **Weakness:** Extremely heavy enterprise CMS (multiple tracking systems, multi-layer analytics); form on separate page from product info
- **vs. Our page:** We have a dramatically lighter page with form + content on the same page. They have ecosystem dominance.

### OroCommerce
- **Approach:** Dedicated demo page with dual pathways
- **Navigation:** Full site nav
- **Form:** Embedded with self-serve AND personalized demo options
- **Strength:** Open-source positioning; dual demo paths (instant access vs. scheduled)
- **Weakness:** Full navigation; less brand recognition
- **vs. Our page:** Their dual demo pathway is smart — we could consider adding a self-service option. We beat them on page weight and navigation.

---

## 6. Competitive Feature Matrix

| Feature | Kibo (Current) | Kibo (New LP) | BigCommerce | Sana Commerce | commercetools | Salesforce | OroCommerce |
|---------|---------------|---------------|-------------|---------------|---------------|------------|-------------|
| Dedicated PPC pages | Partial (`/ppc/`) | Yes | Yes (`/dm/`) | No | No | Yes (`/form/`) | Partial |
| Embedded form | 1 of 6 pages | Yes (2 forms) | No | Yes (Marketo) | No | No (separate) | Yes |
| Stripped navigation | No | Yes | Partial | No | No | No | No |
| Page weight | 500KB-1.5MB | ~109KB | Medium-heavy | Heavy (CMS) | Medium | Very heavy | Medium |
| ROI calculator | No | Yes | No | No | No | No | No |
| Comparison table | No | Yes | Yes | No | No | No | No |
| FAQ schema | No | Yes | No | Partial | No | No | No |
| Architecture diagram | No | Yes | No | No | Partial | No | No |
| Quantified testimonials | No | Yes (4) | Partial | Yes | Partial | Partial | Partial |
| Stats with sources | No | Yes (Forrester) | Partial | Yes | No | No | Partial |
| Mobile-first PPC | No | Yes | Partial | No | No | No | No |

---

## 7. PROS of Our New Landing Page

1. **109KB vs. 500KB-1.5MB** — 5-10x lighter than any current Kibo page or competitor page
2. **Two embedded forms** — hero + final CTA, zero redirect conversion path
3. **Stripped navigation** — only 2 exit paths (logo home link, phone number) vs. 15+ on current site
4. **ROI calculator** — no competitor has this on their PPC landing page; generates engagement time signals
5. **Comparison table** — directly addresses "best b2b ecommerce platform" intent with competitive positioning
6. **FAQ schema markup** — eligible for rich snippets; no current page or competitor has this
7. **Before/after framework** — "Without Kibo / With Kibo" is a proven SaaS conversion pattern
8. **Keyword-dense structure** — H1, H2s, meta description, first paragraph all target the cluster
9. **Zero external dependencies** — no Elementor, no HubSpot JS library, no Facebook SDK, no Swiper.js
10. **Standalone deployment** — can be hosted anywhere (Vercel, S3, Netlify) independent of WordPress
11. **Mobile-first** — form visible without scrolling on mobile; touch targets properly sized
12. **Forrester TEI data woven throughout** — 167% ROI, <6mo payback cited with linked source

---

## 8. CONS / Risks of Our New Landing Page

1. **Not on kibocommerce.com domain** — currently deployed on Vercel, not on the Kibo domain. Google's QS assessment needs it on the same domain as the display URL in ads. **This must be resolved for production.**
2. **No HubSpot form integration** — our forms are HTML mockups. Production deployment needs real HubSpot embed or server-side form handling.
3. **No analytics tracking** — no GTM, no GA4, no HubSpot tracking on the standalone page yet.
4. **No A/B testing infrastructure** — no Optimizely, no VWO, no built-in variant testing.
5. **Content not CMS-managed** — any copy changes require editing raw HTML. Marketing team can't self-serve updates.
6. **Brand consistency risk** — our page has a custom design system. Need to ensure it passes Kibo brand review.
7. **Only covers B2B Commerce cluster** — still need OMS, Wholesale, and Inventory pages for the other keyword clusters.
8. **Testimonials need legal clearance** — attributed quotes need approval from Ace Hardware, Fortis Life Sciences, Wolters Kluwer.
9. **No personalization** — no dynamic content based on visitor company/industry. Salesforce and commercetools do this.
10. **Single-language** — no i18n support. Salesforce has regional variants (FR, UK, EU).

---

## 9. Production Deployment Path

To move from mock to production, these items need to be addressed:

| Item | Priority | Owner | Notes |
|------|----------|-------|-------|
| Deploy to `kibocommerce.com/ppc/b2b-commerce/` | P0 | DevOps/IT | QS requires same domain as ad display URL |
| Replace HTML forms with HubSpot embed | P0 | Marketing Ops | Need form ID and portal ID |
| Add GTM container | P0 | Analytics | GA4 + conversion tracking |
| Legal review of testimonial quotes | P1 | Legal/Marketing | Verify attribution permissions |
| Brand review of visual design | P1 | Brand/Design | Colors, logo usage, typography |
| Add phone tracking number | P1 | Media team | CallRail or similar for PPC attribution |
| Add Google Ads conversion pixel | P0 | Media team | Form submit + phone click events |
| Build OMS variant page | P2 | This team | Covers 10-12 OMS keywords |
| Build Wholesale variant page | P2 | This team | Can iterate on existing `/ppc/wholesale/` |
| Build Inventory variant page | P3 | This team | Covers 5-6 keywords |

---

## 10. Expected QS Impact

| Metric | Current (Subfolder Pages) | Projected (New LP, 90 days) | Basis |
|--------|--------------------------|----------------------------|-------|
| Average QS | 3.06 | 5-6 | Industry benchmark for optimized B2B SaaS LP |
| Landing Page Exp. | 100% Below Average | 50%+ Average | CWV improvement + content relevance |
| Expected CTR | 94% Below Average | 40-50% Average | Better message match → higher CTR |
| Ad Relevance | 87% Above Average | 90%+ Above Average | Maintain current strength |
| Estimated CPC Reduction | Baseline | 15-25% | QS 3→6 typically reduces CPC ~20% |
| Estimated IS Improvement | Baseline | +10-15pp | Better Ad Rank from higher QS |

---

*Analysis compiled Feb 10, 2026. Based on Google Ads data (account 994-869-7111), Kibo Commerce site crawls, and competitive research.*
