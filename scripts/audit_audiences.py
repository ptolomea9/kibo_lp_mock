"""
Comprehensive Audience Audit for Kibo Commerce Google Ads Account

This script audits:
1. First-party audiences (remarketing, customer match)
2. Custom segments (search terms, URLs, apps)
3. Current audience targeting on Search - NonBrand campaign
4. Current audience exclusions
5. Available Google audiences (affinity, in-market)
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
import csv
from datetime import datetime

CUSTOMER_ID = '9948697111'

def query_user_lists():
    """Query all first-party audiences (remarketing lists, customer match, etc.)"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        user_list.id,
        user_list.name,
        user_list.type,
        user_list.size_for_search,
        user_list.size_for_display,
        user_list.membership_status,
        user_list.match_rate_percentage,
        user_list.eligible_for_search,
        user_list.eligible_for_display
    FROM user_list
    WHERE user_list.membership_status = 'OPEN'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    lists = []
    for row in response:
        ul = row.user_list
        lists.append({
            'id': ul.id,
            'name': ul.name,
            'type': ul.type.name if ul.type else 'UNKNOWN',
            'size_search': ul.size_for_search,
            'size_display': ul.size_for_display,
            'match_rate': ul.match_rate_percentage if ul.match_rate_percentage else 'N/A',
            'eligible_search': ul.eligible_for_search,
            'eligible_display': ul.eligible_for_display
        })

    return lists

def query_custom_audiences():
    """Query custom segments/audiences"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        custom_audience.id,
        custom_audience.name,
        custom_audience.type,
        custom_audience.status,
        custom_audience.description
    FROM custom_audience
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

        audiences = []
        for row in response:
            ca = row.custom_audience
            audiences.append({
                'id': ca.id,
                'name': ca.name,
                'type': ca.type.name if ca.type else 'UNKNOWN',
                'status': ca.status.name if ca.status else 'UNKNOWN',
                'description': ca.description
            })

        return audiences
    except Exception as e:
        print(f"  Note: Could not query custom audiences - {e}")
        return []

def query_campaign_audience_targeting():
    """Query audience targeting at campaign level for NonBrand"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        campaign.id,
        campaign.name,
        campaign_criterion.criterion_id,
        campaign_criterion.type,
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

        # Determine audience reference
        audience_ref = ''
        if cc.user_list and cc.user_list.user_list:
            audience_ref = cc.user_list.user_list

        targeting.append({
            'campaign': row.campaign.name,
            'criterion_id': cc.criterion_id,
            'type': cc.type.name if cc.type else 'UNKNOWN',
            'status': cc.status.name if cc.status else 'UNKNOWN',
            'is_exclusion': cc.negative,
            'bid_modifier': cc.bid_modifier if cc.bid_modifier else 1.0,
            'audience_ref': audience_ref
        })

    return targeting

def query_ad_group_audience_targeting():
    """Query audience targeting at ad group level for NonBrand"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group.id,
        ad_group.name,
        campaign.name,
        ad_group_criterion.criterion_id,
        ad_group_criterion.type,
        ad_group_criterion.status,
        ad_group_criterion.negative,
        ad_group_criterion.bid_modifier,
        ad_group_criterion.user_list.user_list
    FROM ad_group_criterion
    WHERE campaign.name = 'Search - NonBrand'
    AND ad_group_criterion.type = 'USER_LIST'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    targeting = []
    for row in response:
        agc = row.ad_group_criterion

        # Determine audience reference
        audience_ref = ''
        if agc.user_list and agc.user_list.user_list:
            audience_ref = agc.user_list.user_list

        targeting.append({
            'ad_group': row.ad_group.name,
            'ad_group_id': row.ad_group.id,
            'criterion_id': agc.criterion_id,
            'type': agc.type.name if agc.type else 'UNKNOWN',
            'status': agc.status.name if agc.status else 'UNKNOWN',
            'is_exclusion': agc.negative,
            'bid_modifier': agc.bid_modifier if agc.bid_modifier else 1.0,
            'audience_ref': audience_ref
        })

    return targeting

def query_audience_info():
    """Query available audience resources (Google audiences)"""
    ga_service = get_googleads_service('GoogleAdsService')

    # Query audiences that are in use or available
    query = '''
    SELECT
        audience.id,
        audience.name,
        audience.description,
        audience.status,
        audience.dimensions
    FROM audience
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

        audiences = []
        for row in response:
            aud = row.audience
            audiences.append({
                'id': aud.id,
                'name': aud.name,
                'description': aud.description if aud.description else '',
                'status': aud.status.name if aud.status else 'UNKNOWN'
            })

        return audiences
    except Exception as e:
        print(f"  Note: Could not query audience info - {e}")
        return []

def query_combined_audiences():
    """Query combined audience segments"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        combined_audience.id,
        combined_audience.name,
        combined_audience.status,
        combined_audience.description
    FROM combined_audience
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

        audiences = []
        for row in response:
            ca = row.combined_audience
            audiences.append({
                'id': ca.id,
                'name': ca.name,
                'status': ca.status.name if ca.status else 'UNKNOWN',
                'description': ca.description if ca.description else ''
            })

        return audiences
    except Exception as e:
        print(f"  Note: Could not query combined audiences - {e}")
        return []

