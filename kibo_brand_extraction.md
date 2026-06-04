# Kibo Commerce Brand Extraction

> Extracted from `kibocommerce.com/ppc/wholesale/` (PPC LP) and `kibocommerce.com/platform/order-management/` (organic OMS page) on March 25, 2026.

---

## 1. Brand Colors (Hex Codes)

### Primary Palette
| Role | Hex | RGB | Usage |
|---|---|---|---|
| **Primary CTA (Yellow)** | `#FFCE01` | rgb(255, 206, 1) | All CTA buttons ("Speak with an Expert", "Contact Sales", "Watch Demo") |
| **Primary Text (Dark)** | `#2E343E` | rgb(46, 52, 62) | Body text, headings on white backgrounds |
| **CTA Text** | `#2B2B2B` | rgb(43, 43, 43) | Text inside yellow CTA buttons |
| **Hero Dark BG** | `#102E77` | rgb(16, 46, 119) | Hero section background on PPC page (dark navy blue) |
| **White** | `#FFFFFF` | rgb(255, 255, 255) | Page background, text on dark sections |

### Secondary / Accent
| Role | Hex | RGB | Usage |
|---|---|---|---|
| **Accent Orange** | `#FF7119` | rgb(255, 113, 25) | Stat counter numbers (65%, 36%, 88%), animated counters |
| **Link Blue** | `#146FF8` | rgb(20, 111, 248) | Interactive elements, links |
| **Light Gray BG** | `#EAEDF2` | rgb(234, 237, 242) | Alternate section backgrounds (OMS page) |
| **Alt Light Gray** | `#E9E9EB` | rgb(233, 233, 235) | Alternate section backgrounds (PPC page) |
| **Footer Dark** | `#020101` | rgb(2, 1, 1) | Footer background |
| **Nav Item Dark** | `#3F444B` | rgb(63, 68, 75) | Navigation sub-items (OMS page) |

### Supporting Text Colors
| Role | Hex | Usage |
|---|---|---|
| **Secondary Text** | `#656868` | Muted body copy |
| **Tertiary Text** | `#8C8C8C` | Footer links, metadata |
| **Dark Alt** | `#1F2124` | Some heading variants |
| **Medium Gray** | `#808080` | Disabled/muted elements |

---

## 2. Typography

### Font Stack
```css
font-family: "Poppins", sans-serif;
```

All text uses Poppins exclusively (headings, body, CTAs, nav, footer). No secondary font in active use on these pages. Roboto and Montserrat are loaded but not actively rendered on visible elements.

### Font Loading
- **Poppins**: Weights 100-900, normal + italic (self-hosted via `/wp-content/cache/perfmatters/`)
- **Roboto**: Weights 100-900, normal + italic (self-hosted, loaded but secondary)
- **Montserrat**: Weight 100 only (loaded but not actively used)
- **Font Awesome 6.4.2**: Icon font (loaded via CDN link)

### Type Scale
| Element | Size | Weight | Line Height | Color |
|---|---|---|---|---|
| H1 (PPC hero) | 40px | 400 | 42.8px (1.07) | `#FFFFFF` (on dark bg) |
| H1 (OMS page) | 24px | 600 | -- | `#2E343E` |
| H2 (section) | 34px | 400 | 40.8px (1.2) | `#2E343E` |
| H2 (hero, OMS) | 40px | 400 | -- | `#2E343E` |
| H3 (testimonial) | 24px | 600 | 26.4px (1.1) | `#2E343E` |
| H5 (subtitle) | 16px | 500 | 16px (1.0) | `#FFFFFF` |
| H6 (form heading) | 16px | 500 | 19.2px (1.2) | `#2E343E` |
| Body / Paragraph | 16px | 400 | 24px (1.5) | `#2E343E` |
| CTA Button | 15px | 500 | 18px | `#2B2B2B` |
| Nav CTA (small) | 14px | 500 | -- | `#2B2B2B` |
| Stat Numbers | 44px | 600 | -- | `#FF7119` |

---

## 3. Logo URLs

| Variant | URL |
|---|---|
| **Header Logo (dark/color)** | `https://kibocommerce.com/wp-content/uploads/2025/12/Kibo-FC-Black-3.png` |
| **Footer Logo (white/reversed)** | `https://kibocommerce.com/wp-content/uploads/2025/12/kibo-footer-logo.png` |

---

## 4. HubSpot Form Details

### Portal & Region
- **Portal ID**: `244644762`
- **Region**: `na2`

### Forms on PPC Wholesale Page
| Form ID | Redirect URL | Purpose |
|---|---|---|
| `d182d7c6-f4c5-469e-8c46-3e81dacfe56b` | `/thank-you/` | Primary demo request form |
| `c5a74857-3ff5-48c7-97f6-737bdac890d6` | `/thank-you-speak-to-an-expert/` | "Speak with an Expert" form |
| `3412b0c3-9638-4b21-84cc-70c35b55a1da` | `/libertine-social-shoptalk-2026-thank-you` | Shoptalk promo (popup) |

