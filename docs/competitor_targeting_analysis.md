# Competitor Targeting Custom Segment Strategy - Analysis

## User Question
> For the custom segment for competitor targeting, where would this be layered on? Are you suggesting a separate competitor campaign? If so, what page would this drive to, and is it advisable given their current impression share, IS lost to budget, and CPAs?

---

## Current Campaign Performance (Last 30 Days)

| Metric | Value | Assessment |
|--------|-------|------------|
| **Search Impression Share** | 60.7% | Moderate coverage |
| **IS Lost to Budget** | 23.3% | **SIGNIFICANT** - Budget-constrained |
| **IS Lost to Rank** | 16.0% | Some rank/quality issues |
| **Top IS** | 46.2% | Below ideal |
| **Abs Top IS** | 30.2% | Below ideal |
| **Impressions** | 4,963 | Low volume |
| **Clicks** | 218 | |
| **Conversions** | 6.0 | Very low volume |
| **CPA** | $1,985 | High (typical for enterprise B2B) |
| **Cost** | $11,911 | |

---

## Strategic Recommendation

### **NOT RECOMMENDED at this time**

A separate competitor targeting campaign is **not advisable** given current metrics:

1. **23.3% IS Lost to Budget** indicates the current NonBrand campaign is already budget-constrained. Adding competitor targeting would:
   - Spread budget thinner across more campaigns
   - Potentially cannibalize existing NonBrand performance
   - Divert spend from proven converting queries

2. **Competitor terms typically have:**
   - Lower Quality Scores (user searched for competitor, not Kibo)
   - Higher CPCs (competitive auctions)
   - Lower conversion rates (users may prefer the competitor)
   - Higher CPAs than non-brand terms

3. **Only 6 conversions/month** means limited data for optimization
   - Adding a competitor campaign would further fragment conversion data
   - Makes statistical significance harder to achieve

---

## Recommended Sequencing

### Phase 1: Maximize NonBrand First (Current Priority)
1. **Increase NonBrand budget** to capture the 23% IS lost to budget
2. **Optimize for rank** to reduce the 16% IS lost to rank
3. Goal: Get Search IS to 80%+ before expansion

### Phase 2: Consider Competitor Targeting (Future)
Only after:
- IS Lost to Budget < 10%
- Monthly conversions > 15-20 (for statistical power)
- Clear budget allocation for incremental testing

---

## If/When Competitor Targeting Proceeds

### Structure: Separate Campaign (Required)
**Reason:** Different intent profile requires:
- Separate budget control
- Different CPAs/ROAS targets
- Independent performance measurement
- Ability to pause without affecting core NonBrand

### Available Custom Segments
| Segment ID | Name | Use Case |
|------------|------|----------|
| 877695143 | OMS Competitor - Keywords | Users searching competitor OMS terms |
| 878722257 | OMS Competitor - URLs | Users browsing competitor OMS sites |
| 615222237 | Pipeline Audience: Competitive Keywords | Competitive keyword signals |

### Landing Page Strategy
**Option A: Comparison Pages (Best Practice)**
- `/compare/kibo-vs-[competitor]/`
- Directly addresses competitor comparison intent
- Requires dedicated landing page development

**Option B: Existing /why-kibo/ Page**
- If comparison pages don't exist
- Add competitor comparison content section
- Track with UTM: `?utm_campaign=competitor&utm_term=[competitor-name]`

**Option C: Vertical Solution Pages with Comparison Messaging**
- Use existing `/ppc/manufacturing/`, `/ppc/wholesale/`, etc.
- Ensure page has competitive differentiation content

### Targeting Mode
- Custom segments should be used as **TARGETING** (not observation)
- This restricts ads to only show to users in those segments
- Higher relevance, smaller audience, more efficient spend

---

## Alternative: Observation Mode Testing

If wanting to test competitor signals without a separate campaign:

1. Add custom segments at **campaign level** in **OBSERVATION mode**
2. This gathers data on how competitor-researching users perform
3. After 60-90 days, analyze:
   - Do these audiences convert?
   - At what CPA?
   - Worth scaling?

**Limitation:** Custom segments cannot be added at ad group level for Search campaigns (API restriction discovered during audience optimization work).

---

## Summary

| Question | Answer |
|----------|--------|
| Where to layer? | **Separate campaign** (if proceeding) or **campaign-level observation** (for testing) |
| Separate campaign? | **Yes, required** - different intent profile, budget control |
| Landing page? | Competitor comparison pages or /why-kibo/ with comparison content |
| Is it advisable now? | **NO** - 23% IS lost to budget means current campaign is constrained; fix that first |

---

## Related Files
- `query_campaign_metrics.py` - Script to pull IS, budget loss, CPA metrics

---

*Analysis Date: January 2026*
