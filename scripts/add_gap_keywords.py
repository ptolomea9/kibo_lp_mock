"""
Add 33 gap keywords as Broad match with keyword-level URLs
Plus ad group-level negative keywords for traffic shaping
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from google.ads.googleads.client import GoogleAdsClient
from google.protobuf import field_mask_pb2

CUSTOMER_ID = '9948697111'
YAML_PATH = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

# Ad group IDs from the account
AD_GROUP_IDS = {
    'OMS': '168315915888',  # Will get dynamically
    'NB - General B2B': '183052168626'  # Will get dynamically
}

# Keywords to add
KEYWORDS_TO_ADD = [
    # OMS ad group keywords
    {'keyword': 'order orchestration platform', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/inventory-promising/'},
    {'keyword': 'fulfillment optimization software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/order-management/'},
    {'keyword': 'real-time inventory visibility', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/inventory-visibility/'},
    {'keyword': 'inventory visibility software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/inventory-visibility/'},
    {'keyword': 'atp ctp software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/inventory-promising/'},
    {'keyword': 'returns management software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/reverse-logistics/'},
    {'keyword': 'reverse logistics software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/reverse-logistics/'},
    {'keyword': 'ai commerce platform', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/agentic-commerce/'},
    {'keyword': 'ai order management', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/order-management/'},
    {'keyword': 'estimated delivery date software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/inventory-promising/'},
    {'keyword': 'available to promise software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/inventory-promising/'},
    {'keyword': 'curbside pickup software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/order-management/'},
    {'keyword': 'rma software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/reverse-logistics/'},
    {'keyword': 'endless aisle software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/dropship/'},
    {'keyword': 'delivery date promise software', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/inventory-promising/'},
    {'keyword': 'd2c order management', 'ad_group': 'OMS', 'url': 'https://kibocommerce.com/platform/order-management/'},

    # NB - General B2B ad group keywords
    {'keyword': 'unified commerce software', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/'},
    {'keyword': 'enterprise ecommerce platform', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/b2b/'},
    {'keyword': 'modular commerce platform', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/b2b/'},
    {'keyword': 'b2b customer portal software', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/b2b/'},
    {'keyword': 'b2b self service portal', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/ppc/wholesale/#b2b-commerce'},
    {'keyword': 'quote to cash software', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/b2b/'},
    {'keyword': 'b2b pricing software', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/platform/catalog-price-promo/'},
    {'keyword': 'b2b account management software', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/b2b/'},
    {'keyword': 'ai search ecommerce', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/platform/ai-search/'},
    {'keyword': 'ecommerce ai search', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/platform/ai-search/'},
    {'keyword': 'mach architecture ecommerce', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/b2b/'},
    {'keyword': 'contract pricing software', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/b2b/'},
    {'keyword': 'grocery ecommerce platform', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/grocery/'},
    {'keyword': 'auto parts ecommerce', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/auto-parts/'},
    {'keyword': 'apparel ecommerce platform', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/solutions/apparel-and-fashion/'},
    {'keyword': 'recurring revenue platform', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/platform/subscription/'},
    {'keyword': 'd2c ecommerce platform', 'ad_group': 'NB - General B2B', 'url': 'https://kibocommerce.com/platform/commerce/'},
]

# Recommended negative keywords for traffic shaping
NEGATIVES_TO_ADD = {
    # Add OMS-specific negatives to NB - General B2B
    'NB - General B2B': [
        'order management',
        'oms',
        'fulfillment',
        'inventory visibility',
        'reverse logistics',
        'returns management',
    ],
    # Add B2B commerce negatives to OMS (if needed)
    'OMS': [
        # OMS already has extensive negatives, may not need more
    ]
}

def get_ad_group_ids(client):
    """Get ad group IDs dynamically"""
    from ads_mcp.utils import get_googleads_service
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT ad_group.id, ad_group.name
    FROM ad_group
    WHERE campaign.name = 'Search - NonBrand'
    AND ad_group.name IN ('OMS', 'NB - General B2B')
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    ids = {}
    for row in response:
        ids[row.ad_group.name] = str(row.ad_group.id)
    return ids

def add_keywords(client, ad_group_ids, dry_run=True):
    """Add keywords as Broad match with keyword-level URLs"""
    operations = []

    for kw_data in KEYWORDS_TO_ADD:
        ag_name = kw_data['ad_group']
        ag_id = ad_group_ids.get(ag_name)

        if not ag_id:
            print(f"  WARNING: Ad group '{ag_name}' not found, skipping {kw_data['keyword']}")
            continue

        # Create keyword criterion
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create

        criterion.ad_group = client.get_service("AdGroupService").ad_group_path(
            CUSTOMER_ID, ag_id
        )

        # Set keyword text and match type (BROAD)
        criterion.keyword.text = kw_data['keyword']
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD

        # Set keyword-level Final URL
        criterion.final_urls.append(kw_data['url'])

        # Set status to ENABLED
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

        operations.append(operation)

    if dry_run:
        print(f"\n[DRY RUN] Would add {len(operations)} keywords:")
        by_ag = {}
        for kw_data in KEYWORDS_TO_ADD:
            ag = kw_data['ad_group']
            if ag not in by_ag:
                by_ag[ag] = []
            by_ag[ag].append(kw_data['keyword'])

        for ag, kws in by_ag.items():
            print(f"\n  {ag} ({len(kws)} keywords):")
            for kw in kws[:5]:
                print(f"    - {kw}")
            if len(kws) > 5:
                print(f"    ... +{len(kws)-5} more")
        return None
    else:
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=CUSTOMER_ID,
            operations=operations
        )
        return response

def add_negatives(client, ad_group_ids, dry_run=True):
    """Add ad group level negative keywords"""
    operations = []

    for ag_name, negatives in NEGATIVES_TO_ADD.items():
        if not negatives:
            continue

        ag_id = ad_group_ids.get(ag_name)
        if not ag_id:
            continue

        for neg_kw in negatives:
            operation = client.get_type("AdGroupCriterionOperation")
            criterion = operation.create

            criterion.ad_group = client.get_service("AdGroupService").ad_group_path(
                CUSTOMER_ID, ag_id
            )

            criterion.keyword.text = neg_kw
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            criterion.negative = True

            operations.append(operation)

    if dry_run:
        if operations:
            print(f"\n[DRY RUN] Would add {len(operations)} negative keywords:")
            for ag_name, negatives in NEGATIVES_TO_ADD.items():
                if negatives:
                    print(f"\n  {ag_name}:")
                    for neg in negatives:
                        print(f"    - {neg}")
        return None
    else:
        if operations:
            ad_group_criterion_service = client.get_service("AdGroupCriterionService")
            response = ad_group_criterion_service.mutate_ad_group_criteria(
                customer_id=CUSTOMER_ID,
                operations=operations
            )
            return response
        return None

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true', help='Execute changes (default is dry run)')
    parser.add_argument('--skip-negatives', action='store_true', help='Skip adding negative keywords')
    args = parser.parse_args()

    print("=" * 70)
    print("Add Gap Keywords Script")
    print("Match Type: BROAD")
    print("=" * 70)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\nGetting ad group IDs...")
    ad_group_ids = get_ad_group_ids(client)
    print(f"  Found: {ad_group_ids}")

    if args.execute:
        print("\n" + "=" * 70)
        print("EXECUTING KEYWORD ADDITIONS")
        print("=" * 70)

        response = add_keywords(client, ad_group_ids, dry_run=False)
        if response:
            print(f"\nSuccessfully added {len(response.results)} keywords!")

        if not args.skip_negatives:
            print("\nAdding negative keywords...")
            neg_response = add_negatives(client, ad_group_ids, dry_run=False)
            if neg_response:
                print(f"Added {len(neg_response.results)} negative keywords")
    else:
        print("\n" + "=" * 70)
        print("DRY RUN MODE (use --execute to apply changes)")
        print("=" * 70)

        add_keywords(client, ad_group_ids, dry_run=True)

        if not args.skip_negatives:
            add_negatives(client, ad_group_ids, dry_run=True)
