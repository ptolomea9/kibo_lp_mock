"""
Pause thematic ads (Gartner, Forrester, Migration Guide) in NonBrand campaigns
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from google.ads.googleads.client import GoogleAdsClient
from google.protobuf import field_mask_pb2

CUSTOMER_ID = '9948697111'
YAML_PATH = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

# Ad IDs to pause (thematic ads)
THEMATIC_AD_IDS = [
    '785759661800',  # OMS - 10 Signs OMS Guide
    '787531726512',  # OMS - Forrester ROI Study
    '787531726518',  # NB - Manufacturers - Gartner
    '787531726521',  # NB - Wholesalers - Gartner
    '785759661803',  # NB - General B2B - Migration Guide
    '787531726524',  # NB - General B2B - Gartner
    '787531726515',  # NB - Distributors - Gartner
]

def pause_ads(client, dry_run=True):
    """Pause the thematic ads"""
    from ads_mcp.utils import get_googleads_service

    # First get the ad group IDs for these ads
    ga_service = get_googleads_service('GoogleAdsService')

    query = f'''
    SELECT
        ad_group_ad.ad.id,
        ad_group.id,
        ad_group.name,
        ad_group_ad.ad.responsive_search_ad.headlines
    FROM ad_group_ad
    WHERE ad_group_ad.ad.id IN ({', '.join(THEMATIC_AD_IDS)})
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    ads_to_pause = []
    for row in response:
        ad_id = row.ad_group_ad.ad.id
        ag_id = row.ad_group.id
        ag_name = row.ad_group.name
        headlines = [h.text for h in row.ad_group_ad.ad.responsive_search_ad.headlines][:2]

        ads_to_pause.append({
            'ad_id': str(ad_id),
            'ad_group_id': str(ag_id),
            'ad_group_name': ag_name,
            'sample_headline': headlines[0] if headlines else 'Unknown'
        })

    if dry_run:
        print(f"\n[DRY RUN] Would pause {len(ads_to_pause)} ads:")
        for ad in ads_to_pause:
            print(f"  - Ad {ad['ad_id']} in {ad['ad_group_name']}: '{ad['sample_headline']}'")
        return None

    # Create pause operations
    operations = []
    for ad in ads_to_pause:
        operation = client.get_type("AdGroupAdOperation")
        ad_obj = operation.update

        ad_obj.resource_name = client.get_service("AdGroupAdService").ad_group_ad_path(
            CUSTOMER_ID, ad['ad_group_id'], ad['ad_id']
        )
        ad_obj.status = client.enums.AdGroupAdStatusEnum.PAUSED

        operation.update_mask.CopyFrom(
            field_mask_pb2.FieldMask(paths=["status"])
        )

        operations.append(operation)

    # Execute
    ad_group_ad_service = client.get_service("AdGroupAdService")
    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=CUSTOMER_ID,
        operations=operations
    )

    return response

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true', help='Execute pause (default is dry run)')
    args = parser.parse_args()

    print("=" * 60)
    print("Pause Thematic Ads Script")
    print("=" * 60)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    if args.execute:
        print("\nPausing thematic ads...")
        response = pause_ads(client, dry_run=False)
        if response:
            print(f"\nSuccessfully paused {len(response.results)} ads!")
            for result in response.results:
                print(f"  Paused: {result.resource_name}")
    else:
        print("\n[DRY RUN MODE] (use --execute to apply)")
        pause_ads(client, dry_run=True)
