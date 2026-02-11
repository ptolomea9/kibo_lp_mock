"""
Search Term Report Analysis - Negation Hygiene & Intent Mapping
Analyzes search query reports for last 60 days to identify:
1. Cross-contamination (brand terms in non-brand, vice versa)
2. Intent mapping issues (search terms going to wrong ad groups)
3. Generate negative keyword recommendations
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

# Compile brand patterns for efficiency
BRAND_REGEX = re.compile('|'.join(BRAND_PATTERNS), re.IGNORECASE)

# Intent mapping rules for NonBrand campaign
# Maps term patterns to expected ad groups
INTENT_RULES = {
    'B2B EComm': [
        r'\bb2b\b(?!.*\b(d2c|b2c|consumer)\b)',
        r'\benterprise\s*(ecommerce|commerce|platform)',
        r'\bwholesale\s*ecommerce\b',
    ],
    'B2C EComm': [
        r'\bb2c\b',
        r'\bd2c\b',
        r'\bdirect\s*to\s*consumer',
        r'\bconsumer\s*(ecommerce|commerce)',
        r'\bretail\s*(ecommerce|platform)',
    ],
    'OMS': [
        r'\boms\b',
        r'\border\s*management',
        r'\bfulfillment',
        r'\binventory\s*management',
        r'\bwarehouse\s*management',
        r'\border\s*orchestration',
    ],
    'NB - Manufacturers': [
        r'\bmanufacturer',
        r'\bmanufacturing\s*(ecommerce|commerce|platform)',
    ],
    'NB - Wholesalers': [
        r'\bwholesaler',
        r'\bwholesale\s*(platform|software|distribution)',
    ],
    'NB - Distributors': [
        r'\bdistributor',
        r'\bdistribution\s*(ecommerce|commerce|platform)',
    ],
    'B2B Other Keywords': [
        r'\bunified\s*commerce',
        r'\bcomposable\s*commerce',
        r'\bheadless\s*(commerce|ecommerce)',
        r'\bmach\s*(architecture|platform)',
        r'\bapi\s*first\s*commerce',
    ],
    'Agentic Commerce': [
        r'\bagentic',
        r'\bai\s*commerce',
        r'\bai\s*powered\s*(commerce|ecommerce)',
    ],
}

# Compile intent rules
COMPILED_INTENT_RULES = {}
for ad_group, patterns in INTENT_RULES.items():
    COMPILED_INTENT_RULES[ad_group] = [re.compile(p, re.IGNORECASE) for p in patterns]


def is_brand_term(search_term):
    """Check if search term contains brand keywords"""
    return bool(BRAND_REGEX.search(search_term))


def get_expected_ad_group(search_term):
    """Determine expected ad group based on search term patterns"""
    for ad_group, patterns in COMPILED_INTENT_RULES.items():
        for pattern in patterns:
            if pattern.search(search_term):
                return ad_group
    return None  # No clear intent detected


def pull_search_term_report():
    """Pull search term report for last 60 days from both campaigns"""
    ga_service = get_googleads_service('GoogleAdsService')

    # Calculate date range (last 60 days)
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

        term_data = {
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
        }
        search_terms.append(term_data)

    return search_terms


def analyze_cross_contamination(search_terms):
    """Identify brand/nonbrand cross-contamination issues"""
    issues = []

    for term in search_terms:
        campaign_name = term['campaign_name'].lower()

        # Check for brand terms in NonBrand campaign
        if 'nonbrand' in campaign_name and term['is_brand_term']:
            issues.append({
                **term,
                'issue_type': 'BRAND_IN_NONBRAND',
                'priority': 'HIGH',
                'recommendation': f'Add [{term["search_term"]}] as EXACT negative to Search - NonBrand campaign',
            })

        # Check for non-brand terms in Brand campaign
        elif 'brand' in campaign_name and 'nonbrand' not in campaign_name and not term['is_brand_term']:
            issues.append({
                **term,
                'issue_type': 'NONBRAND_IN_BRAND',
                'priority': 'MEDIUM',
                'recommendation': f'Add [{term["search_term"]}] as PHRASE negative to Search - Brand campaign',
            })

    return issues


def analyze_intent_mapping(search_terms):
    """Analyze intent mapping for NonBrand campaign terms"""
    issues = []

    for term in search_terms:
        campaign_name = term['campaign_name'].lower()

        # Only analyze NonBrand campaign terms
        if 'nonbrand' not in campaign_name:
            continue

        # Skip brand terms (should be negated anyway)
        if term['is_brand_term']:
            continue

        expected_ad_group = get_expected_ad_group(term['search_term'])
        actual_ad_group = term['ad_group_name']

        # If we have an expected ad group and it doesn't match actual
        if expected_ad_group and expected_ad_group.lower() not in actual_ad_group.lower():
            issues.append({
                **term,
                'expected_ad_group': expected_ad_group,
                'actual_ad_group': actual_ad_group,
                'issue_type': 'INTENT_MISMATCH',
                'priority': 'LOW',
                'recommendation': f'Consider adding [{term["search_term"]}] as negative to [{actual_ad_group}] to route to [{expected_ad_group}]',
            })

    return issues


def generate_negation_recommendations(cross_contamination, intent_issues):
    """Generate prioritized negative keyword recommendations"""
    recommendations = []

    # HIGH priority: Brand terms in NonBrand
    for issue in cross_contamination:
        if issue['issue_type'] == 'BRAND_IN_NONBRAND':
            recommendations.append({
                'priority': 'HIGH',
                'negative_keyword': issue['search_term'],
                'match_type': 'EXACT',
                'level': 'CAMPAIGN',
                'target_campaign': 'Search - NonBrand',
                'target_ad_group': '',
                'reason': 'Brand term appearing in NonBrand campaign',
                'wasted_spend': issue['cost'],
                'clicks': issue['clicks'],
            })

    # MEDIUM priority: NonBrand terms in Brand
    for issue in cross_contamination:
        if issue['issue_type'] == 'NONBRAND_IN_BRAND':
            recommendations.append({
                'priority': 'MEDIUM',
                'negative_keyword': issue['search_term'],
                'match_type': 'PHRASE',
                'level': 'CAMPAIGN',
                'target_campaign': 'Search - Brand',
                'target_ad_group': '',
                'reason': 'Non-brand term appearing in Brand campaign',
                'wasted_spend': issue['cost'],
                'clicks': issue['clicks'],
            })

    # LOW priority: Intent mismatches
    for issue in intent_issues:
        recommendations.append({
            'priority': 'LOW',
            'negative_keyword': issue['search_term'],
            'match_type': 'PHRASE',
            'level': 'AD_GROUP',
            'target_campaign': 'Search - NonBrand',
            'target_ad_group': issue['actual_ad_group'],
            'reason': f'Should route to {issue["expected_ad_group"]} instead of {issue["actual_ad_group"]}',
            'wasted_spend': issue['cost'],
            'clicks': issue['clicks'],
        })

    # Sort by priority and then by wasted spend
    priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    recommendations.sort(key=lambda x: (priority_order[x['priority']], -x['wasted_spend']))

    return recommendations


def save_csv(data, filename, fieldnames=None):
    """Save data to CSV file"""
    if not data:
        print(f"  No data to save for {filename}")
        return

    filepath = f'{OUTPUT_DIR}/{filename}'
    if not fieldnames:
        fieldnames = list(data[0].keys())

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"  Saved: {filename} ({len(data)} rows)")


def print_summary(search_terms, cross_contamination, intent_issues, recommendations):
    """Print console summary of analysis"""
    print("\n" + "=" * 50)
    print("SEARCH TERM ANALYSIS - Kibo Commerce")
    print("=" * 50)
    print("Period: Last 60 Days\n")

    # Campaign summary
    brand_terms = [t for t in search_terms if 'brand' in t['campaign_name'].lower() and 'nonbrand' not in t['campaign_name'].lower()]
    nonbrand_terms = [t for t in search_terms if 'nonbrand' in t['campaign_name'].lower()]

    brand_spend = sum(t['cost'] for t in brand_terms)
    nonbrand_spend = sum(t['cost'] for t in nonbrand_terms)

    print("CAMPAIGN SUMMARY")
    print(f"  Search - Brand: {len(brand_terms)} terms, ${brand_spend:,.2f} spend")
    print(f"  Search - NonBrand: {len(nonbrand_terms)} terms, ${nonbrand_spend:,.2f} spend")
    print()

    # Cross-contamination issues
    brand_in_nonbrand = [i for i in cross_contamination if i['issue_type'] == 'BRAND_IN_NONBRAND']
    nonbrand_in_brand = [i for i in cross_contamination if i['issue_type'] == 'NONBRAND_IN_BRAND']

    brand_in_nonbrand_spend = sum(i['cost'] for i in brand_in_nonbrand)
    nonbrand_in_brand_spend = sum(i['cost'] for i in nonbrand_in_brand)

    print("CROSS-CONTAMINATION ISSUES")
    print(f"  Brand terms in NonBrand: {len(brand_in_nonbrand)} (wasted: ${brand_in_nonbrand_spend:,.2f})")
    print(f"  NonBrand terms in Brand: {len(nonbrand_in_brand)} (wasted: ${nonbrand_in_brand_spend:,.2f})")
    print()

    # Top brand terms in nonbrand
    if brand_in_nonbrand:
        print("TOP BRAND TERMS IN NONBRAND (Immediate Action):")
        sorted_brand_issues = sorted(brand_in_nonbrand, key=lambda x: -x['cost'])[:5]
        for i, issue in enumerate(sorted_brand_issues, 1):
            print(f"  {i}. \"{issue['search_term']}\" - {issue['clicks']} clicks, ${issue['cost']:.2f} cost")
        print()

    # Top nonbrand terms in brand
    if nonbrand_in_brand:
        print("TOP NONBRAND TERMS IN BRAND (Review):")
        sorted_nonbrand_issues = sorted(nonbrand_in_brand, key=lambda x: -x['cost'])[:5]
        for i, issue in enumerate(sorted_nonbrand_issues, 1):
            print(f"  {i}. \"{issue['search_term']}\" - {issue['clicks']} clicks, ${issue['cost']:.2f} cost")
        print()

    # Intent mapping issues
    print(f"INTENT MAPPING ISSUES: {len(intent_issues)} terms")
    if intent_issues:
        sorted_intent = sorted(intent_issues, key=lambda x: -x['cost'])[:5]
        for issue in sorted_intent:
            print(f"  \"{issue['search_term']}\" -> {issue['actual_ad_group']} (expected: {issue['expected_ad_group']})")
    print()

    # Recommendations summary
    high_priority = [r for r in recommendations if r['priority'] == 'HIGH']
    medium_priority = [r for r in recommendations if r['priority'] == 'MEDIUM']
    low_priority = [r for r in recommendations if r['priority'] == 'LOW']

    print("RECOMMENDATIONS SUMMARY")
    print(f"  HIGH priority negatives: {len(high_priority)}")
    print(f"  MEDIUM priority negatives: {len(medium_priority)}")
    print(f"  LOW priority negatives: {len(low_priority)}")
    print("=" * 50)


def main():
    print("Pulling search term report for last 60 days...")
    search_terms = pull_search_term_report()
    print(f"Retrieved {len(search_terms)} search terms\n")

    print("Analyzing cross-contamination...")
    cross_contamination = analyze_cross_contamination(search_terms)
    print(f"Found {len(cross_contamination)} cross-contamination issues\n")

    print("Analyzing intent mapping...")
    intent_issues = analyze_intent_mapping(search_terms)
    print(f"Found {len(intent_issues)} intent mapping issues\n")

    print("Generating negation recommendations...")
    recommendations = generate_negation_recommendations(cross_contamination, intent_issues)
    print(f"Generated {len(recommendations)} recommendations\n")

    # Save output files
    print("Saving output files...")
    save_csv(search_terms, 'search_term_report_60d.csv')
    save_csv(cross_contamination, 'cross_contamination_issues.csv')
    save_csv(intent_issues, 'intent_mapping_issues.csv')
    save_csv(recommendations, 'negation_recommendations.csv')

    # Print summary
    print_summary(search_terms, cross_contamination, intent_issues, recommendations)


if __name__ == '__main__':
    main()
