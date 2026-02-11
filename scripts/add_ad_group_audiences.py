"""
Add Ad Group-Level Audience Layering for Search - NonBrand Campaign

This script adds relevant audiences to each ad group in OBSERVATION mode,
allowing bid adjustments based on audience signals without restricting reach.

Audience types supported:
- USER_LIST: First-party audiences (remarketing, customer match)
- CUSTOM_AUDIENCE: Custom segments (search terms, URLs, purchase intent)
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

def load_audience_mapping(filepath):
    """Load audience mapping from CSV"""
    mapping = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping.append({
                'ad_group': row['ad_group'],
                'audience_type': row['audience_type'],
                'audience_id': row['audience_id'],
                'audience_name': row['audience_name'],
                'rationale': row['rationale']
            })

    return mapping

def check_existing_targeting(ad_group_ids):
    """Check what audience targeting already exists at ad group level"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group.id,
        ad_group.name,
        ad_group_criterion.criterion_id,
        ad_group_criterion.type,
        ad_group_criterion.user_list.user_list
    FROM ad_group_criterion
    WHERE campaign.name = 'Search - NonBrand'
    AND ad_group_criterion.type = 'USER_LIST'
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

        existing = set()
        for row in response:
            ag_id = str(row.ad_group.id)
            agc = row.ad_group_criterion

            # Extract the audience ID from the resource name
            if agc.user_list and agc.user_list.user_list:
                # Format: customers/123/userLists/456
                parts = agc.user_list.user_list.split('/')
                if len(parts) >= 4:
                    existing.add((ag_id, 'USER_LIST', parts[-1]))

        return existing
    except Exception as e:
        print(f"  Note: Could not check existing targeting - {e}")
        return set()