### Embed Pattern
```javascript
hbspt.forms.create({
  portalId: "244644762",
  formId: "FORM_ID_HERE",
  region: "na2",
  redirectUrl: "/thank-you/"
});
```

### Tracking Scripts Present
- **GCLID capture**: Cookie-based, 30-day expiry, passes to HubSpot form hidden field
- **li_fat_id capture**: LinkedIn first-party cookie, 90-day expiry, passes to HubSpot hidden field `linkedin_click_id`
- **HubSpot chat widget**: Portal `244644762`, conversations iframe embedded
- **HubSpot web-interactives**: `js.hubspot.com/web-interactives-embed.js`

---

## 5. PPC Landing Page Template Structure (Wholesale)

### Navigation
**Stripped navigation** -- NO header/nav bar on the PPC page. The page starts directly with the hero section. Footer contains full site links (Products, Add-Ons, Solutions, Company). This is the standard PPC LP pattern: remove top nav to prevent exit.

### Section-by-Section Layout

#### Section 1: Hero (Split Layout)
- **Background**: Dark navy `#102E77`
- **Layout**: Two-column (text left ~60%, form right ~40%)
- **Left column**:
  - H1: Main headline (white, 40px, weight 400)
  - H5: Subtitle (white, 16px, weight 500)
  - Body paragraph: Value prop description (white)
- **Right column**:
  - H6 heading: "Talk to an expert about KIBO for Wholesalers"
  - Yellow triangle accent SVG decoration
  - Embedded HubSpot form (form ID: `d182d7c6-...`)
- **No hero image** -- text + form only

#### Section 2: Value Prop + Icon (Light BG)
- **Background**: White `#FFFFFF`
- **Layout**: Two-column (text left ~65%, icon right ~35%)
- **Content**:
  - H2 heading (34px, dark)
  - Body paragraph explaining pain points
  - CTA button: "Speak with an Expert" (links to `#form` anchor)
- **Icon**: Large SVG illustration on right (custom-segments-icon.svg)

#### Section 3: Feature List with Icons
- **Background**: White or light gray
- **Layout**: Full-width H2 heading + descriptive paragraph, then icon grid
- **Icon grid**: 5 features, each with:
  - Small SVG icon (Unify, Truck, List-2, Search, List)
  - One-line description paragraph
- **CTA**: "Speak with an Expert" button at bottom

#### Section 4: Stats / Social Proof (Metrics)
- **Background**: White `#FFFFFF`
- **Layout**: H2 heading, then 3-column stat grid
- **Stats format**:
  - Large animated counter number (44px, weight 600, color `#FF7119`)
  - "%" suffix (same style)
  - Descriptor text below (16px, weight 500, dark)
- **Actual values**: 65% (implementation time), 36% (quarterly revenue), 88% (AOV)

#### Section 5: Testimonial
- **Background**: White `#FFFFFF`
- **Layout**: Two-column
  - Left: Customer logo (Fortis Life Sciences)
  - Right: Yellow quotation mark SVG + H3 quote text + attribution paragraph
- **Attribution format**: "-Title, Company Name"

#### Section 6: Logo Carousel
- **Component**: Elementor Image Carousel (Swiper v8)
- **37 logos** rotating (Ace Hardware, Total Wine, Office Depot, Playboy, Nivel Parts, etc.)
- **CTA**: "Speak with an Expert" button below carousel

#### Section 7: Modernization Pitch (with Icon)
- **Background**: White
- **Layout**: Two-column (text left with bullet list, icon right)
- **Content**: H2 + paragraph + `<ul>` bullet list (3 items)
- **Icon**: allocation-icon.svg

#### Section 8: Self-Service Portal Features
- **Background**: White
- **Layout**: H2 heading + paragraph + icon feature grid (7 features)
- **Each feature**: Icon + description paragraph

#### Section 9: Footer
- **Background**: Dark `#020101`
- **Layout**: 4-column link grid (Products, Add-Ons, Solutions, Company) + logo + social icons
- **Footer logo**: White version (`kibo-footer-logo.png`)
- **Social links**: X/Twitter, YouTube, LinkedIn, Email
- **Legal bar**: Copyright 2026 + GDPR, Privacy, Slavery Statement, FCAC, Accessibility, Sitemap

---

## 6. Key CSS Patterns

### CTA Buttons
```css
.cta-button {
  background-color: #FFCE01;
  color: #2B2B2B;
  border-radius: 60px;           /* Fully rounded pill shape */
  padding: 10px 35px;            /* Standard body CTA */
  /* OR padding: 9px 21px;       /* Nav CTA (smaller) */
  font-size: 15px;               /* Body CTA */
  /* OR font-size: 14px;         /* Nav CTA */
  font-weight: 500;
  border: none;
  text-decoration: none;
  font-family: "Poppins", sans-serif;
  cursor: pointer;
}
```

