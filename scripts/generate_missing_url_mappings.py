"""
Generate URL mappings for keywords missing Final URLs

This script:
1. Loads active keywords from the 60-day query
2. Identifies keywords without Final URLs
3. Applies URL mapping logic based on ad group and keyword content
4. Outputs mappings in the format expected by update_keyword_urls.py
"""

import csv
import re

BASE_URL = 'https://kibocommerce.com'

# Ad Group to URL mapping (primary logic)
AD_GROUP_URL_MAP = {
    'B2B EComm': '/solutions/b2b/',
    'OMS': '/platform/order-management/',
    'B2C EComm': '/platform/commerce/',
    'NB - Wholesalers': '/ppc/wholesale/',
    'NB - Manufacturers': '/ppc/manufacturing/',
    'NB - Distributors': '/ppc/distributor/',
    'NB - General B2B': '/solutions/b2b/',
    'Agentic Commerce': '/platform/agentic-commerce/',
    'B2B Other Keywords': '/solutions/b2b/',  # Default, will be refined by keyword
}

# Keyword content patterns for URL refinement (secondary logic)
KEYWORD_URL_PATTERNS = [
    # Higher priority - specific product pages
    (r'inventory', '/platform/inventory-visibility/'),
    (r'catalog', '/platform/catalog-price-promo/'),
    (r'subscription', '/platform/subscription/'),
    (r'connect|integration', '/platform/connect-hub/'),
    (r'agentic|ai commerce', '/platform/agentic-commerce/'),
    # Generic patterns
    (r'unified commerce', '/'),  # Homepage
    (r'order management|oms', '/platform/order-management/'),
    (r'wholesal', '/ppc/wholesale/'),
    (r'manufactur', '/ppc/manufacturing/'),
    (r'distributor|distribution', '/ppc/distributor/'),
    (r'b2c|consumer', '/platform/commerce/'),
]

# Anchor sections for specific pages
ANCHOR_MAP = {
    '/ppc/wholesale/': {
        'order management': '#order-management',
        'b2b portal': '#b2b-commerce',
        'b2b commerce': '#b2b-commerce',
        'trade portal': '#b2b-commerce',
    },
    '/ppc/manufacturing/': {
        'b2b commerce': '#b2b-commerce',
        'dealer portal': '#b2b-commerce',
        'order management': '#form',
    },
    '/ppc/distributor/': {
        'inventory': '#form',
    },
}


def load_active_keywords(filepath):
    """Load active keywords from the 60-day query CSV"""
    keywords = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            keywords.append({
                'keyword': row['keyword'],
                'match_type': row['match_type'],
                'criterion_id': row['criterion_id'],
                'final_urls': row['final_urls'],
                'ad_group_name': row['ad_group_name'],
                'ad_group_id': row['ad_group_id'],
                'campaign_name': row['campaign_name'],
                'campaign_id': row['campaign_id'],
                'impressions': int(row['impressions']),
                'clicks': int(row['clicks']),
            })
    return keywords


def get_url_for_keyword(keyword_text, ad_group_name):
    """
    Determine the best URL for a keyword based on ad group and keyword content.
    Returns (url_path, anchor, rationale)
    """
    keyword_lower = keyword_text.lower()

    # Start with ad group default
    base_path = AD_GROUP_URL_MAP.get(ad_group_name, '/solutions/b2b/')
    anchor = ''
    rationale = f'Ad group default: {ad_group_name}'

    # Check keyword content for more specific URLs
    for pattern, url_path in KEYWORD_URL_PATTERNS:
        if re.search(pattern, keyword_lower):
            # Only override if it's a more specific match
            if url_path != base_path:
                base_path = url_path
                rationale = f'Keyword contains "{pattern}" pattern'
            break

    # Check for anchor opportunities
    if base_path in ANCHOR_MAP:
        for anchor_pattern, anchor_suffix in ANCHOR_MAP[base_path].items():
            if anchor_pattern in keyword_lower:
                anchor = anchor_suffix
                rationale += f' with anchor for "{anchor_pattern}"'
                break

    return base_path, anchor, rationale


def determine_priority(impressions, clicks):
    """Determine priority based on performance"""
    if impressions >= 100 or clicks >= 5:
        return 'High'
    elif impressions >= 20:
        return 'Medium'
    return 'Low'


