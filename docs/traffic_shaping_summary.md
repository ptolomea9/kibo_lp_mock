# Traffic Shaping Analysis Summary - Kibo Commerce NonBrand

## Analysis Period: Last 60 Days

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total NonBrand Search Terms | 1,150 |
| Correctly Routed (by intent) | 737 (64.1%) |
| Correctly Routed (by negatives) | 5 (0.4%) |
| Potential Mismatches | 172 (15.0%) |
| No Clear Intent | 236 (20.5%) |
| **Items Needing Review** | **28 ($2,625 spend)** |

---

## Current Traffic Shaping Structure

| Ad Group | Negatives | Purpose |
|----------|-----------|---------|
| OMS | 644 | Highly curated - blocks competitor brands, off-topic terms |
| B2B EComm | 11 | Blocks: marketplace, b2c, cart terms |
| B2C EComm | 9 | Blocks: b2b, developer terms |
| NB - General B2B | 7 | Blocks: fulfillment, oms, inventory, order management |
| Agentic Commerce | 7 | Blocks: competitor/off-topic terms |
| B2B Other Keywords | 2 | Blocks: b2c, competitor |

**Key Insight**: NB - General B2B has negatives blocking OMS terms, which routes "b2b order management" etc. to OMS correctly.

---

## Identified Issues by Category

### 1. B2B EComm Terms in Wrong Ad Group (~$1,054 spend)

These terms have "b2b ecommerce" intent but are routing to NB - General B2B instead of B2B EComm:

| Search Term | Cost | Clicks | Conv |
|-------------|------|--------|------|
| b2b ecommerce | $564.44 | 12 | 1.0 |
| b2b ecommerce platforms | $113.12 | 1 | 0 |
| b2b ecommerce services | $78.55 | 1 | 0 |
| b2b ecommerce world | $78.50 | 1 | 0 |
| b2b ecommerce solutions | $68.74 | 1 | 0 |
| top 10 b2b ecommerce platforms | $53.91 | 1 | 0 |
| top b2b ecommerce platforms | $13.88 | 1 | 0 |

**Root Cause**: B2B EComm ad group likely missing keywords for these terms, OR NB - General B2B is winning the auction with broader match.

**Recommendation**:
- Check B2B EComm keywords - ensure "b2b ecommerce" variants are present
- Consider adding phrase match negatives to NB - General B2B to force routing

---

### 2. OMS Terms Routing to Industry Verticals (~$970 spend)

Terms with clear OMS intent are going to NB - Wholesalers/Distributors instead of OMS:

| Search Term | Current AG | Cost | Clicks |
|-------------|------------|------|--------|
| wholesale order management system | NB - Wholesalers | $211.38 | 1 |
| distributed order management systems | NB - Distributors | $177.89 | 1 |
| vendor managed inventory software | NB - Wholesalers | $145.62 | 1 |
| wholesale order management | NB - Wholesalers | $112.24 | 1 |
| wholesale inventory management software | NB - Wholesalers | $91.30 | 1 |
| vendor management inventory system | NB - Wholesalers | $43.00 | 1 |
| vendor owned inventory management | NB - Wholesalers | $38.40 | 1 |

**Question for Review**: Is this intentional?
- If Kibo wants industry-specific messaging for wholesale OMS terms → Current routing is correct
- If OMS ad group has better landing pages/messaging → Add negatives to route to OMS

**Recommendation**: If OMS ad group is the primary conversion driver, add these as phrase negatives to industry verticals:
- `[order management]` → negative in NB - Wholesalers, NB - Distributors
- `[inventory management]` → negative in NB - Wholesalers, NB - Distributors

---

### 3. Unified Commerce Terms Not Reaching B2B Other Keywords (~$157 spend)

| Search Term | Current AG | Expected | Cost |
|-------------|------------|----------|------|
| unified commerce platform | NB - General B2B | B2B Other Keywords | $95.80 |
| unified commerce | NB - General B2B | B2B Other Keywords | $61.40 |

**Recommendation**: Add "unified commerce" as a phrase negative to NB - General B2B to route to B2B Other Keywords.

---

### 4. Wholesale Terms in NB - General B2B (~$62 spend)

| Search Term | Current AG | Expected | Cost |
|-------------|------------|----------|------|
| top b2b wholesale websites | NB - General B2B | NB - Wholesalers | $44.97 |
| b2b wholesale marketplace | NB - General B2B | NB - Wholesalers | $16.80 |

**Recommendation**: Add "wholesale" as phrase negative to NB - General B2B.

---

## Ad Group Performance Comparison

| Ad Group | Terms | Clicks | Spend | Conv | CPA |
|----------|-------|--------|-------|------|-----|
| NB - General B2B | 429 | 123 | $5,775 | 3.0 | $1,925 |
| NB - Wholesalers | 260 | 146 | $4,987 | 2.0 | $2,494 |
| OMS | 336 | 53 | $3,879 | 3.0 | $1,293 |
| NB - Distributors | 81 | 13 | $843 | 0.0 | - |
| NB - Manufacturers | 44 | 8 | $676 | 0.0 | - |

**Key Finding**: OMS has the best CPA ($1,293) - routing more inventory/order management terms there may improve efficiency.

---

## Recommended Actions

### HIGH Priority (>$100 potential impact)
1. Add `b2b ecommerce` phrase negative to NB - General B2B → routes to B2B EComm
2. Review OMS vs. Wholesale routing strategy for "order management" terms
3. Add `unified commerce` phrase negative to NB - General B2B

### MEDIUM Priority
4. Add `wholesale` phrase negative to NB - General B2B
5. Review "b2b online marketplaces" routing (currently NB - Wholesalers)

### Optional (Design Decisions)
- Decide if "b2b ordering system/platform" should stay in OMS or move to General B2B
- Confirm industry vertical strategy for OMS-intent terms

---

## Files Generated

| File | Description |
|------|-------------|
| `traffic_routing_analysis.csv` | Full analysis of 1,150 terms with routing status |
| `refined_recommendations.csv` | 28 items needing review with actions |
| `ad_group_negatives.csv` | Current negative keyword structure |
| `search_term_report_60d.csv` | Raw search term data |

---

*Generated by analyze_search_terms_v2.py*
