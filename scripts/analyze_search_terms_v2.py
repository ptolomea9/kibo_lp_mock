"""
Search Term Report Analysis v2 - With Traffic Shaping Context
Analyzes search query reports accounting for intentional cross-ad-group negatives
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
import csv
import re
from collections import defaultdict
from datetime import datetime, timedelta

CUSTOMER_ID = '9948697111'
OUTPUT_DIR = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data'

# Brand detection patterns
BRAND_PATTERNS = [
    r'\bkibo\b',
    r'\bkibocommerce\b',
    r'kibo\s*commerce',
    r'kibo\s*oms',
    r'kibo\s*platform',
]
BRAND_REGEX = re.compile('|'.join(BRAND_PATTERNS), re.IGNORECASE)


def is_brand_term(search_term):
    return bool(BRAND_REGEX.search(search_term))


def get_ad_group_negatives():
    """Pull existing ad group level negatives for traffic shaping analysis"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group.id,
        ad_group.name,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type
    FROM ad_group_criterion
    WHERE campaign.name LIKE '%NonBrand%'
    AND ad_group_criterion.negative = TRUE
    AND ad_group_criterion.type = 'KEYWORD'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    # Group negatives by ad group
    negatives_by_ag = defaultdict(set)
    for row in response:
        ag_name = row.ad_group.name
        kw = row.ad_group_criterion.keyword.text.lower()
        negatives_by_ag[ag_name].add(kw)

    return negatives_by_ag


