"""
Query current quality scores for Kibo Commerce keywords
and compare with historical Oct-Dec data for pre/post analysis
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from google.ads.googleads.client import GoogleAdsClient
import csv

CUSTOMER_ID = '9948697111'
YAML_PATH = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

def query_current_quality_scores():
    """Query current quality scores for all enabled NonBrand keywords"""
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    ga_service = client.get_service("GoogleAdsService")

    # Query current QS + recent metrics
    query = '''
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.criterion_id,
        ad_group_criterion.final_urls,
        ad_group_criterion.status,
        ad_group_criterion.quality_info.quality_score,
        ad_group_criterion.quality_info.creative_quality_score,
        ad_group_criterion.quality_info.post_click_quality_score,
        ad_group_criterion.quality_info.search_predicted_ctr,
        ad_group.name,
        campaign.name,
        campaign.status
    FROM ad_group_criterion
    WHERE campaign.name = 'Search - NonBrand'
        AND ad_group_criterion.type = 'KEYWORD'
        AND ad_group_criterion.status != 'REMOVED'
    ORDER BY ad_group.name, ad_group_criterion.keyword.text
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    keywords = []
    for row in response:
        criterion = row.ad_group_criterion
        qi = criterion.quality_info

        kw = {
            'keyword': criterion.keyword.text,
            'match_type': criterion.keyword.match_type.name,
            'criterion_id': criterion.criterion_id,
            'final_urls': list(criterion.final_urls) if criterion.final_urls else [],
            'status': criterion.status.name,
            'quality_score': qi.quality_score if qi.quality_score else None,
            'ad_relevance': qi.creative_quality_score.name if qi.creative_quality_score else None,
            'landing_page_exp': qi.post_click_quality_score.name if qi.post_click_quality_score else None,
            'expected_ctr': qi.search_predicted_ctr.name if qi.search_predicted_ctr else None,
            'ad_group': row.ad_group.name,
            'campaign': row.campaign.name,
            'campaign_status': row.campaign.status.name,
        }
        keywords.append(kw)

    return keywords


def query_recent_metrics():
    """Query impression/click data for the last 7 days (since campaign was unpaused)"""
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    ga_service = client.get_service("GoogleAdsService")

    query = '''
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.criterion_id,
        ad_group.name,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.ctr,
        metrics.average_cpc,
        segments.date
    FROM keyword_view
    WHERE campaign.name = 'Search - NonBrand'
        AND segments.date DURING LAST_7_DAYS
        AND metrics.impressions > 0
    ORDER BY segments.date DESC, metrics.impressions DESC
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    daily_metrics = []
    for row in response:
        criterion = row.ad_group_criterion
        m = row.metrics
        daily_metrics.append({
            'keyword': criterion.keyword.text,
            'match_type': criterion.keyword.match_type.name,
            'criterion_id': criterion.criterion_id,
            'ad_group': row.ad_group.name,
            'date': row.segments.date,
            'impressions': m.impressions,
            'clicks': m.clicks,
            'cost': m.cost_micros / 1_000_000 if m.cost_micros else 0,
            'ctr': m.ctr,
            'avg_cpc': m.average_cpc / 1_000_000 if m.average_cpc else 0,
        })

    return daily_metrics


def load_historical_qs():
    """Load historical Oct-Dec QS data"""
    historical = {}
    filepath = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/Kibocommerce_Oct - Dec_KW QS Data.csv'

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean keyword - remove brackets
            keyword = row['Keyword'].strip('[]')
            ad_group = row['Ad group']

            # Parse impressions (remove commas)
            impr_str = row['Impr.'].replace(',', '')
            impressions = int(impr_str) if impr_str else 0

            historical[(keyword.lower(), ad_group)] = {
                'keyword': keyword,
                'ad_group': ad_group,
                'quality_score': int(row['Quality Score (hist.)']) if row['Quality Score (hist.)'] else None,
                'expected_ctr': row['Exp. CTR (hist.)'],
                'landing_page_exp': row['Landing page exp. (hist.)'],
                'ad_relevance': row['Ad relevance (hist.)'],
                'impressions': impressions,
                'clicks': int(row['Clicks']) if row['Clicks'] else 0,
                'cost': float(row['Cost'].replace(',', '')) if row['Cost'] else 0,
            }

    return historical


if __name__ == '__main__':
    print("=" * 70)
    print("KIBO COMMERCE - QUALITY SCORE PRE/POST ANALYSIS")
    print("=" * 70)

    # 1. Load historical QS data
    print("\n--- Loading Historical QS Data (Oct-Dec) ---")
    historical = load_historical_qs()
    print(f"  Loaded {len(historical)} historical keyword records")

    # 2. Query current quality scores
    print("\n--- Querying Current Quality Scores ---")
    current_keywords = query_current_quality_scores()
    print(f"  Retrieved {len(current_keywords)} total keywords")

    # Filter to enabled keywords with QS
    with_qs = [k for k in current_keywords if k['quality_score'] is not None]
    enabled = [k for k in current_keywords if k['status'] == 'ENABLED']
    enabled_with_qs = [k for k in with_qs if k['status'] == 'ENABLED']
    print(f"  Enabled keywords: {len(enabled)}")
    print(f"  Keywords with current QS: {len(with_qs)}")
    print(f"  Enabled keywords with current QS: {len(enabled_with_qs)}")

    # 3. Query recent metrics (last 7 days)
    print("\n--- Querying Recent Metrics (Last 7 Days) ---")
    recent_metrics = query_recent_metrics()
    print(f"  Retrieved {len(recent_metrics)} daily metric records")

    # Aggregate recent metrics by keyword
    recent_agg = {}
    for m in recent_metrics:
        key = (m['keyword'].lower(), m['ad_group'])
        if key not in recent_agg:
            recent_agg[key] = {'impressions': 0, 'clicks': 0, 'cost': 0, 'dates': set()}
        recent_agg[key]['impressions'] += m['impressions']
        recent_agg[key]['clicks'] += m['clicks']
        recent_agg[key]['cost'] += m['cost']
        recent_agg[key]['dates'].add(m['date'])

    # Get unique active dates
    all_dates = set()
    for m in recent_metrics:
        all_dates.add(m['date'])

    print(f"  Unique keywords with impressions: {len(recent_agg)}")
    print(f"  Date range: {min(all_dates) if all_dates else 'N/A'} to {max(all_dates) if all_dates else 'N/A'}")
    print(f"  Days with data: {len(all_dates)}")

    # 4. Build comparison dataset
    print("\n" + "=" * 70)
    print("PRE/POST QUALITY SCORE COMPARISON")
    print("=" * 70)

    # Save detailed comparison to CSV
    output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/quality_score_pre_post.csv'

    comparison_rows = []

    for kw in enabled_with_qs:
        key = (kw['keyword'].lower(), kw['ad_group'])
        hist = historical.get(key, None)
        recent = recent_agg.get(key, None)

        row = {
            'keyword': kw['keyword'],
            'match_type': kw['match_type'],
            'ad_group': kw['ad_group'],
            'has_keyword_url': 'Yes' if kw['final_urls'] else 'No',
            'final_url': kw['final_urls'][0] if kw['final_urls'] else '',
            'current_qs': kw['quality_score'],
            'current_landing_page_exp': kw['landing_page_exp'],
            'current_ad_relevance': kw['ad_relevance'],
            'current_expected_ctr': kw['expected_ctr'],
            'historical_qs': hist['quality_score'] if hist else 'N/A (new)',
            'historical_landing_page_exp': hist['landing_page_exp'] if hist else 'N/A',
            'historical_ad_relevance': hist['ad_relevance'] if hist else 'N/A',
            'historical_expected_ctr': hist['expected_ctr'] if hist else 'N/A',
            'historical_impressions': hist['impressions'] if hist else 0,
            'recent_impressions': recent['impressions'] if recent else 0,
            'recent_clicks': recent['clicks'] if recent else 0,
            'qs_change': (kw['quality_score'] - hist['quality_score']) if hist and hist['quality_score'] else 'NEW',
        }
        comparison_rows.append(row)

    # Also check for keywords that are NEW (have QS now but didn't historically)
    # These are keywords we added URLs to that now have enough data for QS

    # Sort by recent impressions (highest first)
    comparison_rows.sort(key=lambda x: x['recent_impressions'], reverse=True)

    # Save to CSV
    if comparison_rows:
        fieldnames = list(comparison_rows[0].keys())
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(comparison_rows)
        print(f"\n  Saved {len(comparison_rows)} rows to: {output_file}")

    # 5. Compute impression-weighted QS
    print("\n" + "=" * 70)
    print("IMPRESSION-WEIGHTED QUALITY SCORE ANALYSIS")
    print("=" * 70)

    # Historical impression-weighted QS (using Oct-Dec data)
    hist_total_impr = 0
    hist_weighted_qs = 0
    hist_count = 0

    for key, hist in historical.items():
        if hist['quality_score'] and hist['impressions'] > 0:
            hist_weighted_qs += hist['quality_score'] * hist['impressions']
            hist_total_impr += hist['impressions']
            hist_count += 1

    hist_avg_weighted_qs = hist_weighted_qs / hist_total_impr if hist_total_impr > 0 else 0
    hist_simple_avg = sum(h['quality_score'] for h in historical.values() if h['quality_score']) / len([h for h in historical.values() if h['quality_score']]) if historical else 0

    print(f"\n  HISTORICAL (Oct-Dec):")
    print(f"    Keywords with QS: {hist_count}")
    print(f"    Total Impressions: {hist_total_impr:,}")
    print(f"    Simple Average QS: {hist_simple_avg:.2f}")
    print(f"    Impression-Weighted QS: {hist_avg_weighted_qs:.2f}")

    # Current impression-weighted QS (using recent metrics)
    curr_total_impr = 0
    curr_weighted_qs = 0
    curr_count = 0

    for row in comparison_rows:
        if row['current_qs'] and row['recent_impressions'] > 0:
            curr_weighted_qs += row['current_qs'] * row['recent_impressions']
            curr_total_impr += row['recent_impressions']
            curr_count += 1

    curr_avg_weighted_qs = curr_weighted_qs / curr_total_impr if curr_total_impr > 0 else 0
    curr_simple_avg = sum(r['current_qs'] for r in comparison_rows if r['current_qs']) / len([r for r in comparison_rows if r['current_qs']]) if comparison_rows else 0

    print(f"\n  CURRENT (Post URL Changes):")
    print(f"    Keywords with QS: {curr_count}")
    print(f"    Total Impressions (last 7d): {curr_total_impr:,}")
    print(f"    Simple Average QS: {curr_simple_avg:.2f}")
    print(f"    Impression-Weighted QS: {curr_avg_weighted_qs:.2f}")

    print(f"\n  CHANGE:")
    print(f"    Impression-Weighted QS: {hist_avg_weighted_qs:.2f} -> {curr_avg_weighted_qs:.2f} ({curr_avg_weighted_qs - hist_avg_weighted_qs:+.2f})")
    print(f"    Simple Average QS: {hist_simple_avg:.2f} -> {curr_simple_avg:.2f} ({curr_simple_avg - hist_simple_avg:+.2f})")

    # 6. Breakdown by sub-component
    print("\n" + "=" * 70)
    print("QS SUB-COMPONENT ANALYSIS")
    print("=" * 70)

    # Count sub-component ratings
    hist_lp = {'Below average': 0, 'Average': 0, 'Above average': 0}
    curr_lp = {'BELOW_AVERAGE': 0, 'AVERAGE': 0, 'ABOVE_AVERAGE': 0}
    hist_ctr = {'Below average': 0, 'Average': 0, 'Above average': 0}
    curr_ctr = {'BELOW_AVERAGE': 0, 'AVERAGE': 0, 'ABOVE_AVERAGE': 0}
    hist_ar = {'Below average': 0, 'Average': 0, 'Above average': 0}
    curr_ar = {'BELOW_AVERAGE': 0, 'AVERAGE': 0, 'ABOVE_AVERAGE': 0}

    for hist in historical.values():
        if hist['landing_page_exp'] in hist_lp:
            hist_lp[hist['landing_page_exp']] += 1
        if hist['expected_ctr'] in hist_ctr:
            hist_ctr[hist['expected_ctr']] += 1
        if hist['ad_relevance'] in hist_ar:
            hist_ar[hist['ad_relevance']] += 1

    for row in comparison_rows:
        if row['current_landing_page_exp'] in curr_lp:
            curr_lp[row['current_landing_page_exp']] += 1
        if row['current_expected_ctr'] in curr_ctr:
            curr_ctr[row['current_expected_ctr']] += 1
        if row['current_ad_relevance'] in curr_ar:
            curr_ar[row['current_ad_relevance']] += 1

    print(f"\n  Landing Page Experience:")
    print(f"    Historical:  Below Avg: {hist_lp['Below average']}, Average: {hist_lp['Average']}, Above Avg: {hist_lp['Above average']}")
    print(f"    Current:     Below Avg: {curr_lp['BELOW_AVERAGE']}, Average: {curr_lp['AVERAGE']}, Above Avg: {curr_lp['ABOVE_AVERAGE']}")

    print(f"\n  Expected CTR:")
    print(f"    Historical:  Below Avg: {hist_ctr['Below average']}, Average: {hist_ctr['Average']}, Above Avg: {hist_ctr['Above average']}")
    print(f"    Current:     Below Avg: {curr_ctr['BELOW_AVERAGE']}, Average: {curr_ctr['AVERAGE']}, Above Avg: {curr_ctr['ABOVE_AVERAGE']}")

    print(f"\n  Ad Relevance:")
    print(f"    Historical:  Below Avg: {hist_ar['Below average']}, Average: {hist_ar['Average']}, Above Avg: {hist_ar['Above average']}")
    print(f"    Current:     Below Avg: {curr_ar['BELOW_AVERAGE']}, Average: {curr_ar['AVERAGE']}, Above Avg: {curr_ar['ABOVE_AVERAGE']}")

    # 7. Problem keywords - still at QS <= 5 with landing page issues
    print("\n" + "=" * 70)
    print("PROBLEM KEYWORDS (QS <= 5, Landing Page Issues)")
    print("=" * 70)

    problem_keywords = [r for r in comparison_rows
                       if r['current_qs'] and r['current_qs'] <= 5
                       and r['current_landing_page_exp'] in ('BELOW_AVERAGE', 'AVERAGE')]

    # Group by landing page URL
    lp_groups = {}
    for kw in problem_keywords:
        url = kw['final_url'] or 'No keyword-level URL'
        if url not in lp_groups:
            lp_groups[url] = []
        lp_groups[url].append(kw)

    print(f"\n  Total problem keywords: {len(problem_keywords)}")
    print(f"  Unique landing pages affected: {len(lp_groups)}")

    for url, kws in sorted(lp_groups.items(), key=lambda x: -sum(k['recent_impressions'] for k in x[1])):
        total_impr = sum(k['recent_impressions'] for k in kws)
        avg_qs = sum(k['current_qs'] for k in kws) / len(kws) if kws else 0
        print(f"\n  URL: {url}")
        print(f"    Keywords: {len(kws)} | Total Impressions: {total_impr:,} | Avg QS: {avg_qs:.1f}")
        for kw in sorted(kws, key=lambda x: -x['recent_impressions'])[:5]:
            lp_status = kw['current_landing_page_exp']
            print(f"      [{kw['keyword']}] QS={kw['current_qs']} | LP={lp_status} | Impr={kw['recent_impressions']:,}")

    # Save problem keywords
    problem_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/problem_keywords_landing_page.csv'
    if problem_keywords:
        with open(problem_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(problem_keywords[0].keys()))
            writer.writeheader()
            writer.writerows(problem_keywords)
        print(f"\n  Saved problem keywords to: {problem_file}")

    # 8. Per-keyword detail
    print("\n" + "=" * 70)
    print("DETAILED KEYWORD-LEVEL COMPARISON")
    print("=" * 70)
    print(f"\n  {'Keyword':<45} {'AG':<18} {'Hist QS':>7} {'Curr QS':>7} {'Change':>7} {'Hist LP':>16} {'Curr LP':>16} {'Has URL':>8} {'Impr':>6}")
    print("  " + "-" * 140)

    for row in comparison_rows:
        hist_qs_str = str(row['historical_qs']) if row['historical_qs'] != 'N/A (new)' else 'NEW'
        change_str = str(row['qs_change']) if row['qs_change'] != 'NEW' else 'NEW'

        # Shorten LP experience names
        curr_lp_short = str(row['current_landing_page_exp']).replace('BELOW_AVERAGE', 'Below Avg').replace('ABOVE_AVERAGE', 'Above Avg').replace('AVERAGE', 'Average')
        hist_lp_short = str(row['historical_landing_page_exp']).replace('Below average', 'Below Avg').replace('Above average', 'Above Avg')

        print(f"  {row['keyword']:<45} {row['ad_group']:<18} {hist_qs_str:>7} {row['current_qs']:>7} {change_str:>7} {hist_lp_short:>16} {curr_lp_short:>16} {row['has_keyword_url']:>8} {row['recent_impressions']:>6}")
