"""
Optimize Campaign-Level Audiences for Search - NonBrand

This script:
1. Re-enables 8 paused audiences that are relevant
2. Adds ~10 valuable missing audiences at campaign level
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from google.ads.googleads.client import GoogleAdsClient
from ads_mcp.utils import get_googleads_service

CUSTOMER_ID = '9948697111'
YAML_PATH = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

# Campaign ID for Search - NonBrand
def get_campaign_id():
    """Get campaign ID for Search - NonBrand"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT campaign.id
    FROM campaign
    WHERE campaign.name = 'Search - NonBrand'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in response:
        return str(row.campaign.id)
    return None

# Paused audiences to re-enable (criterion IDs from the audit)
PAUSED_AUDIENCES_TO_ENABLE = [
    {'criterion_id': None, 'user_list_id': '6445966751', 'name': 'High Quality UTMs - 540 days'},
    {'criterion_id': None, 'user_list_id': '605230394', 'name': 'Returning Visitors'},
    {'criterion_id': None, 'user_list_id': '7313720711', 'name': 'Order Management Page Visits Last 90 days'},
    {'criterion_id': None, 'user_list_id': '7314834856', 'name': 'Personalization page visits last 90 days'},
    {'criterion_id': None, 'user_list_id': '7314852397', 'name': 'PPC Landing Page Visitors Last 90 Days'},
    {'criterion_id': None, 'user_list_id': '7315189059', 'name': 'eCommerce Page Visits Last 90 days'},
    {'criterion_id': None, 'user_list_id': '541635811', 'name': 'Ecommerce Visitors - 30 days'},
    {'criterion_id': None, 'user_list_id': '605564938', 'name': 'More than 2 Pages Visited'},
]

# New audiences to add (user list IDs from the audit)
NEW_AUDIENCES_TO_ADD = [
    {'user_list_id': '8145699524', 'name': 'B2B Visitors - L90', 'size': 700},
    {'user_list_id': '9014947107', 'name': '2025 - B2B Commerce - L90', 'size': 370},
    {'user_list_id': '8145697562', 'name': '2025 - Order Management Visitors - L90', 'size': 360},
    {'user_list_id': '9160978168', 'name': 'KIBO Customer Match List 7/16/25', 'size': 300},
    {'user_list_id': '9014377412', 'name': '2025 - Agentic Commerce - L90', 'size': 160},
    {'user_list_id': '9265142234', 'name': 'HubSpot - B2B Target Account List', 'size': 100},
    {'user_list_id': '9013252978', 'name': '2025 - Composable Commerce - L90', 'size': 64},
    {'user_list_id': '9013240258', 'name': '2025 - Headless Commerce - L90', 'size': 64},
    {'user_list_id': '7638278756', 'name': 'OMS Interest - L90', 'size': 0},
    {'user_list_id': '8661834992', 'name': 'Order Management Page Visits Last 90 days - GA4', 'size': 40},
]

def get_paused_criterion_ids():
    """Get criterion IDs for paused audiences"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        campaign_criterion.criterion_id,
        campaign_criterion.user_list.user_list,
        campaign_criterion.status
    FROM campaign_criterion
    WHERE campaign.name = 'Search - NonBrand'
    AND campaign_criterion.type = 'USER_LIST'
    AND campaign_criterion.status = 'PAUSED'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    paused = {}
    for row in response:
        if row.campaign_criterion.user_list and row.campaign_criterion.user_list.user_list:
            parts = row.campaign_criterion.user_list.user_list.split('/')
            if len(parts) >= 4:
                user_list_id = parts[-1]
                paused[user_list_id] = row.campaign_criterion.criterion_id

    return paused

def get_existing_user_list_ids():
    """Get user list IDs already targeted at campaign level"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        campaign_criterion.user_list.user_list
    FROM campaign_criterion
    WHERE campaign.name = 'Search - NonBrand'
    AND campaign_criterion.type = 'USER_LIST'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    existing = set()
    for row in response:
        if row.campaign_criterion.user_list and row.campaign_criterion.user_list.user_list:
            parts = row.campaign_criterion.user_list.user_list.split('/')
            if len(parts) >= 4:
                existing.add(parts[-1])

    return existing