def generate_missing_url_mappings(keywords):
    """Generate URL mappings for keywords without Final URLs"""
    mappings = []

    for kw in keywords:
        # Skip keywords that already have URLs
        if kw['final_urls']:
            continue

        # Get URL recommendation
        url_path, anchor, rationale = get_url_for_keyword(
            kw['keyword'],
            kw['ad_group_name']
        )

        full_url = BASE_URL + url_path + anchor

        # Determine priority based on impressions
        priority = determine_priority(kw['impressions'], kw['clicks'])

        mappings.append({
            'Keyword': f"[{kw['keyword']}]",
            'Ad Group': kw['ad_group_name'],
            'Campaign': kw['campaign_name'],
            'Match Type': kw['match_type'].capitalize(),
            'Current URL': 'Not specified',
            'Current Intent Level': 'Unknown',
            'Recommended URL (with anchor if applicable)': full_url,
            'Recommended Intent Level': 'HIGH',
            'Anchor Section Topic': 'Main page' if not anchor else anchor.replace('#', '').replace('-', ' ').title(),
            'Relevance Score (1-10)': '8',
            'CTA on Page': 'Watch Demo; Talk to Sales',
            'Rationale': rationale,
            'Gap Flag': 'No',
            'Priority': priority,
            # Extra fields for reference
            'Impressions (60d)': kw['impressions'],
            'Clicks (60d)': kw['clicks'],
            'Criterion ID': kw['criterion_id'],
            'Ad Group ID': kw['ad_group_id'],
        })

    return mappings


if __name__ == '__main__':
    print("=" * 70)
    print("Generate Missing URL Mappings - Kibo Commerce")
    print("=" * 70)

    input_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/active_keywords_60d.csv'

    print(f"\nLoading active keywords from: {input_file}")
    keywords = load_active_keywords(input_file)
    print(f"  Loaded {len(keywords)} keywords")

    # Count current state
    with_urls = [k for k in keywords if k['final_urls']]
    without_urls = [k for k in keywords if not k['final_urls']]
    print(f"  - With Final URLs: {len(with_urls)}")
    print(f"  - Without Final URLs: {len(without_urls)}")

    print("\nGenerating URL mappings for keywords missing URLs...")
    mappings = generate_missing_url_mappings(keywords)
    print(f"  Generated {len(mappings)} mappings")

    # Show by priority
    high_priority = [m for m in mappings if m['Priority'] == 'High']
    medium_priority = [m for m in mappings if m['Priority'] == 'Medium']
    low_priority = [m for m in mappings if m['Priority'] == 'Low']

    print(f"\n  By Priority:")
    print(f"    High: {len(high_priority)}")
    print(f"    Medium: {len(medium_priority)}")
    print(f"    Low: {len(low_priority)}")

    # Show by target URL
    print("\n" + "-" * 70)
    print("Mappings by Target URL:")
    print("-" * 70)

    url_groups = {}
    for m in mappings:
        url = m['Recommended URL (with anchor if applicable)']
        if url not in url_groups:
            url_groups[url] = []
        url_groups[url].append(m)

    for url, group in sorted(url_groups.items(), key=lambda x: -len(x[1])):
        print(f"\n  {url} ({len(group)} keywords)")
        for m in group[:3]:
            print(f"    - {m['Keyword']} ({m['Impressions (60d)']} impr, {m['Priority']})")
        if len(group) > 3:
            print(f"    ... and {len(group) - 3} more")

    # Show high priority keywords
    if high_priority:
        print("\n" + "-" * 70)
        print("High Priority Keywords (top performers missing URLs):")
        print("-" * 70)
        for m in sorted(high_priority, key=lambda x: -x['Impressions (60d)'])[:10]:
            print(f"  {m['Keyword']} -> {m['Recommended URL (with anchor if applicable)']}")
            print(f"    {m['Impressions (60d)']} impr | {m['Ad Group']} | {m['Rationale']}")

    # Save to CSV in audit format
    output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/missing_url_mappings.csv'

    # Use the same columns as keyword_landing_page_audit.csv for compatibility
    audit_columns = [
        'Keyword', 'Ad Group', 'Campaign', 'Match Type', 'Current URL',
        'Current Intent Level', 'Recommended URL (with anchor if applicable)',
        'Recommended Intent Level', 'Anchor Section Topic', 'Relevance Score (1-10)',
        'CTA on Page', 'Rationale', 'Gap Flag', 'Priority'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=audit_columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(mappings)

    print(f"\n\nMappings saved to: {output_file}")
    print("\nTo apply these mappings:")
    print("  1. Review the CSV file")
    print("  2. Run: python scripts/update_keyword_urls.py --input data/missing_url_mappings.csv")
    print("  3. If dry run looks good: python scripts/update_keyword_urls.py --input data/missing_url_mappings.csv --execute")
