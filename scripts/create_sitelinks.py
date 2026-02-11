"""
Create ad group-level sitelink assets for Kibo Commerce Search - NonBrand campaign

Creates 30 sitelink assets (6 per ad group x 5 ad groups) from sitelink_mapping.csv
Each asset includes:
- Link text (headline) - 25 char limit
- Description 1 - 35 char limit
- Description 2 - 35 char limit
- Final URL
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

def load_sitelink_mapping(filepath):
    """Load sitelink definitions from CSV"""
    sitelinks = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sitelinks.append({
                'ad_group': row['ad_group'],
                'link_text': row['link_text'],
                'description1': row['description1'],
                'description2': row['description2'],
                'final_url': row['final_url']
            })

    return sitelinks

def validate_sitelink(sitelink):
    """Validate sitelink character limits"""
    errors = []

    if len(sitelink['link_text']) > 25:
        errors.append(f"Link text '{sitelink['link_text']}' exceeds 25 chars ({len(sitelink['link_text'])})")

    if len(sitelink['description1']) > 35:
        errors.append(f"Description 1 '{sitelink['description1']}' exceeds 35 chars ({len(sitelink['description1'])})")

    if len(sitelink['description2']) > 35:
        errors.append(f"Description 2 '{sitelink['description2']}' exceeds 35 chars ({len(sitelink['description2'])})")

    return errors

def create_sitelink_assets(client, sitelinks, dry_run=True):
    """Create sitelink assets in Google Ads"""
    operations = []
    created = []

    for sl in sitelinks:
        # Validate first
        errors = validate_sitelink(sl)
        if errors:
            print(f"\n  WARNING: Validation errors for '{sl['link_text']}':")
            for e in errors:
                print(f"    - {e}")
            continue

        # Create asset operation
        operation = client.get_type("AssetOperation")
        asset = operation.create

        # Set asset name for identification
        asset.name = f"Sitelink - {sl['ad_group']} - {sl['link_text']}"

        # Set sitelink asset fields
        asset.sitelink_asset.link_text = sl['link_text']
        asset.sitelink_asset.description1 = sl['description1']
        asset.sitelink_asset.description2 = sl['description2']
        asset.final_urls.append(sl['final_url'])

        operations.append(operation)
        created.append(sl)

    if dry_run:
        print(f"\n[DRY RUN] Would create {len(operations)} sitelink assets:")

        # Group by ad group
        by_ad_group = {}
        for sl in created:
            ag = sl['ad_group']
            if ag not in by_ad_group:
                by_ad_group[ag] = []
            by_ad_group[ag].append(sl)

        for ag, sls in by_ad_group.items():
            print(f"\n  {ag} ({len(sls)} sitelinks):")
            for sl in sls:
                print(f"    - {sl['link_text']}")
                print(f"      D1: {sl['description1']}")
                print(f"      D2: {sl['description2']}")
                print(f"      URL: {sl['final_url']}")

        return None
    else:
        # Execute the operations
        asset_service = client.get_service("AssetService")
        response = asset_service.mutate_assets(
            customer_id=CUSTOMER_ID,
            operations=operations
        )

        # Map resource names back to sitelinks
        results = []
        for i, result in enumerate(response.results):
            results.append({
                'resource_name': result.resource_name,
                'ad_group': created[i]['ad_group'],
                'link_text': created[i]['link_text']
            })

        return results

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

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true', help='Execute (default is dry run)')
    args = parser.parse_args()

    print("=" * 70)
    print("Create Ad Group-Level Sitelink Assets")
    print("=" * 70)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\nLoading sitelink mapping...")
    mapping_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/sitelink_mapping.csv'
    sitelinks = load_sitelink_mapping(mapping_file)
    print(f"  Loaded {len(sitelinks)} sitelinks")

    # Validate all sitelinks
    print("\nValidating sitelink character limits...")
    all_valid = True
    for sl in sitelinks:
        errors = validate_sitelink(sl)
        if errors:
            all_valid = False
            print(f"\n  {sl['ad_group']} - {sl['link_text']}:")
            for e in errors:
                print(f"    ERROR: {e}")

    if all_valid:
        print("  All sitelinks pass validation")

    # Get ad group IDs for reference
    print("\nFetching ad group IDs...")
    ad_group_ids = get_ad_group_ids()
    for name, id in ad_group_ids.items():
        print(f"  {name}: {id}")

    if args.execute:
        print("\n" + "=" * 70)
        print("CREATING SITELINK ASSETS")
        print("=" * 70)

        results = create_sitelink_assets(client, sitelinks, dry_run=False)

        if results:
            print(f"\nSuccessfully created {len(results)} sitelink assets!")

            # Save results for assign_sitelinks.py
            output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/created_sitelink_assets.csv'
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['resource_name', 'ad_group', 'link_text'])
                writer.writeheader()
                writer.writerows(results)

            print(f"\nAsset resource names saved to: {output_file}")
            print("Run assign_sitelinks.py next to link assets to ad groups")
    else:
        print("\n" + "=" * 70)
        print("DRY RUN MODE (use --execute to create assets)")
        print("=" * 70)

        create_sitelink_assets(client, sitelinks, dry_run=True)

        print("\n" + "-" * 70)
        print("Next steps:")
        print("  1. Run with --execute to create assets")
        print("  2. Run assign_sitelinks.py to link assets to ad groups")