def get_campaign_level_user_lists():
    """Get user lists already targeted at campaign level for NonBrand"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        campaign_criterion.user_list.user_list
    FROM campaign_criterion
    WHERE campaign.name = 'Search - NonBrand'
    AND campaign_criterion.type = 'USER_LIST'
    '''

    campaign_lists = set()
    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
        for row in response:
            if row.campaign_criterion.user_list and row.campaign_criterion.user_list.user_list:
                parts = row.campaign_criterion.user_list.user_list.split('/')
                if len(parts) >= 4:
                    campaign_lists.add(parts[-1])
    except Exception as e:
        print(f"  Note: Could not check campaign-level targeting - {e}")

    return campaign_lists

def add_audiences_to_ad_groups(client, mapping, ad_group_ids, existing_targeting, campaign_level_lists, dry_run=True):
    """Add audiences to ad groups in observation mode"""
    operations = []
    to_add = []
    skipped = []

    for item in mapping:
        ag_name = item['ad_group']
        ag_id = ad_group_ids.get(ag_name)

        if not ag_id:
            print(f"  WARNING: Ad group '{ag_name}' not found, skipping")
            continue

        audience_type = item['audience_type']
        audience_id = item['audience_id']

        # Skip CUSTOM_AUDIENCE - not supported for Search campaigns at ad group level
        if audience_type == 'CUSTOM_AUDIENCE':
            skipped.append({
                'ad_group': ag_name,
                'audience_name': item['audience_name'],
                'reason': 'Custom segments not supported for Search ad groups'
            })
            continue

        # Check if this user list is already at campaign level
        if audience_id in campaign_level_lists:
            skipped.append({
                'ad_group': ag_name,
                'audience_name': item['audience_name'],
                'reason': 'Already targeted at campaign level'
            })
            continue

        # Check if this combination already exists at ad group level
        if (ag_id, audience_type, audience_id) in existing_targeting:
            skipped.append({
                'ad_group': ag_name,
                'audience_name': item['audience_name'],
                'reason': 'Already exists at ad group level'
            })
            continue

        # Create the operation
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create

        # Set ad group
        criterion.ad_group = client.get_service("AdGroupService").ad_group_path(
            CUSTOMER_ID, ag_id
        )

        # Set status to ENABLED
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

        # Set bid modifier to 0% (no adjustment initially - gather data first)
        # Use 1.0 for no adjustment, >1.0 for positive, <1.0 for negative
        criterion.bid_modifier = 1.0

        # Set the audience - only USER_LIST supported here
        criterion.user_list.user_list = client.get_service("UserListService").user_list_path(
            CUSTOMER_ID, audience_id
        )

        operations.append(operation)
        to_add.append(item)

    if dry_run:
        print(f"\n[DRY RUN] Would add {len(operations)} audience targeting criteria:")

        # Group by ad group
        by_ag = {}
        for item in to_add:
            ag = item['ad_group']
            if ag not in by_ag:
                by_ag[ag] = []
            by_ag[ag].append(item)

        for ag, items in by_ag.items():
            print(f"\n  {ag} ({len(items)} audiences):")
            for item in items:
                print(f"    + [{item['audience_type']}] {item['audience_name']}")
                print(f"      Rationale: {item['rationale']}")

        if skipped:
            print(f"\n  Skipped {len(skipped)} (already exist):")
            for s in skipped:
                print(f"    - {s['ad_group']}: {s['audience_name']}")

        return None
    else:
        if not operations:
            print("\n  No new audiences to add (all already exist)")
            return None

        # Execute the operations
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=CUSTOMER_ID,
            operations=operations
        )

        return response, to_add, skipped

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true', help='Execute (default is dry run)')
    args = parser.parse_args()

    print("=" * 70)
    print("Add Ad Group-Level Audience Layering")
    print("Campaign: Search - NonBrand")
    print("Mode: Observation (no reach restriction)")
    print("=" * 70)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    # Get ad group IDs
    print("\nFetching ad group IDs...")
    ad_group_ids = get_ad_group_ids()
    for name, id in ad_group_ids.items():
        print(f"  {name}: {id}")

    # Load audience mapping
    print("\nLoading audience mapping...")
    mapping_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/ad_group_audience_mapping.csv'
    mapping = load_audience_mapping(mapping_file)
    print(f"  Loaded {len(mapping)} audience assignments")

    # Check existing targeting
    print("\nChecking existing ad group-level targeting...")
    existing = check_existing_targeting(ad_group_ids)
    print(f"  Found {len(existing)} existing audience criteria")

    # Check campaign-level targeting (to avoid conflicts)
    print("\nChecking campaign-level targeting (to avoid conflicts)...")
    campaign_lists = get_campaign_level_user_lists()
    print(f"  Found {len(campaign_lists)} user lists at campaign level")

    if args.execute:
        print("\n" + "=" * 70)
        print("ADDING AUDIENCE TARGETING")
        print("=" * 70)

        result = add_audiences_to_ad_groups(client, mapping, ad_group_ids, existing, campaign_lists, dry_run=False)

        if result:
            response, added, skipped = result
            print(f"\nSuccessfully added {len(response.results)} audience criteria!")

            for i, res in enumerate(response.results):
                if i < len(added):
                    print(f"  + {added[i]['ad_group']}: {added[i]['audience_name']}")

            if skipped:
                print(f"\nSkipped {len(skipped)} (already existed)")

            print("\n" + "-" * 70)
            print("Verification:")
            print("  Run audit_audiences.py to verify the new targeting")
            print("  Check Google Ads UI to set bid adjustments after gathering data")
    else:
        print("\n" + "=" * 70)
        print("DRY RUN MODE (use --execute to add audiences)")
        print("=" * 70)

        add_audiences_to_ad_groups(client, mapping, ad_group_ids, existing, campaign_lists, dry_run=True)

        print("\n" + "-" * 70)
        print("Next steps:")
        print("  1. Review the audiences above")
        print("  2. Run with --execute to add them")
        print("  3. Monitor performance and set bid adjustments")