def query_ad_group_info():
    """Get NonBrand ad groups for reference"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group.id,
        ad_group.name,
        ad_group.status,
        campaign.name
    FROM ad_group
    WHERE campaign.name = 'Search - NonBrand'
    AND ad_group.status = 'ENABLED'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    ad_groups = []
    for row in response:
        ad_groups.append({
            'id': row.ad_group.id,
            'name': row.ad_group.name
        })

    return ad_groups

if __name__ == '__main__':
    print("=" * 80)
    print("Kibo Commerce Audience Audit Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 1. First-Party Audiences
    print("\n" + "=" * 80)
    print("1. FIRST-PARTY AUDIENCES (Remarketing, Customer Match)")
    print("=" * 80)
    user_lists = query_user_lists()
    if user_lists:
        print(f"\nFound {len(user_lists)} first-party audience(s):\n")
        for ul in user_lists:
            print(f"  ID: {ul['id']}")
            print(f"  Name: {ul['name']}")
            print(f"  Type: {ul['type']}")
            print(f"  Size (Search): {ul['size_search']:,}" if ul['size_search'] else "  Size (Search): N/A")
            print(f"  Size (Display): {ul['size_display']:,}" if ul['size_display'] else "  Size (Display): N/A")
            print(f"  Match Rate: {ul['match_rate']}%")
            print(f"  Eligible for Search: {ul['eligible_search']}")
            print(f"  Eligible for Display: {ul['eligible_display']}")
            print()
    else:
        print("\n  No first-party audiences found in this account.")

    # 2. Custom Segments
    print("\n" + "=" * 80)
    print("2. CUSTOM SEGMENTS (Search Terms, URLs, Apps)")
    print("=" * 80)
    custom_audiences = query_custom_audiences()
    if custom_audiences:
        print(f"\nFound {len(custom_audiences)} custom segment(s):\n")
        for ca in custom_audiences:
            print(f"  ID: {ca['id']}")
            print(f"  Name: {ca['name']}")
            print(f"  Type: {ca['type']}")
            print(f"  Status: {ca['status']}")
            if ca['description']:
                print(f"  Description: {ca['description']}")
            print()
    else:
        print("\n  No custom segments found in this account.")

    # 3. Combined Audiences
    print("\n" + "=" * 80)
    print("3. COMBINED AUDIENCES")
    print("=" * 80)
    combined = query_combined_audiences()
    if combined:
        print(f"\nFound {len(combined)} combined audience(s):\n")
        for ca in combined:
            print(f"  ID: {ca['id']}")
            print(f"  Name: {ca['name']}")
            print(f"  Status: {ca['status']}")
            if ca['description']:
                print(f"  Description: {ca['description']}")
            print()
    else:
        print("\n  No combined audiences found in this account.")

    # 4. Audience Resources
    print("\n" + "=" * 80)
    print("4. AUDIENCE RESOURCES (Created Audiences)")
    print("=" * 80)
    audiences = query_audience_info()
    if audiences:
        print(f"\nFound {len(audiences)} audience resource(s):\n")
        for aud in audiences[:20]:  # Limit output
            print(f"  ID: {aud['id']}")
            print(f"  Name: {aud['name']}")
            print(f"  Status: {aud['status']}")
            if aud['description']:
                print(f"  Description: {aud['description'][:100]}...")
            print()
        if len(audiences) > 20:
            print(f"  ... and {len(audiences) - 20} more")
    else:
        print("\n  No audience resources found.")

    # 5. NonBrand Ad Groups
    print("\n" + "=" * 80)
    print("5. SEARCH - NONBRAND AD GROUPS")
    print("=" * 80)
    ad_groups = query_ad_group_info()
    print(f"\nFound {len(ad_groups)} enabled ad group(s):\n")
    for ag in ad_groups:
        print(f"  - {ag['name']} (ID: {ag['id']})")

    # 6. Campaign-Level Audience Targeting
    print("\n" + "=" * 80)
    print("6. CAMPAIGN-LEVEL AUDIENCE TARGETING (Search - NonBrand)")
    print("=" * 80)
    campaign_targeting = query_campaign_audience_targeting()
    if campaign_targeting:
        inclusions = [t for t in campaign_targeting if not t['is_exclusion']]
        exclusions = [t for t in campaign_targeting if t['is_exclusion']]

        print(f"\nTargeted Audiences ({len(inclusions)}):")
        if inclusions:
            for t in inclusions:
                bid_adj = f"+{(t['bid_modifier']-1)*100:.0f}%" if t['bid_modifier'] > 1 else f"{(t['bid_modifier']-1)*100:.0f}%" if t['bid_modifier'] < 1 else "No adjustment"
                print(f"  - Type: {t['type']}, Status: {t['status']}, Bid: {bid_adj}")
                print(f"    Reference: {t['audience_ref']}")
        else:
            print("  None")

        print(f"\nExcluded Audiences ({len(exclusions)}):")
        if exclusions:
            for t in exclusions:
                print(f"  - Type: {t['type']}, Status: {t['status']}")
                print(f"    Reference: {t['audience_ref']}")
        else:
            print("  None")
    else:
        print("\n  No audience targeting found at campaign level.")

    # 7. Ad Group-Level Audience Targeting
    print("\n" + "=" * 80)
    print("7. AD GROUP-LEVEL AUDIENCE TARGETING (Search - NonBrand)")
    print("=" * 80)
    ag_targeting = query_ad_group_audience_targeting()
    if ag_targeting:
        # Group by ad group
        by_ag = {}
        for t in ag_targeting:
            ag_name = t['ad_group']
            if ag_name not in by_ag:
                by_ag[ag_name] = {'inclusions': [], 'exclusions': []}
            if t['is_exclusion']:
                by_ag[ag_name]['exclusions'].append(t)
            else:
                by_ag[ag_name]['inclusions'].append(t)

        for ag_name, targets in by_ag.items():
            print(f"\n  {ag_name}:")
            print(f"    Targeted: {len(targets['inclusions'])}")
            for t in targets['inclusions']:
                bid_adj = f"+{(t['bid_modifier']-1)*100:.0f}%" if t['bid_modifier'] > 1 else f"{(t['bid_modifier']-1)*100:.0f}%" if t['bid_modifier'] < 1 else "No adjustment"
                print(f"      - {t['type']}: {t['audience_ref']} (Bid: {bid_adj})")
            print(f"    Excluded: {len(targets['exclusions'])}")
            for t in targets['exclusions']:
                print(f"      - {t['type']}: {t['audience_ref']}")
    else:
        print("\n  No audience targeting found at ad group level.")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 80)

    print(f"""
