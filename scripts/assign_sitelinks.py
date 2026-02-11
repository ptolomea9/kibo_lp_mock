"""
Assign sitelink assets to ad groups for Kibo Commerce Search - NonBrand campaign

This script:
1. Reads created sitelink assets from created_sitelink_assets.csv
2. Links each asset to its corresponding ad group using AdGroupAssetOperation
3. Uses field_type = SITELINK for proper assignment
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from google.ads.googleads.client import GoogleAdsClient
from ads_mcp.utils import get_googleads_service
import csv

CUSTOMER_ID = '9948697111'
YAML_PATH = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

def get_ad_group_ids():
    """Get ad group IDs for Search - NonBrand campaign"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT ad_group.id, ad_group.name
    FROM ad_group
    WHERE campaign.name = 'Search - NonBrand'
    AND ad_group.status = 'ENABLED'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    ids = {}
    for row in response:
        ids[row.ad_group.name] = str(row.ad_group.id)
    return ids

def load_created_assets(filepath):
    """Load created sitelink assets from CSV"""
    assets = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            assets.append({
                'resource_name': row['resource_name'],
                'ad_group': row['ad_group'],
                'link_text': row['link_text']
            })

    return assets

def assign_sitelinks_to_ad_groups(client, assets, ad_group_ids, dry_run=True):
    """Assign sitelink assets to ad groups"""
    operations = []
    assignments = []

    for asset in assets:
        ag_name = asset['ad_group']
        ag_id = ad_group_ids.get(ag_name)

        if not ag_id:
            print(f"  WARNING: Ad group '{ag_name}' not found, skipping '{asset['link_text']}'")
            continue

        # Create ad group asset operation
        operation = client.get_type("AdGroupAssetOperation")
        ad_group_asset = operation.create

        # Set ad group resource name
        ad_group_asset.ad_group = client.get_service("AdGroupService").ad_group_path(
            CUSTOMER_ID, ag_id
        )

        # Set asset resource name
        ad_group_asset.asset = asset['resource_name']

        # Set field type to SITELINK
        ad_group_asset.field_type = client.enums.AssetFieldTypeEnum.SITELINK

        operations.append(operation)
        assignments.append({
            'ad_group': ag_name,
            'ad_group_id': ag_id,
            'link_text': asset['link_text'],
            'asset': asset['resource_name']
        })

    if dry_run:
        print(f"\n[DRY RUN] Would assign {len(operations)} sitelinks to ad groups:")

        # Group by ad group
        by_ad_group = {}
        for a in assignments:
            ag = a['ad_group']
            if ag not in by_ad_group:
                by_ad_group[ag] = []
            by_ad_group[ag].append(a)

        for ag, sls in by_ad_group.items():
            print(f"\n  {ag} (ID: {sls[0]['ad_group_id']}) - {len(sls)} sitelinks:")
            for sl in sls:
                print(f"    - {sl['link_text']}")

        return None
    else:
        # Execute the operations
        ad_group_asset_service = client.get_service("AdGroupAssetService")
        response = ad_group_asset_service.mutate_ad_group_assets(
            customer_id=CUSTOMER_ID,
            operations=operations
        )

        return response, assignments

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true', help='Execute (default is dry run)')
    args = parser.parse_args()

    print("=" * 70)
    print("Assign Sitelink Assets to Ad Groups")
    print("=" * 70)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    # Load created assets
    print("\nLoading created sitelink assets...")
    assets_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/created_sitelink_assets.csv'

    try:
        assets = load_created_assets(assets_file)
        print(f"  Loaded {len(assets)} assets")
    except FileNotFoundError:
        print(f"  ERROR: {assets_file} not found!")
        print("  Run create_sitelinks.py --execute first")
        sys.exit(1)

    # Get ad group IDs
    print("\nFetching ad group IDs...")
    ad_group_ids = get_ad_group_ids()
    for name, id in ad_group_ids.items():
        print(f"  {name}: {id}")

    if args.execute:
        print("\n" + "=" * 70)
        print("ASSIGNING SITELINKS TO AD GROUPS")
        print("=" * 70)

        result = assign_sitelinks_to_ad_groups(client, assets, ad_group_ids, dry_run=False)

        if result:
            response, assignments = result
            print(f"\nSuccessfully assigned {len(response.results)} sitelinks!")

            for i, res in enumerate(response.results):
                if i < len(assignments):
                    print(f"  {assignments[i]['ad_group']}: {assignments[i]['link_text']}")

            print("\n" + "-" * 70)
            print("Verification:")
            print("  1. Run query_sitelinks.py to verify assignments")
            print("  2. Check Google Ads UI Ad Preview for each ad group")
    else:
        print("\n" + "=" * 70)
        print("DRY RUN MODE (use --execute to assign sitelinks)")
        print("=" * 70)

        assign_sitelinks_to_ad_groups(client, assets, ad_group_ids, dry_run=True)

        print("\n" + "-" * 70)
        print("Next steps:")
        print("  1. Run with --execute to assign sitelinks to ad groups")
        print("  2. Run query_sitelinks.py to verify assignments")
