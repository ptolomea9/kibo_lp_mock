"""
Query Campaign Performance Metrics for Strategic Analysis

Pulls impression share, IS lost to budget/rank, CPAs, and conversion data
to inform competitor targeting strategy decisions.
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
from datetime import datetime

CUSTOMER_ID = '9948697111'

def get_campaign_metrics():
    """Get key performance metrics for Search - NonBrand"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        campaign.name,
        campaign.status,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value,
        metrics.search_impression_share,
        metrics.search_budget_lost_impression_share,
        metrics.search_rank_lost_impression_share,
        metrics.search_top_impression_share,
        metrics.search_absolute_top_impression_share
    FROM campaign
    WHERE campaign.name = 'Search - NonBrand'
    AND segments.date DURING LAST_30_DAYS
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    totals = {
        'impressions': 0,
        'clicks': 0,
        'cost': 0,
        'conversions': 0,
        'conv_value': 0,
        'is_share': [],
        'is_lost_budget': [],
        'is_lost_rank': [],
        'top_is': [],
        'abs_top_is': []
    }

    for row in response:
        m = row.metrics
        totals['impressions'] += m.impressions
        totals['clicks'] += m.clicks
        totals['cost'] += m.cost_micros / 1_000_000
        totals['conversions'] += m.conversions
        totals['conv_value'] += m.conversions_value

        if m.search_impression_share:
            totals['is_share'].append(m.search_impression_share)
        if m.search_budget_lost_impression_share:
            totals['is_lost_budget'].append(m.search_budget_lost_impression_share)
        if m.search_rank_lost_impression_share:
            totals['is_lost_rank'].append(m.search_rank_lost_impression_share)
        if m.search_top_impression_share:
            totals['top_is'].append(m.search_top_impression_share)
        if m.search_absolute_top_impression_share:
            totals['abs_top_is'].append(m.search_absolute_top_impression_share)

    return totals

def get_ad_group_metrics():
    """Get metrics by ad group"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.search_impression_share,
        metrics.search_budget_lost_impression_share,
        metrics.search_rank_lost_impression_share
    FROM ad_group
    WHERE campaign.name = 'Search - NonBrand'
    AND ad_group.status = 'ENABLED'
    AND segments.date DURING LAST_30_DAYS
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    ad_groups = {}
    for row in response:
        ag_name = row.ad_group.name
        m = row.metrics

        if ag_name not in ad_groups:
            ad_groups[ag_name] = {
                'impressions': 0,
                'clicks': 0,
                'cost': 0,
                'conversions': 0,
                'is_share': [],
                'is_lost_budget': [],
                'is_lost_rank': []
            }

        ad_groups[ag_name]['impressions'] += m.impressions
        ad_groups[ag_name]['clicks'] += m.clicks
        ad_groups[ag_name]['cost'] += m.cost_micros / 1_000_000
        ad_groups[ag_name]['conversions'] += m.conversions

        if m.search_impression_share:
            ad_groups[ag_name]['is_share'].append(m.search_impression_share)
        if m.search_budget_lost_impression_share:
            ad_groups[ag_name]['is_lost_budget'].append(m.search_budget_lost_impression_share)
        if m.search_rank_lost_impression_share:
            ad_groups[ag_name]['is_lost_rank'].append(m.search_rank_lost_impression_share)

    return ad_groups

if __name__ == '__main__':
    print("=" * 80)
    print("Campaign Performance Analysis: Search - NonBrand")
    print(f"Period: Last 30 Days | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    # Campaign-level metrics
    print("\n" + "=" * 80)
    print("CAMPAIGN-LEVEL METRICS")
    print("=" * 80)

    metrics = get_campaign_metrics()

    # Calculate averages for IS metrics
    avg_is = sum(metrics['is_share']) / len(metrics['is_share']) if metrics['is_share'] else 0
    avg_is_lost_budget = sum(metrics['is_lost_budget']) / len(metrics['is_lost_budget']) if metrics['is_lost_budget'] else 0
    avg_is_lost_rank = sum(metrics['is_lost_rank']) / len(metrics['is_lost_rank']) if metrics['is_lost_rank'] else 0
    avg_top_is = sum(metrics['top_is']) / len(metrics['top_is']) if metrics['top_is'] else 0
    avg_abs_top_is = sum(metrics['abs_top_is']) / len(metrics['abs_top_is']) if metrics['abs_top_is'] else 0

    ctr = (metrics['clicks'] / metrics['impressions'] * 100) if metrics['impressions'] else 0
    cpc = (metrics['cost'] / metrics['clicks']) if metrics['clicks'] else 0
    cpa = (metrics['cost'] / metrics['conversions']) if metrics['conversions'] else 0
    conv_rate = (metrics['conversions'] / metrics['clicks'] * 100) if metrics['clicks'] else 0
    roas = (metrics['conv_value'] / metrics['cost']) if metrics['cost'] else 0

    print(f"""
VOLUME METRICS:
  Impressions:     {metrics['impressions']:,}
  Clicks:          {metrics['clicks']:,}
  Cost:            ${metrics['cost']:,.2f}
  Conversions:     {metrics['conversions']:.1f}
  Conv Value:      ${metrics['conv_value']:,.2f}

EFFICIENCY METRICS:
  CTR:             {ctr:.2f}%
  Avg CPC:         ${cpc:.2f}
  CPA:             ${cpa:.2f}
  Conv Rate:       {conv_rate:.2f}%
  ROAS:            {roas:.2f}x