First-Party Audiences Available: {len(user_lists)}
Custom Segments Available: {len(custom_audiences)}
Combined Audiences: {len(combined)}
Campaign-Level Targeting: {len(campaign_targeting)} criterion(s)
Ad Group-Level Targeting: {len(ag_targeting)} criterion(s)

Next Steps:
1. Review which first-party audiences should be targeted or excluded
2. Consider creating custom segments for B2B commerce intent signals
3. Add relevant in-market audiences for B2B software/technology
4. Set up proper exclusions for existing customers if RLSA strategy requires
""")

    # Save to CSV for reference
    output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/audience_audit_results.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'ID', 'Name', 'Type', 'Status', 'Details'])

        for ul in user_lists:
            writer.writerow(['First-Party', ul['id'], ul['name'], ul['type'],
                           'Eligible' if ul['eligible_search'] else 'Not Eligible',
                           f"Size: {ul['size_search']}"])

        for ca in custom_audiences:
            writer.writerow(['Custom Segment', ca['id'], ca['name'], ca['type'],
                           ca['status'], ca['description']])

        for ca in combined:
            writer.writerow(['Combined', ca['id'], ca['name'], 'COMBINED',
                           ca['status'], ca['description']])

    print(f"\nAudit results saved to: {output_file}")
    print("=" * 80)
