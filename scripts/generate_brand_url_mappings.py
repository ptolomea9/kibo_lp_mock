"""
Generate URL mappings for Brand keywords missing Final URLs

This script:
1. Loads active Brand keywords from the 60-day query
2. Identifies keywords without Final URLs or with suboptimal URLs
3. Applies brand-specific URL mapping logic
4. Outputs mappings in the format expected by update_keyword_urls.py
"""

import csv
import re

BASE_URL = 'https://kibocommerce.com'

# Brand keyword patterns and their recommended URLs
# Order matters - more specific patterns should come first
BRAND_KEYWORD_URL_PATTERNS = [
    # High-intent conversion pages
    (r'demo|trial|free trial', '/request-a-demo/'),
    (r'pricing|cost|price', '/request-a-demo/'),
    (r'contact|talk to|speak', '/speak-with-an-expert/'),

    # Product-specific pages
    (r'oms|order management|fulfillment', '/platform/order-management/'),
    (r'inventory|stock', '/platform/inventory-visibility/'),
    (r'subscription|recurring', '/platform/subscription/'),
    (r'catalog|product information|pim', '/platform/catalog-price-promo/'),
    (r'agentic|ai commerce|artificial intelligence', '/platform/agentic-commerce/'),
    (r'connect|integration|api', '/platform/connect-hub/'),

    # Solution pages
    (r'b2b commerce|b2b platform|b2b ecommerce', '/solutions/b2b/'),
    (r'b2c|consumer|retail', '/platform/commerce/'),
    (r'unified commerce|omnichannel', '/platform/platform-commerce/'),

    # Social proof / research intent
    (r'review|comparison|vs|versus', '/customer-stories/'),
    (r'case stud|success stor|testimonial', '/customer-stories/'),

    # Industry verticals (if present in brand searches)
    (r'wholesal', '/ppc/wholesale/'),
    (r'manufactur', '/ppc/manufacturing/'),
    (r'distribut', '/ppc/distributor/'),

    # Generic brand - homepage
    (r'kibo commerce|kibo platform', '/'),
    (r'^kibo$', '/'),
]

# URLs that are considered optimal (don't need updating)
OPTIMAL_URLS = [
    'https://kibocommerce.com/',
    'https://kibocommerce.com/request-a-demo/',
    'https://kibocommerce.com/platform/order-management/',
    'https://kibocommerce.com/platform/inventory-visibility/',
    'https://kibocommerce.com/platform/subscription/',
    'https://kibocommerce.com/platform/agentic-commerce/',
    'https://kibocommerce.com/platform/catalog-price-promo/',
    'https://kibocommerce.com/platform/connect-hub/',
    'https://kibocommerce.com/platform/platform-commerce/',
    'https://kibocommerce.com/platform/commerce/',
    'https://kibocommerce.com/solutions/b2b/',
    'https://kibocommerce.com/customer-stories/',
    'https://kibocommerce.com/speak-with-an-expert/',
]


def load_brand_keywords(filepath):
    """Load brand keywords from the 60-day query CSV"""
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


def get_url_for_brand_keyword(keyword_text):
    """
    Determine the best URL for a brand keyword based on content.
    Returns (url_path, rationale)
    """
    keyword_lower = keyword_text.lower()

    # Check each pattern in order
    for pattern, url_path in BRAND_KEYWORD_URL_PATTERNS:
        if re.search(pattern, keyword_lower):
            return url_path, f'Keyword matches "{pattern}" pattern'

    # Default: homepage for pure brand terms
    return '/', 'Default brand term - homepage'


def is_url_optimal(current_url, keyword_text):
    """
    Check if the current URL is already optimal for this keyword.
    Returns True if URL is good, False if it should be updated.
    """
    if not current_url:
        return False

    # Get the recommended URL for this keyword
    recommended_path, _ = get_url_for_brand_keyword(keyword_text)
    recommended_url = BASE_URL + recommended_path

    # Check if current URL matches recommended
    if current_url.rstrip('/') == recommended_url.rstrip('/'):
        return True

    # Check if current URL is in the optimal list
    if current_url.rstrip('/') in [u.rstrip('/') for u in OPTIMAL_URLS]:
        # URL is valid, but may not be optimal for this specific keyword
        # Only flag for update if recommended is significantly different
        return True

    return False


def determine_priority(impressions, clicks):
    """Determine priority based on performance"""
    if impressions >= 100 or clicks >= 5:
        return 'High'
    elif impressions >= 20:
        return 'Medium'
    return 'Low'


def generate_brand_url_mappings(keywords):
    """Generate URL mappings for brand keywords needing updates"""
    mappings = []

    for kw in keywords:
        current_url = kw['final_urls'].split(';')[0] if kw['final_urls'] else ''

        # Check if URL needs updating
        if is_url_optimal(current_url, kw['keyword']):
            continue

        # Get URL recommendation
        url_path, rationale = get_url_for_brand_keyword(kw['keyword'])
        full_url = BASE_URL + url_path

        # Skip if recommended URL is same as current
        if current_url.rstrip('/') == full_url.rstrip('/'):
            continue

        # Determine priority based on impressions
        priority = determine_priority(kw['impressions'], kw['clicks'])

        mappings.append({
            'Keyword': f"[{kw['keyword']}]",
            'Ad Group': kw['ad_group_name'],
            'Campaign': kw['campaign_name'],
            'Match Type': kw['match_type'].capitalize(),
            'Current URL': current_url if current_url else 'Not specified',
            'Current Intent Level': 'Unknown' if not current_url else 'Medium',
            'Recommended URL (with anchor if applicable)': full_url,
            'Recommended Intent Level': 'HIGH',
            'Anchor Section Topic': 'Main page',
            'Relevance Score (1-10)': '9',  # Brand keywords are highly relevant
            'CTA on Page': 'Request Demo; Talk to Sales',
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
    print("Generate Brand URL Mappings - Kibo Commerce")
    print("=" * 70)

    input_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/brand_keywords_60d.csv'

    print(f"\nLoading brand keywords from: {input_file}")
    keywords = load_brand_keywords(input_file)
    print(f"  Loaded {len(keywords)} keywords")

    # Count current state
    with_urls = [k for k in keywords if k['final_urls']]
    without_urls = [k for k in keywords if not k['final_urls']]
    print(f"  - With Final URLs: {len(with_urls)}")
    print(f"  - Without Final URLs: {len(without_urls)}")

    print("\nGenerating URL mappings for brand keywords...")
    mappings = generate_brand_url_mappings(keywords)
    print(f"  Generated {len(mappings)} mappings")

    if not mappings:
        print("\n  All brand keywords already have optimal URLs!")
    else:
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
                current = m['Current URL']
                print(f"    - {m['Keyword']} (was: {current[:40]}{'...' if len(current) > 40 else ''})")
            if len(group) > 3:
                print(f"    ... and {len(group) - 3} more")

        # Show high priority keywords
        if high_priority:
            print("\n" + "-" * 70)
            print("High Priority Keywords:")
            print("-" * 70)
            for m in sorted(high_priority, key=lambda x: -x['Impressions (60d)'])[:10]:
                print(f"  {m['Keyword']} -> {m['Recommended URL (with anchor if applicable)']}")
                print(f"    {m['Impressions (60d)']} impr | {m['Rationale']}")

    # Save to CSV in audit format
    output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/brand_url_mappings.csv'

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
    print("  2. Run: python scripts/update_keyword_urls.py --input data/brand_url_mappings.csv")
    print("  3. If dry run looks good: python scripts/update_keyword_urls.py --input data/brand_url_mappings.csv --execute")
