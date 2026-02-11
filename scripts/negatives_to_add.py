"""
Generate negative keyword additions based on traffic shaping analysis.
Fixes:
1. B2B ecommerce terms should route to B2B EComm (add negatives to NB - General B2B)
2. Unified commerce terms should route to B2B Other Keywords (add negatives to NB - General B2B)
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
OUTPUT_DIR = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data'

# Negatives to add to NB - General B2B ad group
# These will force traffic to the correct ad groups
NEGATIVES_FOR_GENERAL_B2B = [
    # Route to B2B EComm
    {'keyword': 'b2b ecommerce', 'match_type': 'PHRASE', 'reason': 'Route to B2B EComm'},
    {'keyword': 'b2b e-commerce', 'match_type': 'PHRASE', 'reason': 'Route to B2B EComm'},
    {'keyword': 'b2b ecommerce platform', 'match_type': 'PHRASE', 'reason': 'Route to B2B EComm'},
    {'keyword': 'b2b ecommerce platforms', 'match_type': 'PHRASE', 'reason': 'Route to B2B EComm'},
    {'keyword': 'b2b ecommerce solution', 'match_type': 'PHRASE', 'reason': 'Route to B2B EComm'},
    {'keyword': 'b2b ecommerce solutions', 'match_type': 'PHRASE', 'reason': 'Route to B2B EComm'},
    {'keyword': 'b2b ecommerce software', 'match_type': 'PHRASE', 'reason': 'Route to B2B EComm'},
    {'keyword': 'b2b ecommerce services', 'match_type': 'PHRASE', 'reason': 'Route to B2B EComm'},
    # Route to B2B Other Keywords
    {'keyword': 'unified commerce', 'match_type': 'PHRASE', 'reason': 'Route to B2B Other Keywords'},
    {'keyword': 'composable commerce', 'match_type': 'PHRASE', 'reason': 'Route to B2B Other Keywords'},
    {'keyword': 'headless commerce', 'match_type': 'PHRASE', 'reason': 'Route to B2B Other Keywords'},
]


def get_ad_group_id(ad_group_name):
    """Get ad group ID by name"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = f'''
    SELECT ad_group.id, ad_group.name
    FROM ad_group
    WHERE campaign.name LIKE '%NonBrand%'
    AND ad_group.name = '{ad_group_name}'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in response:
        return row.ad_group.id
    return None


def check_existing_negatives(ad_group_id):
    """Get existing negatives for an ad group"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = f'''
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type
    FROM ad_group_criterion
    WHERE ad_group.id = {ad_group_id}
    AND ad_group_criterion.negative = TRUE
    AND ad_group_criterion.type = 'KEYWORD'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    existing = set()
    for row in response:
        kw = row.ad_group_criterion.keyword.text.lower()
        existing.add(kw)
    return existing


def add_negative_keywords(ad_group_id, negatives):
    """Add negative keywords to an ad group"""
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    ad_group_criterion_service = client.get_service('AdGroupCriterionService')

    operations = []
    for neg in negatives:
        operation = client.get_type('AdGroupCriterionOperation')
        criterion = operation.create

        criterion.ad_group = client.get_service("AdGroupService").ad_group_path(
            CUSTOMER_ID, ad_group_id
        )
        criterion.negative = True
        criterion.keyword.text = neg['keyword']

        match_type_enum = client.enums.KeywordMatchTypeEnum
        if neg['match_type'] == 'PHRASE':
            criterion.keyword.match_type = match_type_enum.PHRASE
        elif neg['match_type'] == 'EXACT':
            criterion.keyword.match_type = match_type_enum.EXACT
        else:
            criterion.keyword.match_type = match_type_enum.BROAD

        operations.append(operation)

    if operations:
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=CUSTOMER_ID,
            operations=operations
        )
        return len(response.results)
    return 0


def main():
    print("=" * 60)
    print("NEGATIVE KEYWORD ADDITIONS FOR TRAFFIC SHAPING")
    print("=" * 60)

    # Get NB - General B2B ad group ID
    print("\nLooking up NB - General B2B ad group...")
    general_b2b_id = get_ad_group_id('NB - General B2B')

    if not general_b2b_id:
        print("ERROR: Could not find NB - General B2B ad group")
        return

    print(f"Found ad group ID: {general_b2b_id}")

    # Check existing negatives
    print("\nChecking existing negatives...")
    existing = check_existing_negatives(general_b2b_id)
    print(f"Found {len(existing)} existing negatives")

    # Filter out already-existing negatives
    to_add = []
    already_exists = []
    for neg in NEGATIVES_FOR_GENERAL_B2B:
        if neg['keyword'].lower() in existing:
            already_exists.append(neg)
        else:
            to_add.append(neg)

    print(f"\nNegatives already present: {len(already_exists)}")
    for neg in already_exists:
        print(f"  - [{neg['keyword']}] (already exists)")

    print(f"\nNegatives to add: {len(to_add)}")
    for neg in to_add:
        print(f"  + [{neg['keyword']}] ({neg['match_type']}) - {neg['reason']}")

    if not to_add:
        print("\nNo new negatives to add.")
        return

    # Confirm before adding
    print("\n" + "-" * 40)
    response = input("Add these negatives? (yes/no): ").strip().lower()

    if response == 'yes':
        print("\nAdding negatives...")
        count = add_negative_keywords(general_b2b_id, to_add)
        print(f"Successfully added {count} negative keywords to NB - General B2B")

        # Save record of what was added
        with open(f'{OUTPUT_DIR}/negatives_added_log.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ad_group', 'keyword', 'match_type', 'reason'])
            writer.writeheader()
            for neg in to_add:
                writer.writerow({
                    'ad_group': 'NB - General B2B',
                    'keyword': neg['keyword'],
                    'match_type': neg['match_type'],
                    'reason': neg['reason']
                })
        print(f"Log saved to: negatives_added_log.csv")
    else:
        print("\nAborted. No changes made.")

        # Save recommendations for manual review
        with open(f'{OUTPUT_DIR}/negatives_recommended.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ad_group', 'keyword', 'match_type', 'reason'])
            writer.writeheader()
            for neg in to_add:
                writer.writerow({
                    'ad_group': 'NB - General B2B',
                    'keyword': neg['keyword'],
                    'match_type': neg['match_type'],
                    'reason': neg['reason']
                })
        print(f"Recommendations saved to: negatives_recommended.csv")


if __name__ == '__main__':
    main()
