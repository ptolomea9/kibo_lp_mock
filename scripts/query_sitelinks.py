"""
Query current sitelinks and ad group IDs from Kibo Commerce Google Ads account

This script pulls:
- All sitelink assets in the account
- Campaign-level sitelink assignments
- Ad group-level sitelink assignments (if any)
- NonBrand ad group list with IDs
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
import csv

CUSTOMER_ID = '9948697111'

def query_all_sitelink_assets():
    """Query all sitelink assets in the account"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        asset.id,
        asset.name,
        asset.sitelink_asset.link_text,
        asset.sitelink_asset.description1,
        asset.sitelink_asset.description2,
        asset.final_urls,
        asset.type,
        asset.resource_name
    FROM asset
    WHERE asset.type = 'SITELINK'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    assets = []
    for row in response:
        sitelink = row.asset.sitelink_asset
        assets.append({
            'asset_id': row.asset.id,
            'name': row.asset.name,
            'link_text': sitelink.link_text,
            'description1': sitelink.description1,
            'description2': sitelink.description2,
            'final_urls': list(row.asset.final_urls) if row.asset.final_urls else [],
            'resource_name': row.asset.resource_name
        })

    return assets

def query_customer_sitelinks():
    """Query account-level (customer) sitelink assignments"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        customer_asset.asset,
        customer_asset.field_type,
        customer_asset.status,
        asset.id,
        asset.sitelink_asset.link_text,
        asset.final_urls
    FROM customer_asset
    WHERE customer_asset.field_type = 'SITELINK'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    assignments = []
    for row in response:
        assignments.append({
            'level': 'ACCOUNT',
            'asset_id': row.asset.id,
            'link_text': row.asset.sitelink_asset.link_text,
            'final_urls': list(row.asset.final_urls) if row.asset.final_urls else [],
            'status': row.customer_asset.status.name
        })

    return assignments

def query_campaign_sitelinks():
    """Query campaign-level sitelink assignments"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        campaign_asset.campaign,
        campaign_asset.asset,
        campaign_asset.field_type,
        campaign_asset.status,
        campaign.name,
        campaign.id,
        asset.id,
        asset.sitelink_asset.link_text,
        asset.final_urls
    FROM campaign_asset
    WHERE campaign_asset.field_type = 'SITELINK'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    assignments = []
    for row in response:
        assignments.append({
            'level': 'CAMPAIGN',
            'campaign_name': row.campaign.name,
            'campaign_id': row.campaign.id,
            'asset_id': row.asset.id,
            'link_text': row.asset.sitelink_asset.link_text,
            'final_urls': list(row.asset.final_urls) if row.asset.final_urls else [],
            'status': row.campaign_asset.status.name
        })

    return assignments

def query_ad_group_sitelinks():
    """Query ad group-level sitelink assignments"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group_asset.ad_group,
        ad_group_asset.asset,
        ad_group_asset.field_type,
        ad_group_asset.status,
        ad_group.name,
        ad_group.id,
        campaign.name,
        asset.id,
        asset.sitelink_asset.link_text,
        asset.final_urls
    FROM ad_group_asset
    WHERE ad_group_asset.field_type = 'SITELINK'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    assignments = []
    for row in response:
        assignments.append({
            'level': 'AD_GROUP',
            'campaign_name': row.campaign.name,
            'ad_group_name': row.ad_group.name,
            'ad_group_id': row.ad_group.id,
            'asset_id': row.asset.id,
            'link_text': row.asset.sitelink_asset.link_text,
            'final_urls': list(row.asset.final_urls) if row.asset.final_urls else [],
            'status': row.ad_group_asset.status.name
        })

    return assignments

def query_nonbrand_ad_groups():
    """Query ad groups from Search - NonBrand campaign"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group.id,
        ad_group.name,
        ad_group.status,
        campaign.name,
        campaign.id
    FROM ad_group
    WHERE campaign.name = 'Search - NonBrand'
    AND ad_group.status = 'ENABLED'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    ad_groups = []
    for row in response:
        ad_groups.append({
            'ad_group_id': row.ad_group.id,
            'ad_group_name': row.ad_group.name,
            'campaign_name': row.campaign.name,
            'campaign_id': row.campaign.id
        })

    return ad_groups

if __name__ == '__main__':
    print("=" * 70)
    print("Kibo Commerce Sitelink Query Report")
    print("=" * 70)

    # 1. Query all sitelink assets
    print("\n1. ALL SITELINK ASSETS IN ACCOUNT")
    print("-" * 50)
    assets = query_all_sitelink_assets()
    print(f"   Total sitelink assets: {len(assets)}")
    for a in assets:
        url = a['final_urls'][0] if a['final_urls'] else 'No URL'
        print(f"\n   Asset ID: {a['asset_id']}")
        print(f"   Link Text: {a['link_text']}")
        print(f"   Description 1: {a['description1']}")
        print(f"   Description 2: {a['description2']}")
        print(f"   URL: {url}")

    # 2. Query account-level sitelinks
    print("\n\n2. ACCOUNT-LEVEL SITELINK ASSIGNMENTS")
    print("-" * 50)
    account_sitelinks = query_customer_sitelinks()
    if account_sitelinks:
        print(f"   Total account-level sitelinks: {len(account_sitelinks)}")
        for s in account_sitelinks:
            url = s['final_urls'][0] if s['final_urls'] else 'No URL'
            print(f"   - [{s['status']}] {s['link_text']} -> {url}")
    else:
        print("   No account-level sitelinks found")

    # 3. Query campaign-level sitelinks
    print("\n\n3. CAMPAIGN-LEVEL SITELINK ASSIGNMENTS")
    print("-" * 50)
    campaign_sitelinks = query_campaign_sitelinks()
    if campaign_sitelinks:
        print(f"   Total campaign-level sitelinks: {len(campaign_sitelinks)}")
        for s in campaign_sitelinks:
            url = s['final_urls'][0] if s['final_urls'] else 'No URL'
            print(f"   - [{s['status']}] {s['campaign_name']}: {s['link_text']} -> {url}")
    else:
        print("   No campaign-level sitelinks found")

    # 4. Query ad group-level sitelinks
    print("\n\n4. AD GROUP-LEVEL SITELINK ASSIGNMENTS")
    print("-" * 50)
    ag_sitelinks = query_ad_group_sitelinks()
    if ag_sitelinks:
        print(f"   Total ad group-level sitelinks: {len(ag_sitelinks)}")
        for s in ag_sitelinks:
            url = s['final_urls'][0] if s['final_urls'] else 'No URL'
            print(f"   - [{s['status']}] {s['ad_group_name']}: {s['link_text']} -> {url}")
    else:
        print("   No ad group-level sitelinks found")

    # 5. Query NonBrand ad groups
    print("\n\n5. NONBRAND AD GROUPS (Target for new sitelinks)")
    print("-" * 50)
    ad_groups = query_nonbrand_ad_groups()
    print(f"   Total ad groups: {len(ad_groups)}")
    for ag in ad_groups:
        print(f"   - ID: {ag['ad_group_id']} | Name: {ag['ad_group_name']}")

    # Save ad group IDs to file for reference
    output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/nonbrand_ad_groups.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['ad_group_id', 'ad_group_name', 'campaign_name', 'campaign_id'])
        writer.writeheader()
        writer.writerows(ad_groups)
    print(f"\n   Ad groups saved to: {output_file}")

    print("\n" + "=" * 70)
    print("Query Complete")
    print("=" * 70)