def pull_search_term_report():
    """Pull search term report for last 60 days"""
    ga_service = get_googleads_service('GoogleAdsService')

    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    query = f'''
    SELECT
        search_term_view.search_term,
        search_term_view.status,
        campaign.id,
        campaign.name,
        ad_group.id,
        ad_group.name,
        segments.keyword.info.text,
        segments.keyword.info.match_type,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value
    FROM search_term_view
    WHERE segments.date BETWEEN '{start_str}' AND '{end_str}'
    AND campaign.advertising_channel_type = 'SEARCH'
    AND metrics.impressions > 0
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    search_terms = []
    for row in response:
        cost = row.metrics.cost_micros / 1_000_000
        clicks = row.metrics.clicks
        impressions = row.metrics.impressions
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (cost / clicks) if clicks > 0 else 0

        search_terms.append({
            'search_term': row.search_term_view.search_term,
            'status': row.search_term_view.status.name if row.search_term_view.status else 'UNKNOWN',
            'campaign_id': row.campaign.id,
            'campaign_name': row.campaign.name,
            'ad_group_id': row.ad_group.id,
            'ad_group_name': row.ad_group.name,
            'keyword_text': row.segments.keyword.info.text if row.segments.keyword.info.text else '',
            'match_type': row.segments.keyword.info.match_type.name if row.segments.keyword.info.match_type else '',
            'impressions': impressions,
            'clicks': clicks,
            'cost': round(cost, 2),
            'conversions': row.metrics.conversions,
            'conversion_value': round(row.metrics.conversions_value, 2),
            'ctr': round(ctr, 2),
            'cpc': round(cpc, 2),
            'is_brand_term': is_brand_term(row.search_term_view.search_term),
        })

    return search_terms


def check_blocked_by_negative(search_term, ad_group_negatives):
    """Check if a search term would be blocked by any negative in an ad group"""
    search_lower = search_term.lower()
    blocked_by = []

    for ag_name, negatives in ad_group_negatives.items():
        for neg in negatives:
            # Check phrase/broad match (negative contains in search term)
            if neg in search_lower:
                blocked_by.append((ag_name, neg))

    return blocked_by


def analyze_traffic_routing(search_terms, ad_group_negatives):
    """
    Analyze where traffic is routing and why.
    Categorizes each term's routing as:
    - CORRECT_BY_INTENT: Term naturally belongs in this ad group
    - CORRECT_BY_NEGATIVE: Term routed here because blocked elsewhere
    - POTENTIAL_MISMATCH: Term might belong elsewhere, review needed

    Priority order for intent detection (highest to lowest):
    1. OMS - order management, fulfillment, inventory terms
    2. Industry verticals - wholesale, distributor, manufacturer
    3. B2C - consumer/d2c terms
    4. B2B Other - composable, headless, unified
    5. Agentic - AI commerce terms
    6. B2B EComm - generic b2b ecommerce/commerce/platform
    7. NB - General B2B - catch-all b2b
    """

    def detect_intent(search_term):
        """Determine expected ad group with priority-based matching"""
        term = search_term.lower()

        # Priority 1: OMS terms (most specific)
        oms_patterns = ['oms', 'order management', 'fulfillment', 'inventory management',
                       'inventory software', 'inventory system', 'warehouse management',
                       'returns management', 'reverse logistics', 'distributed order',
                       'order orchestration', 'ship from store']
        for pattern in oms_patterns:
            if pattern in term:
                return 'OMS'

        # Priority 2: Industry verticals (wholesale, distributor, manufacturer)
        # These take precedence over generic B2B
        if any(w in term for w in ['wholesaler', 'wholesale']):
            return 'NB - Wholesalers'
        if any(w in term for w in ['distributor', 'distribution']):
            return 'NB - Distributors'
        if any(w in term for w in ['manufacturer', 'manufacturing']):
            return 'NB - Manufacturers'

        # Priority 3: B2C/D2C terms
        if any(w in term for w in ['b2c', 'd2c', 'direct to consumer', 'consumer ecommerce']):
            return 'B2C EComm'

        # Priority 4: B2B Other (composable, headless, unified)
        if any(w in term for w in ['unified commerce', 'composable', 'headless', 'mach ']):
            return 'B2B Other Keywords'

        # Priority 5: Agentic Commerce
        if any(w in term for w in ['agentic', 'ai commerce', 'ai-powered commerce']):
            return 'Agentic Commerce'

        # Priority 6: B2B EComm - specific B2B ecommerce terms
        b2b_ecomm_patterns = ['b2b ecommerce', 'b2b e-commerce', 'b2b commerce platform',
                              'b2b ecommerce platform', 'enterprise ecommerce',
                              'business to business ecommerce', 'b2b online store']
        for pattern in b2b_ecomm_patterns:
            if pattern in term:
                return 'B2B EComm'

        # Priority 7: General B2B catch-all
        if 'b2b' in term:
            return 'NB - General B2B'

        # No clear intent
        return None

    # Define ad group themes for intent detection (legacy - kept for reference)
    AD_GROUP_THEMES = {
        'OMS': ['oms', 'order management', 'fulfillment', 'inventory', 'warehouse',
                'returns', 'reverse logistics', 'distributed order'],
        'B2B EComm': ['b2b ecommerce', 'b2b commerce', 'b2b platform', 'enterprise ecommerce',
                     'b2b e-commerce', 'business to business'],
        'B2C EComm': ['b2c', 'd2c', 'direct to consumer', 'consumer ecommerce', 'retail ecommerce'],
        'NB - Manufacturers': ['manufacturer', 'manufacturing ecommerce', 'manufacturing commerce'],
        'NB - Wholesalers': ['wholesaler', 'wholesale platform', 'wholesale ecommerce', 'wholesale'],
        'NB - Distributors': ['distributor', 'distribution platform', 'distribution ecommerce', 'distribution'],
        'B2B Other Keywords': ['unified commerce', 'composable commerce', 'headless commerce',
                              'mach architecture', 'api first'],
        'Agentic Commerce': ['agentic', 'ai commerce', 'ai powered commerce'],
        'NB - General B2B': ['b2b'],  # Catch-all for general B2B terms
    }

    analysis = []

    for term in search_terms:
        if 'nonbrand' not in term['campaign_name'].lower():
            continue
        if term['is_brand_term']:
            continue

        search_lower = term['search_term'].lower()
        actual_ag = term['ad_group_name']

        # Find which ad groups this term is blocked from
        blocked_from = check_blocked_by_negative(term['search_term'], ad_group_negatives)
        blocked_ag_names = [b[0] for b in blocked_from]

        # Determine natural intent using priority-based detection
        natural_intent_ag = detect_intent(term['search_term'])

        if natural_intent_ag == actual_ag:
            routing_status = 'CORRECT_BY_INTENT'
            routing_reason = f'Term matches {actual_ag} theme'
        elif natural_intent_ag and natural_intent_ag in blocked_ag_names:
            routing_status = 'CORRECT_BY_NEGATIVE'
            neg_used = [b[1] for b in blocked_from if b[0] == natural_intent_ag][0]
            routing_reason = f'Blocked from {natural_intent_ag} by negative [{neg_used}]'
        elif natural_intent_ag and natural_intent_ag != actual_ag:
            routing_status = 'POTENTIAL_MISMATCH'
            routing_reason = f'Expected {natural_intent_ag}, but in {actual_ag}'
        else:
            routing_status = 'NO_CLEAR_INTENT'
            routing_reason = 'No strong theme match detected'

        analysis.append({
            **term,
            'routing_status': routing_status,
            'routing_reason': routing_reason,
            'natural_intent': natural_intent_ag or 'UNCLEAR',
            'blocked_from': ', '.join(blocked_ag_names) if blocked_from else '',
        })

    return analysis


def generate_refined_recommendations(analysis):
    """Generate recommendations only for true mismatches"""
    recommendations = []

    for item in analysis:
        if item['routing_status'] == 'POTENTIAL_MISMATCH':
            # Check if it's high-value enough to warrant action
            if item['cost'] >= 10 or item['clicks'] >= 2:
                recommendations.append({
                    'priority': 'REVIEW',
                    'search_term': item['search_term'],
                    'current_ad_group': item['ad_group_name'],
                    'expected_ad_group': item['natural_intent'],
                    'clicks': item['clicks'],
                    'cost': item['cost'],
                    'conversions': item['conversions'],
                    'reason': item['routing_reason'],
                    'action': f'Consider adding to {item["ad_group_name"]} negative list to route to {item["natural_intent"]}',
                })

    recommendations.sort(key=lambda x: -x['cost'])
    return recommendations


def print_traffic_shaping_summary(analysis, ad_group_negatives):
    """Print comprehensive traffic shaping analysis"""

    print("\n" + "=" * 60)
    print("TRAFFIC SHAPING ANALYSIS - Kibo Commerce NonBrand")
    print("=" * 60)

    # Summary of existing negatives
    print("\nEXISTING TRAFFIC SHAPING NEGATIVES")
    print("-" * 40)
    for ag_name, negs in sorted(ad_group_negatives.items()):
        print(f"  {ag_name}: {len(negs)} negatives")

    # Routing status breakdown
    status_counts = defaultdict(int)
    status_spend = defaultdict(float)
    for item in analysis:
        status_counts[item['routing_status']] += 1
        status_spend[item['routing_status']] += item['cost']

    print("\nROUTING STATUS BREAKDOWN")
    print("-" * 40)
    total_terms = sum(status_counts.values())
    for status in ['CORRECT_BY_INTENT', 'CORRECT_BY_NEGATIVE', 'POTENTIAL_MISMATCH', 'NO_CLEAR_INTENT']:
        count = status_counts[status]
        spend = status_spend[status]
        pct = (count / total_terms * 100) if total_terms > 0 else 0
        print(f"  {status}: {count} terms ({pct:.1f}%) - ${spend:,.2f}")

    # Traffic shaping effectiveness
    correctly_shaped = status_counts['CORRECT_BY_NEGATIVE']
    print(f"\n[OK] Traffic shaping is working for {correctly_shaped} search terms")
    print(f"     These terms are correctly blocked from wrong ad groups")

    # Show examples of successful traffic shaping
    shaped_examples = [a for a in analysis if a['routing_status'] == 'CORRECT_BY_NEGATIVE']
    shaped_examples.sort(key=lambda x: -x['cost'])

    if shaped_examples:
        print("\nTOP TRAFFIC SHAPING EXAMPLES (working as intended):")
        print("-" * 40)
        for item in shaped_examples[:10]:
            print(f"  \"{item['search_term']}\"")
            print(f"    -> Routed to: {item['ad_group_name']}")
            print(f"    -> {item['routing_reason']}")
            print(f"    -> ${item['cost']:.2f} spend, {item['clicks']} clicks")
            print()

    # Show potential mismatches
    mismatches = [a for a in analysis if a['routing_status'] == 'POTENTIAL_MISMATCH']
    mismatches.sort(key=lambda x: -x['cost'])

    if mismatches:
        print("\n[!] POTENTIAL MISMATCHES (need review):")
        print("-" * 40)
        for item in mismatches[:10]:
            print(f"  \"{item['search_term']}\" - ${item['cost']:.2f}")
            print(f"    -> Currently in: {item['ad_group_name']}")
            print(f"    -> Expected in: {item['natural_intent']}")
            print()

    # Ad group distribution analysis
    print("\nAD GROUP TRAFFIC DISTRIBUTION")
    print("-" * 40)
    ag_stats = defaultdict(lambda: {'terms': 0, 'clicks': 0, 'cost': 0, 'conv': 0})
    for item in analysis:
        ag = item['ad_group_name']
        ag_stats[ag]['terms'] += 1
        ag_stats[ag]['clicks'] += item['clicks']
        ag_stats[ag]['cost'] += item['cost']
        ag_stats[ag]['conv'] += item['conversions']

    for ag, stats in sorted(ag_stats.items(), key=lambda x: -x[1]['cost']):
        cpa = stats['cost'] / stats['conv'] if stats['conv'] > 0 else 0
        print(f"  {ag}")
        print(f"    {stats['terms']} terms | {stats['clicks']} clicks | ${stats['cost']:,.2f} | {stats['conv']:.1f} conv | CPA: ${cpa:.2f}")

    print("\n" + "=" * 60)


def save_csv(data, filename, fieldnames=None):
    if not data:
        print(f"  No data for {filename}")
        return
    filepath = f'{OUTPUT_DIR}/{filename}'
    if not fieldnames:
        fieldnames = list(data[0].keys())
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"  Saved: {filename} ({len(data)} rows)")


def main():
    print("Pulling ad group negatives for traffic shaping context...")
    ad_group_negatives = get_ad_group_negatives()
    total_negs = sum(len(v) for v in ad_group_negatives.values())
    print(f"Found {total_negs} ad group level negatives across {len(ad_group_negatives)} ad groups\n")

    print("Pulling search term report for last 60 days...")
    search_terms = pull_search_term_report()
    print(f"Retrieved {len(search_terms)} search terms\n")

    print("Analyzing traffic routing with shaping context...")
    analysis = analyze_traffic_routing(search_terms, ad_group_negatives)
    print(f"Analyzed {len(analysis)} NonBrand terms\n")

    print("Generating refined recommendations...")
    recommendations = generate_refined_recommendations(analysis)
    print(f"Found {len(recommendations)} items needing review\n")

    # Save outputs
    print("Saving output files...")
    save_csv(analysis, 'traffic_routing_analysis.csv')
    save_csv(recommendations, 'refined_recommendations.csv')

    # Print summary
    print_traffic_shaping_summary(analysis, ad_group_negatives)


if __name__ == '__main__':
    main()