def enable_paused_audiences(client, campaign_id, paused_criterion_ids, dry_run=True):
    """Re-enable paused audiences"""
    operations = []
    to_enable = []

    for aud in PAUSED_AUDIENCES_TO_ENABLE:
        user_list_id = aud['user_list_id']
        criterion_id = paused_criterion_ids.get(user_list_id)

        if not criterion_id:
            print(f"  WARNING: Could not find criterion ID for {aud['name']}, skipping")
            continue

        # Create update operation
        operation = client.get_type("CampaignCriterionOperation")
        criterion = operation.update

        # Set the resource name
        criterion.resource_name = client.get_service("CampaignCriterionService").campaign_criterion_path(
            CUSTOMER_ID, campaign_id, criterion_id
        )

        # Set status to ENABLED
        criterion.status = client.enums.CampaignCriterionStatusEnum.ENABLED

        # Set update mask
        operation.update_mask.paths.append("status")

        operations.append(operation)
        to_enable.append(aud)

    if dry_run:
        print(f"\n[DRY RUN] Would re-enable {len(operations)} paused audiences:")
        for aud in to_enable:
            print(f"  + {aud['name']}")
        return None
    else:
        if not operations:
            print("\n  No paused audiences to enable")
            return None

        campaign_criterion_service = client.get_service("CampaignCriterionService")
        response = campaign_criterion_service.mutate_campaign_criteria(
            customer_id=CUSTOMER_ID,
            operations=operations
        )
        return response, to_enable

def add_new_audiences(client, campaign_id, existing_ids, dry_run=True):
    """Add new audiences at campaign level"""
    operations = []
    to_add = []
    skipped = []

    for aud in NEW_AUDIENCES_TO_ADD:
        user_list_id = aud['user_list_id']

        # Skip if already exists
        if user_list_id in existing_ids:
            skipped.append(aud)
            continue

        # Create operation
        operation = client.get_type("CampaignCriterionOperation")
        criterion = operation.create

        # Set campaign
        criterion.campaign = client.get_service("CampaignService").campaign_path(
            CUSTOMER_ID, campaign_id
        )

        # Set user list
        criterion.user_list.user_list = client.get_service("UserListService").user_list_path(
            CUSTOMER_ID, user_list_id
        )

        # Set status to ENABLED
        criterion.status = client.enums.CampaignCriterionStatusEnum.ENABLED

        # Set bid modifier to 1.0 (no adjustment - gather data first)
        criterion.bid_modifier = 1.0

        operations.append(operation)
        to_add.append(aud)

    if dry_run:
        print(f"\n[DRY RUN] Would add {len(operations)} new audiences:")
        for aud in to_add:
            size_str = f"{aud['size']:,}" if aud['size'] else "N/A"
            print(f"  + {aud['name']} (Size: {size_str})")

        if skipped:
            print(f"\n  Skipped {len(skipped)} (already exist):")
            for aud in skipped:
                print(f"    - {aud['name']}")

        return None
    else:
        if not operations:
            print("\n  No new audiences to add (all already exist)")
            return None

        campaign_criterion_service = client.get_service("CampaignCriterionService")
        response = campaign_criterion_service.mutate_campaign_criteria(
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
    print("Optimize Campaign-Level Audiences")
    print("Campaign: Search - NonBrand")
    print("=" * 70)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    # Get campaign ID
    print("\nFetching campaign ID...")
    campaign_id = get_campaign_id()
    print(f"  Campaign ID: {campaign_id}")

    # Get paused criterion IDs
    print("\nFetching paused audience criterion IDs...")
    paused_ids = get_paused_criterion_ids()
    print(f"  Found {len(paused_ids)} paused audiences")

    # Get existing user list IDs
    print("\nFetching existing audience targeting...")
    existing_ids = get_existing_user_list_ids()
    print(f"  Found {len(existing_ids)} existing audiences")

    if args.execute:
        print("\n" + "=" * 70)
        print("PART 1: RE-ENABLING PAUSED AUDIENCES")
        print("=" * 70)

        result1 = enable_paused_audiences(client, campaign_id, paused_ids, dry_run=False)

        if result1:
            response, enabled = result1
            print(f"\nSuccessfully re-enabled {len(response.results)} audiences:")
            for aud in enabled:
                print(f"  [OK] {aud['name']}")

        print("\n" + "=" * 70)
        print("PART 2: ADDING NEW AUDIENCES")
        print("=" * 70)

        result2 = add_new_audiences(client, campaign_id, existing_ids, dry_run=False)

        if result2:
            response, added, skipped = result2
            print(f"\nSuccessfully added {len(response.results)} new audiences:")
            for aud in added:
                print(f"  [OK] {aud['name']}")

            if skipped:
                print(f"\nSkipped {len(skipped)} (already existed)")

        print("\n" + "=" * 70)
        print("OPTIMIZATION COMPLETE")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Run review_campaign_audiences.py to verify changes")
        print("  2. Monitor performance over 2-4 weeks")
        print("  3. Apply bid adjustments based on audience performance")

    else:
        print("\n" + "=" * 70)
        print("DRY RUN MODE (use --execute to apply changes)")
        print("=" * 70)

        print("\n--- PART 1: RE-ENABLE PAUSED AUDIENCES ---")
        enable_paused_audiences(client, campaign_id, paused_ids, dry_run=True)

        print("\n--- PART 2: ADD NEW AUDIENCES ---")
        add_new_audiences(client, campaign_id, existing_ids, dry_run=True)

        print("\n" + "-" * 70)
        print("Run with --execute to apply these changes")
