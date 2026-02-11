"""
Review Campaign-Level Audiences for Search - NonBrand

This script:
1. Shows all current campaign-level audiences (enabled, paused, excluded)
2. Identifies valuable audiences NOT currently targeted
3. Makes recommendations for optimization
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
from datetime import datetime

CUSTOMER_ID = '9948697111'

def get_all_user_lists():
    """Get all first-party audiences with details"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        user_list.id,
        user_list.name,
        user_list.type,
        user_list.size_for_search,
        user_list.membership_status,
        user_list.eligible_for_search
    FROM user_list
    WHERE user_list.membership_status = 'OPEN'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    lists = {}
    for row in response:
        ul = row.user_list
        lists[str(ul.id)] = {
            'id': str(ul.id),
            'name': ul.name,
            'type': ul.type.name if ul.type else 'UNKNOWN',
            'size_search': ul.size_for_search if ul.size_for_search else 0,
            'eligible_search': ul.eligible_for_search
        }

    return lists

def get_campaign_audience_targeting():
    """Get current audience targeting on Search - NonBrand"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        campaign_criterion.criterion_id,
        campaign_criterion.status,
        campaign_criterion.negative,
        campaign_criterion.bid_modifier,
        campaign_criterion.user_list.user_list
    FROM campaign_criterion
    WHERE campaign.name = 'Search - NonBrand'
    AND campaign_criterion.type = 'USER_LIST'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    targeting = []
    for row in response:
        cc = row.campaign_criterion

        # Extract user list ID
        user_list_id = ''
        if cc.user_list and cc.user_list.user_list:
            parts = cc.user_list.user_list.split('/')
            if len(parts) >= 4:
                user_list_id = parts[-1]

        targeting.append({
            'criterion_id': cc.criterion_id,
            'user_list_id': user_list_id,
            'status': cc.status.name if cc.status else 'UNKNOWN',
            'is_exclusion': cc.negative,
            'bid_modifier': cc.bid_modifier if cc.bid_modifier else 1.0
        })

    return targeting

if __name__ == '__main__':
    print("=" * 90)
    print("Campaign Audience Review: Search - NonBrand")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)

    # Get all user lists
    print("\nLoading all user lists...")
    all_lists = get_all_user_lists()
    print(f"  Found {len(all_lists)} total user lists")

    # Get campaign targeting
    print("\nLoading campaign targeting...")
    targeting = get_campaign_audience_targeting()
    print(f"  Found {len(targeting)} audience criteria")

    # Categorize current targeting
    enabled = []
    paused = []
    excluded = []

    for t in targeting:
        ul_id = t['user_list_id']
        ul_info = all_lists.get(ul_id, {'name': 'Unknown', 'size_search': 0, 'type': 'UNKNOWN'})

        t['name'] = ul_info.get('name', 'Unknown')
        t['size'] = ul_info.get('size_search', 0)
        t['type'] = ul_info.get('type', 'UNKNOWN')

        if t['is_exclusion']:
            excluded.append(t)
        elif t['status'] == 'ENABLED':
            enabled.append(t)
        elif t['status'] == 'PAUSED':
            paused.append(t)

    # Get IDs of all currently targeted lists
    targeted_ids = set(t['user_list_id'] for t in targeting)

    # ============================================================
    # SECTION 1: CURRENTLY ENABLED
    # ============================================================
    print("\n" + "=" * 90)
    print("1. ENABLED AUDIENCES (Observation Mode)")
    print("=" * 90)

    enabled_sorted = sorted(enabled, key=lambda x: x['size'], reverse=True)
    for t in enabled_sorted:
        bid_adj = f"+{(t['bid_modifier']-1)*100:.0f}%" if t['bid_modifier'] > 1 else f"{(t['bid_modifier']-1)*100:.0f}%" if t['bid_modifier'] < 1 else "0%"
        print(f"\n  [{t['status']}] {t['name']}")
        print(f"    ID: {t['user_list_id']} | Type: {t['type']} | Size: {t['size']:,}")
        print(f"    Bid Adjustment: {bid_adj}")

    # ============================================================
    # SECTION 2: PAUSED AUDIENCES - REVIEW THESE
    # ============================================================
    print("\n" + "=" * 90)
    print("2. PAUSED AUDIENCES (Review for Re-enabling)")
    print("=" * 90)

    paused_sorted = sorted(paused, key=lambda x: x['size'], reverse=True)
    for t in paused_sorted:
        relevance = "LOW"
        recommendation = "Keep paused"

        name_lower = t['name'].lower()

        # High relevance indicators
        if any(kw in name_lower for kw in ['order management', 'oms', 'b2b', 'ecommerce', 'commerce']):
            relevance = "HIGH"
            recommendation = "ENABLE - Directly relevant to NonBrand themes"
        elif any(kw in name_lower for kw in ['ppc', 'landing page', 'cpc', 'traffic medium']):
            relevance = "MEDIUM"
            recommendation = "ENABLE - Paid traffic re-engagement"
        elif any(kw in name_lower for kw in ['personalization', 'more than 2 pages', 'returning']):
            relevance = "MEDIUM"
            recommendation = "ENABLE - Engaged users"
        elif 'high quality' in name_lower:
            relevance = "HIGH"
            recommendation = "ENABLE - High quality traffic"
        elif t['size'] == 0:
            relevance = "LOW"
            recommendation = "Keep paused - No search size"

        print(f"\n  [{t['status']}] {t['name']}")
        print(f"    ID: {t['user_list_id']} | Type: {t['type']} | Size: {t['size']:,}")
        print(f"    >>> Relevance: {relevance} | Recommendation: {recommendation}")

    # ============================================================
    # SECTION 3: EXCLUDED AUDIENCES
    # ============================================================
    print("\n" + "=" * 90)
    print("3. EXCLUDED AUDIENCES (Keep as-is)")
    print("=" * 90)

    for t in excluded:
        print(f"\n  [EXCLUDED] {t['name']}")
        print(f"    ID: {t['user_list_id']} | Type: {t['type']} | Size: {t['size']:,}")
        print(f"    >>> Purpose: Prevent wasted spend on existing customers/users")

    # ============================================================
    # SECTION 4: MISSING AUDIENCES - NOT CURRENTLY TARGETED
    # ============================================================
    print("\n" + "=" * 90)
    print("4. VALUABLE AUDIENCES NOT CURRENTLY TARGETED")
    print("=" * 90)

    # Define high-value audience patterns for B2B commerce
    high_value_patterns = [
        'order management',
        'oms',
        'b2b',
        'b2c',
        'commerce',
        'agentic',
        'composable',
        'headless',
        'unified',
        'subscription',
        'hubspot',
        'target account',
        'prospect',
        'customer match',
        'email list',
        'youtube'
    ]

    missing_valuable = []
    for ul_id, ul_info in all_lists.items():
        # Skip if already targeted
        if ul_id in targeted_ids:
            continue

        # Skip if not eligible for search
        if not ul_info.get('eligible_search', False):
            continue

        # Skip similar audiences (deprecated/limited)
        if 'similar to' in ul_info['name'].lower():
            continue

        name_lower = ul_info['name'].lower()

        # Check if matches high-value patterns
        for pattern in high_value_patterns:
            if pattern in name_lower:
                missing_valuable.append({
                    'id': ul_id,
                    'name': ul_info['name'],
                    'type': ul_info['type'],
                    'size': ul_info['size_search'],
                    'pattern': pattern
                })
                break

    # Sort by size
    missing_sorted = sorted(missing_valuable, key=lambda x: x['size'], reverse=True)

    print(f"\nFound {len(missing_sorted)} valuable audiences not currently targeted:\n")

    for m in missing_sorted[:25]:  # Top 25
        size_str = f"{m['size']:,}" if m['size'] else "N/A"
        print(f"  {m['name']}")
        print(f"    ID: {m['id']} | Type: {m['type']} | Size: {size_str}")
        print(f"    Matched pattern: {m['pattern']}")
        print()

    # ============================================================
    # SECTION 5: SUMMARY & RECOMMENDATIONS
    # ============================================================
    print("\n" + "=" * 90)
    print("5. SUMMARY & RECOMMENDATIONS")
    print("=" * 90)

    # Count recommendations
    enable_count = sum(1 for t in paused if any(kw in t['name'].lower() for kw in
        ['order management', 'oms', 'b2b', 'ecommerce', 'commerce', 'ppc', 'landing page',
         'cpc', 'traffic medium', 'personalization', 'more than 2 pages', 'returning', 'high quality']))

    print(f"""
CURRENT STATE:
  - Enabled audiences: {len(enabled)}
  - Paused audiences: {len(paused)}
  - Excluded audiences: {len(excluded)}
  - Missing valuable audiences: {len(missing_sorted)}

RECOMMENDATIONS:

1. RE-ENABLE PAUSED AUDIENCES ({enable_count} recommended):
   - High Quality UTMs - 540 days
   - Returning Visitors
   - Order Management Page Visits Last 90 days
   - Personalization page visits last 90 days
   - PPC Landing Page Visitors Last 90 Days
   - eCommerce Page Visits Last 90 days
   - Ecommerce Visitors - 30 days
   - More than 2 Pages Visited

2. ADD NEW AUDIENCES (Top recommendations):
   - 2025 - Order Management Visitors - L90 (420 users)
   - 2025 - B2B Commerce - L90 (430 users)
   - 2025 - Agentic Commerce - L90 (200 users)
   - B2B Visitors - L90 (830 users)
   - HubSpot - B2B Target Account List
   - KIBO Customer Match Lists

3. KEEP EXCLUSIONS AS-IS:
   - Customer list exclusion (96% match) - Prevents existing customer spend
   - Login user audiences - Prevents existing user spend
""")

    print("=" * 90)