IMPRESSION SHARE METRICS:
  Search IS:              {avg_is*100:.1f}%
  IS Lost (Budget):       {avg_is_lost_budget*100:.1f}%
  IS Lost (Rank):         {avg_is_lost_rank*100:.1f}%
  Top IS:                 {avg_top_is*100:.1f}%
  Abs Top IS:             {avg_abs_top_is*100:.1f}%
""")

    # Ad group-level metrics
    print("=" * 80)
    print("AD GROUP-LEVEL METRICS")
    print("=" * 80)

    ad_groups = get_ad_group_metrics()

    for ag_name, data in sorted(ad_groups.items(), key=lambda x: x[1]['cost'], reverse=True):
        ag_ctr = (data['clicks'] / data['impressions'] * 100) if data['impressions'] else 0
        ag_cpc = (data['cost'] / data['clicks']) if data['clicks'] else 0
        ag_cpa = (data['cost'] / data['conversions']) if data['conversions'] else 0

        ag_is = sum(data['is_share']) / len(data['is_share']) * 100 if data['is_share'] else 0
        ag_is_budget = sum(data['is_lost_budget']) / len(data['is_lost_budget']) * 100 if data['is_lost_budget'] else 0
        ag_is_rank = sum(data['is_lost_rank']) / len(data['is_lost_rank']) * 100 if data['is_lost_rank'] else 0

        cpa_str = f"${ag_cpa:.2f}" if data['conversions'] else "N/A"

        print(f"""
  {ag_name}
    Impr: {data['impressions']:,} | Clicks: {data['clicks']:,} | Cost: ${data['cost']:,.2f}
    CTR: {ag_ctr:.2f}% | CPC: ${ag_cpc:.2f} | Conv: {data['conversions']:.1f} | CPA: {cpa_str}
    Search IS: {ag_is:.1f}% | IS Lost Budget: {ag_is_budget:.1f}% | IS Lost Rank: {ag_is_rank:.1f}%
""")

    # Strategic analysis
    print("=" * 80)
    print("STRATEGIC ANALYSIS")
    print("=" * 80)

    # Determine budget constraint level
    budget_constraint = "LOW" if avg_is_lost_budget < 0.10 else "MODERATE" if avg_is_lost_budget < 0.25 else "HIGH"
    rank_issue = "LOW" if avg_is_lost_rank < 0.15 else "MODERATE" if avg_is_lost_rank < 0.30 else "HIGH"

    print(f"""
CURRENT STATE ASSESSMENT:

  Budget Constraint Level: {budget_constraint}
    - {avg_is_lost_budget*100:.1f}% IS lost to budget
    - {"Room to scale" if budget_constraint == "LOW" else "May need budget increase before expansion" if budget_constraint == "MODERATE" else "Budget-limited - expansion not recommended"}

  Rank/Quality Issue Level: {rank_issue}
    - {avg_is_lost_rank*100:.1f}% IS lost to rank
    - {"Good ad rank" if rank_issue == "LOW" else "Some rank optimization needed" if rank_issue == "MODERATE" else "Significant rank issues - focus on quality before expansion"}

  Overall Impression Share: {avg_is*100:.1f}%
    - {"Strong coverage" if avg_is > 0.60 else "Moderate coverage - room to grow" if avg_is > 0.35 else "Low coverage - significant growth opportunity"}

COMPETITOR CAMPAIGN RECOMMENDATION:

  Based on current metrics:
""")

    if avg_is_lost_budget > 0.20:
        print("""    NOT RECOMMENDED at this time

    Reason: {:.1f}% IS lost to budget indicates the current campaign is already
    budget-constrained. Adding competitor targeting would spread budget thinner
    and potentially cannibalize existing NonBrand performance.

    Recommended action: Increase NonBrand budget first, then consider expansion.""".format(avg_is_lost_budget*100))
    elif avg_is_lost_rank > 0.25:
        print("""    PROCEED WITH CAUTION

    Reason: {:.1f}% IS lost to rank suggests quality/bid optimization needed.
    Competitor terms typically have lower Quality Scores (users searching for
    specific competitors may not find your ad relevant), which could worsen
    rank issues.

    Recommended action: Optimize current campaign QS first, then test competitor
    targeting with small budget in separate campaign.""".format(avg_is_lost_rank*100))
    else:
        print("""    VIABLE OPTION

    Current IS metrics suggest room for expansion:
    - IS Lost Budget: {:.1f}% (acceptable)
    - IS Lost Rank: {:.1f}% (acceptable)

    A separate competitor campaign is advisable because:
    1. Competitor terms have different intent/QS profiles
    2. Separate budget control prevents cannibalization
    3. Easier to measure incremental value
    4. Can pause without affecting core NonBrand""".format(avg_is_lost_budget*100, avg_is_lost_rank*100))

    print("""
CUSTOM SEGMENT STRATEGY:

  Available competitor-focused segments:
    - OMS Competitor - Keywords (ID: 877695143)
    - OMS Competitor - URLs (ID: 878722257)
    - Pipeline Audience: Competitive Keywords (ID: 615222237)

  Where to layer:
    Option A: New "Search - Competitor" campaign (RECOMMENDED)
      - Dedicated budget
      - Competitor-specific ad copy
      - Competitor comparison landing pages
      - Custom segments as TARGETING (not observation)

    Option B: Add to NonBrand as observation layer
      - Uses custom segments for bid signals only
      - Note: Custom segments can be added at CAMPAIGN level
      - No reach restriction, just bid adjustments

  Landing Page Strategy:
    - Dedicated competitor comparison pages work best
    - E.g., /compare/kibo-vs-[competitor]/
    - Or /why-kibo/ with competitor comparison content
    - Alternative: Use existing solution pages with ?utm tracking
""")

    print("=" * 80)