### Section Spacing
- **WP block gap**: `24px` (CSS variable `--wp--style--block-gap`)
- **Content width**: `800px` (CSS variable `--wp--style--global--content-size`)
- **Wide width**: `1200px` (CSS variable `--wp--style--global--wide-size`)
- **Section padding**: Varies by section; hero has no explicit padding on container
- **H6 margin**: `8px 0px 10px` (form heading)

### Shadows (WP Presets)
```css
--wp--preset--shadow--natural: 6px 6px 9px rgba(0, 0, 0, 0.2);
--wp--preset--shadow--deep: 12px 12px 50px rgba(0, 0, 0, 0.4);
--wp--preset--shadow--sharp: 6px 6px 0px rgba(0, 0, 0, 0.2);
--wp--preset--shadow--crisp: 6px 6px 0px rgb(0, 0, 0);
```

### Border Radius
- **CTA buttons**: `60px` (pill shape)
- **All other elements**: `0px` (no rounding observed on cards, sections, images)

### Font Size Scale (WP Presets)
```css
--wp--preset--font-size--small: 13px;
--wp--preset--font-size--medium: 20px;
--wp--preset--font-size--large: 36px;
--wp--preset--font-size--x-large: 42px;
```

### Spacing Scale (WP Presets)
```css
--wp--preset--spacing--20: 0.44rem;   /* ~7px */
--wp--preset--spacing--30: 0.67rem;   /* ~11px */
--wp--preset--spacing--40: 1rem;      /* 16px */
--wp--preset--spacing--50: 1.5rem;    /* 24px */
--wp--preset--spacing--60: 2.25rem;   /* 36px */
--wp--preset--spacing--70: 3.38rem;   /* 54px */
--wp--preset--spacing--80: 5.06rem;   /* 81px */
```

---

## 7. OMS Organic Page Differences

The `/platform/order-management/` page differs from the PPC LP:

| Feature | PPC Wholesale | OMS Organic |
|---|---|---|
| **Navigation** | Stripped (none) | Full mega-menu (Platform, Solutions, Developers, Partners, Company, Resources) |
| **Header height** | N/A | ~90px |
| **Header CTA** | N/A | "Contact Sales" (yellow pill) + "Login" + "Support" |
| **Hero style** | Dark navy bg + form | White bg + large hero image + single CTA |
| **Hero CTA** | Embedded HubSpot form | "Watch the Demo" button linking to `/request-a-demo` |
| **Logo carousel** | 37 logos, image format | 45 logos, SVG format (cleaner) |
| **Stats section** | Animated counters | Not present (replaced by feature cards) |
| **Testimonial** | Single quote block | Not present on OMS page |
| **Pricing section** | Not present | 3-tier packaging table (Starter, Essentials, Advanced) |
| **AI agents section** | Not present | Interactive card grid with popups |
| **Form placement** | Hero right column (above fold) | No embedded form (CTA buttons link to separate pages) |
| **Bottom CTA** | "Speak with an Expert" | Dual CTA: "Watch Demo" + "Talk to Sales" |

---

## 8. Asset URLs for Reuse

### SVG Icons (PPC Wholesale Page)
```
https://kibocommerce.com/wp-content/uploads/2025/02/yellow-triangle-sm.svg
https://kibocommerce.com/wp-content/uploads/2025/02/custom-segments-icon.svg
https://kibocommerce.com/wp-content/uploads/2025/02/Unify.svg
https://kibocommerce.com/wp-content/uploads/2025/02/Truck.svg
https://kibocommerce.com/wp-content/uploads/2025/02/List-2.svg
https://kibocommerce.com/wp-content/uploads/2025/02/Search.svg
https://kibocommerce.com/wp-content/uploads/2025/02/List.svg
https://kibocommerce.com/wp-content/uploads/2025/02/allocation-icon.svg
https://kibocommerce.com/wp-content/uploads/2025/03/icon-quotation-mark-yellow.svg
```

### OMS Page Hero Image
```
https://kibocommerce.com/wp-content/uploads/2025/12/Group-1546.webp
```

### OMS Page Feature Images
```
https://kibocommerce.com/wp-content/uploads/2026/01/Group-1643.png  (Commerce + OMS concept)
```

---

## 9. Platform Details

- **CMS**: WordPress 6.9.4 + Elementor 3.35.7 + Hello Elementor theme 3.4.7
- **Page builder**: Elementor (sections, widgets, popups)
- **Carousel**: Swiper v8.4.5 (via Elementor Image Carousel widget)
- **Performance**: PerfMatters plugin (CSS combining, minification)
- **Popups**: Popup Maker plugin
- **Caching**: PerfMatters cache layer
