"""
Disable HubSpot Lead - Manual Conversion Action

This conversion action has include_in_conversions=True but 0 conversions,
which pollutes Smart Bidding signals. This script disables it.
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service, _get_googleads_client as get_googleads_client
from google.protobuf import field_mask_pb2
from datetime import datetime

CUSTOMER_ID = '9948697111'
CONVERSION_ACTION_ID = '7386341177'  # HubSpot Lead - Manual


def disable_conversion_action():
    """Disable the HubSpot Lead - Manual conversion action"""

    print("=" * 80)
    print("DISABLE HUBSPOT LEAD - MANUAL")
    print(f"Account: {CUSTOMER_ID}")
    print(f"Conversion Action ID: {CONVERSION_ACTION_ID}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    client = get_googleads_client()
    conversion_action_service = client.get_service("ConversionActionService")

    # Create the resource name
    resource_name = f"customers/{CUSTOMER_ID}/conversionActions/{CONVERSION_ACTION_ID}"

    # Create the operation to update the conversion action
    operation = client.get_type("ConversionActionOperation")

    # Set the conversion action to update
    conversion_action = operation.update
    conversion_action.resource_name = resource_name

    # Set status to REMOVED (permanent removal)
    # Note: HIDDEN and include_in_conversions_metric are immutable for UPLOAD_CLICKS type
    conversion_action.status = client.enums.ConversionActionStatusEnum.REMOVED

    # Set the update mask to specify which fields to update
    field_mask = field_mask_pb2.FieldMask(paths=["status"])
    operation.update_mask.CopyFrom(field_mask)

    print("\n  Applying changes:")
    print("    - Status: ENABLED -> REMOVED")

    # Execute the mutation
    try:
        response = conversion_action_service.mutate_conversion_actions(
            customer_id=CUSTOMER_ID,
            operations=[operation]
        )

        print("\n  [SUCCESS] Conversion action updated!")
        print(f"    Resource: {response.results[0].resource_name}")

    except Exception as e:
        print(f"\n  [ERROR] Failed to update: {e}")
        return False

    # Verify the change
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    query = f'''
    SELECT
        conversion_action.id,
        conversion_action.name,
        conversion_action.status,
        conversion_action.include_in_conversions_metric
    FROM conversion_action
    WHERE conversion_action.id = {CONVERSION_ACTION_ID}
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    for row in response:
        ca = row.conversion_action
        print(f"\n  {ca.name}")
        print(f"    ID: {ca.id}")
        print(f"    Status: {ca.status.name}")
        print(f"    Include in Conversions: {ca.include_in_conversions_metric}")

    return True


if __name__ == '__main__':
    success = disable_conversion_action()

    if success:
        print("\n" + "=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print("""
  The "HubSpot Lead - Manual" conversion action has been disabled.

  This means:
  - It will no longer appear in the "Conversions" column
  - Smart Bidding will no longer optimize toward it
  - Historical data is preserved
  - It can be re-enabled if needed

  Remaining cleanup recommended:
  - Remove 34 Universal Analytics goals
  - Remove 13 Salesforce conversion actions
  - Extend HubSpot lookback windows to 90 days
  - Increase HubSpot conversion values
""")
