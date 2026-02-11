"""
Create new RSA ads from ad_copy_recommendations.csv

Creates 1 new RSA per ad group in Search - NonBrand campaign with:
- DKI headline pinned to position 1
- Gartner/Forrester social proof headlines
- Conversion-focused messaging
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

def load_ad_copy_recommendations(filepath):
    """Load ad copy recommendations grouped by ad group"""
    ad_groups = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ag = row['Ad Group']
            if ag not in ad_groups:
                # Use first row for each ad group as the template
                headlines = []
                for i in range(1, 16):
                    h_col = f'Headline {i}' if i > 1 else 'Headline 1 (DKI)'
                    if h_col in row and row[h_col]:
                        headlines.append(row[h_col])

                descriptions = []
                for i in range(1, 5):
                    d_col = f'Description {i}'
                    if d_col in row and row[d_col]:
                        descriptions.append(row[d_col])

                # Get landing page URL - ensure it starts with https
                url = row.get('Landing Page URL', '')
                if not url.startswith('http'):
                    # Default URL based on ad group
                    default_urls = {
                        'OMS': 'https://kibocommerce.com/platform/order-management/',
                        'NB - Manufacturers': 'https://kibocommerce.com/ppc/manufacturing/',
                        'NB - Wholesalers': 'https://kibocommerce.com/ppc/wholesale/',
                        'NB - General B2B': 'https://kibocommerce.com/solutions/b2b/',
                        'NB - Distributors': 'https://kibocommerce.com/ppc/distributor/',
                    }
                    url = default_urls.get(ag, 'https://kibocommerce.com/')

                ad_groups[ag] = {
                    'headlines': headlines[:15],  # Max 15
                    'descriptions': descriptions[:4],  # Max 4
                    'final_url': url,
                    'h1_pin': row.get('H1 Pin Position', '1'),
                    'd1_pin': row.get('D1 Pin Position', '1')
                }

    return ad_groups

def create_rsas(client, ad_group_ids, ad_copy, dry_run=True):
    """Create new RSA ads"""
    operations = []
    created = []

    for ag_name, copy in ad_copy.items():
        ag_id = ad_group_ids.get(ag_name)
        if not ag_id:
            print(f"  WARNING: Ad group '{ag_name}' not found, skipping")
            continue

        # Create ad operation
        operation = client.get_type("AdGroupAdOperation")
        ad_group_ad = operation.create

        # Set ad group
        ad_group_ad.ad_group = client.get_service("AdGroupService").ad_group_path(
            CUSTOMER_ID, ag_id
        )

        # Set status
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

        # Create RSA
        rsa = ad_group_ad.ad.responsive_search_ad

        # Add headlines (with pinning for DKI)
        for i, headline_text in enumerate(copy['headlines']):
            # Check if it's a DKI headline
            is_dki = '{' in headline_text and '}' in headline_text

            if is_dki:
                # Don't truncate DKI - if too long, use shorter default
                if len(headline_text) > 30:
                    # Try to shorten the default text inside the DKI
                    import re
                    match = re.match(r'\{KeyWord:(.+)\}', headline_text)
                    if match:
                        default = match.group(1)
                        # Shorten default to fit
                        max_default_len = 30 - len('{KeyWord:}')
                        short_default = default[:max_default_len]
                        headline_text = f'{{KeyWord:{short_default}}}'
            elif len(headline_text) > 30:
                # Truncate non-DKI headlines
                headline_text = headline_text[:27] + '...'

            headline = client.get_type("AdTextAsset")
            headline.text = headline_text

            # Pin position 1 for DKI headline
            if i == 0 and is_dki:
                headline.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1

            rsa.headlines.append(headline)

        # Add descriptions (with pinning for D1)
        for i, desc_text in enumerate(copy['descriptions']):
            if len(desc_text) > 90:
                desc_text = desc_text[:87] + '...'

            description = client.get_type("AdTextAsset")
            description.text = desc_text

            # Pin position 1 for first description
            if i == 0:
                description.pinned_field = client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_1

            rsa.descriptions.append(description)

        # Set final URLs
        ad_group_ad.ad.final_urls.append(copy['final_url'])

        operations.append(operation)
        created.append({
            'ad_group': ag_name,
            'headlines': len(copy['headlines']),
            'descriptions': len(copy['descriptions']),
            'url': copy['final_url']
        })

    if dry_run:
        print(f"\n[DRY RUN] Would create {len(operations)} RSA ads:")
        for c in created:
            print(f"\n  {c['ad_group']}:")
            print(f"    Headlines: {c['headlines']}")
            print(f"    Descriptions: {c['descriptions']}")
            print(f"    URL: {c['url']}")
        return None
    else:
        ad_group_ad_service = client.get_service("AdGroupAdService")
        response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=CUSTOMER_ID,
            operations=operations
        )
        return response, created

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true', help='Execute (default is dry run)')
    args = parser.parse_args()

    print("=" * 60)
    print("Create New RSA Ads from Recommendations")
    print("=" * 60)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\nGetting ad group IDs...")
    ad_group_ids = get_ad_group_ids()
    print(f"  Found: {list(ad_group_ids.keys())}")

    print("\nLoading ad copy recommendations...")
    ad_copy_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/ad_copy_recommendations.csv'
    ad_copy = load_ad_copy_recommendations(ad_copy_file)
    print(f"  Found copy for {len(ad_copy)} ad groups: {list(ad_copy.keys())}")

    # Filter to only NonBrand ad groups
    nonbrand_ag = ['OMS', 'NB - Manufacturers', 'NB - Wholesalers', 'NB - General B2B', 'NB - Distributors']
    filtered_copy = {k: v for k, v in ad_copy.items() if k in nonbrand_ag}
    print(f"  Filtered to NonBrand: {list(filtered_copy.keys())}")

    if args.execute:
        print("\n" + "=" * 60)
        print("CREATING RSA ADS")
        print("=" * 60)

        result = create_rsas(client, ad_group_ids, filtered_copy, dry_run=False)
        if result:
            response, created = result
            print(f"\nSuccessfully created {len(response.results)} RSA ads!")
            for i, res in enumerate(response.results):
                print(f"  Created: {res.resource_name}")
                if i < len(created):
                    print(f"    Ad Group: {created[i]['ad_group']}")
    else:
        print("\n" + "=" * 60)
        print("DRY RUN MODE (use --execute to create ads)")
        print("=" * 60)

        create_rsas(client, ad_group_ids, filtered_copy, dry_run=True)
