"""
Update HubSpot Conversion Action Lookback Windows

Changes click-through lookback window from 30 days to 90 days
for B2B lead cycle attribution.
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service, _get_googleads_client as get_googleads_client
from google.protobuf import field_mask_pb2
from datetime import datetime

CUSTOMER_ID = '9948697111'

# HubSpot conversion actions to update
HUBSPOT_ACTIONS = [
    {'id': '7388736944', 'name': 'HubSpot - Lead'},
    {'id': '7388666341', 'name': 'HubSpot - MQL'},
]

NEW_LOOKBACK_DAYS = 90


def update_lookback_window(conversion_action_id, name):
    """Update the click-through lookback window for a conversion action"""

    client = get_googleads_client()
    conversion_action_service = client.get_service("ConversionActionService")

    resource_name = f"customers/{CUSTOMER_ID}/conversionActions/{conversion_action_id}"

    operation = client.get_type("ConversionActionOperation")
    conversion_action = operation.update
    conversion_action.resource_name = resource_name
    conversion_action.click_through_lookback_window_days = NEW_LOOKBACK_DAYS

    field_mask = field_mask_pb2.FieldMask(paths=["click_through_lookback_window_days"])
    operation.update_mask.CopyFrom(field_mask)

    try:
        response = conversion_action_service.mutate_conversion_actions(
            customer_id=CUSTOMER_ID,
            operations=[operation]
        )
        print(f"  [OK] {name}: Updated to {NEW_LOOKBACK_DAYS}-day lookback")
        return True
    except Exception as e:
        print(f"  [ERROR] {name}: {str(e)[:100]}")
        return False


def verify_changes():
    """Verify the lookback windows were updated"""
    ga_service = get_googleads_service('GoogleAdsService')

    ids = [a['id'] for a in HUBSPOT_ACTIONS]
    id_filter = ', '.join(ids)

    query = f'''
    SELECT
        conversion_action.id,
        conversion_action.name,
        conversion_action.click_through_lookback_window_days,
        conversion_action.view_through_lookback_window_days
    FROM conversion_action
    WHERE conversion_action.id IN ({id_filter})
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    print("\n  Verification:")
    for row in response:
        ca = row.conversion_action
        print(f"    {ca.name}")
        print(f"      Click-through lookback: {ca.click_through_lookback_window_days} days")
        print(f"      View-through lookback: {ca.view_through_lookback_window_days} days")


if __name__ == '__main__':
    print("=" * 80)
    print("UPDATE HUBSPOT LOOKBACK WINDOWS")
    print(f"Account: {CUSTOMER_ID}")
    print(f"New Lookback: {NEW_LOOKBACK_DAYS} days")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    print("\n  Updating conversion actions...")

    success_count = 0
    for action in HUBSPOT_ACTIONS:
        if update_lookback_window(action['id'], action['name']):
            success_count += 1

    print(f"\n  Updated {success_count}/{len(HUBSPOT_ACTIONS)} conversion actions")

    verify_changes()

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
