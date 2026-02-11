"""
Salesforce Integration Diagnostic Script

Checks the status of Salesforce-Google Ads integration:
1. Linked Salesforce accounts
2. Salesforce conversion action details
3. Recent conversion data (if any)
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
from datetime import datetime, timedelta

CUSTOMER_ID = '9948697111'


def check_salesforce_link():
    """Check if Salesforce is linked to this Google Ads account"""
    print("\n" + "=" * 80)
    print("1. CHECKING SALESFORCE ACCOUNT LINK")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    # Query for third-party app analytics links (includes Salesforce)
    query = '''
    SELECT
        third_party_app_analytics_link.resource_name,
        third_party_app_analytics_link.shareable_link_id
    FROM third_party_app_analytics_link
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
        links = list(response)
        if links:
            print(f"  Found {len(links)} third-party app links")
            for link in links:
                print(f"    - {link.third_party_app_analytics_link.resource_name}")
        else:
            print("  No third-party app analytics links found")
    except Exception as e:
        print(f"  Could not query third-party links: {str(e)[:100]}")

    # Check for data partner links
    query2 = '''
    SELECT
        data_link.resource_name,
        data_link.data_link_id,
        data_link.product_link_id
    FROM data_link
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query2)
        links = list(response)
        if links:
            print(f"\n  Found {len(links)} data links:")
            for link in links:
                print(f"    - ID: {link.data_link.data_link_id}")
        else:
            print("\n  No data links found")
    except Exception as e:
        print(f"\n  Could not query data links: {str(e)[:100]}")


def get_salesforce_conversion_details():
    """Get detailed info on Salesforce conversion actions"""
    print("\n" + "=" * 80)
    print("2. SALESFORCE CONVERSION ACTION DETAILS")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        conversion_action.id,
        conversion_action.name,
        conversion_action.type,
        conversion_action.status,
        conversion_action.primary_for_goal,
        conversion_action.include_in_conversions_metric,
        conversion_action.value_settings.default_value,
        conversion_action.attribution_model_settings.attribution_model,
        conversion_action.click_through_lookback_window_days
    FROM conversion_action
    WHERE conversion_action.type = 'SALESFORCE'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    sf_actions = []
    for row in response:
        ca = row.conversion_action
        sf_actions.append({
            'id': ca.id,
            'name': ca.name,
            'status': ca.status.name,
            'primary': ca.primary_for_goal,
            'include_in_conv': ca.include_in_conversions_metric,
            'default_value': ca.value_settings.default_value if ca.value_settings else 0,
            'attribution': ca.attribution_model_settings.attribution_model.name if ca.attribution_model_settings else 'N/A',
            'lookback': ca.click_through_lookback_window_days
        })

    print(f"\n  Found {len(sf_actions)} Salesforce conversion actions:\n")

    for action in sf_actions:
        primary_flag = "[PRIMARY]" if action['primary'] else ""
        include_flag = "[IN CONVERSIONS]" if action['include_in_conv'] else ""
        print(f"  {action['name']} {primary_flag} {include_flag}")
        print(f"    ID: {action['id']}")
        print(f"    Status: {action['status']}")
        print(f"    Default Value: ${action['default_value']}")
        print(f"    Attribution: {action['attribution']}")
        print(f"    Lookback: {action['lookback']} days")
        print()

    return sf_actions


def check_salesforce_conversion_data():
    """Check if any Salesforce conversions have been recorded"""
    print("\n" + "=" * 80)
    print("3. SALESFORCE CONVERSION DATA (Last 180 Days)")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    # Check last 180 days for any Salesforce conversion data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    date_range = f"segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'"

    query = f'''
    SELECT
        segments.conversion_action_name,
        segments.conversion_action,
        metrics.conversions,
        metrics.all_conversions,
        metrics.conversions_value
    FROM customer
    WHERE {date_range}
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    # Filter for Salesforce-related conversions
    sf_keywords = ['salesforce', 'sf:', 'lead converted', 'working lead', 'working opportunity', 'won opportunity']

    sf_data = {}
    for row in response:
        name = row.segments.conversion_action_name.lower()
        if any(kw in name for kw in sf_keywords):
            if row.segments.conversion_action_name not in sf_data:
                sf_data[row.segments.conversion_action_name] = {
                    'conversions': 0,
                    'all_conversions': 0,
                    'value': 0
                }
            sf_data[row.segments.conversion_action_name]['conversions'] += row.metrics.conversions
            sf_data[row.segments.conversion_action_name]['all_conversions'] += row.metrics.all_conversions
            sf_data[row.segments.conversion_action_name]['value'] += row.metrics.conversions_value

    if sf_data:
        print(f"\n  Salesforce conversion data found:\n")
        for name, data in sf_data.items():
            print(f"  {name}")
            print(f"    Conversions: {data['conversions']:.1f}")
            print(f"    All Conversions: {data['all_conversions']:.1f}")
            print(f"    Value: ${data['value']:.2f}")
            print()
    else:
        print("\n  [!] NO Salesforce conversion data in last 180 days")
        print("      This confirms the integration is NOT working.")


def check_offline_conversion_uploads():
    """Check for any offline conversion upload jobs"""
    print("\n" + "=" * 80)
    print("4. OFFLINE CONVERSION UPLOAD HISTORY")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    # Check for offline user data jobs (includes Salesforce uploads)
    query = '''
    SELECT
        offline_user_data_job.resource_name,
        offline_user_data_job.id,
        offline_user_data_job.status,
        offline_user_data_job.type,
        offline_user_data_job.failure_reason
    FROM offline_user_data_job
    ORDER BY offline_user_data_job.id DESC
    LIMIT 20
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
        jobs = list(response)

        if jobs:
            print(f"\n  Found {len(jobs)} recent offline data jobs:\n")
            for job in jobs:
                j = job.offline_user_data_job
                status = j.status.name if j.status else 'UNKNOWN'
                job_type = j.type.name if j.type else 'UNKNOWN'
                failure = j.failure_reason.name if j.failure_reason else 'None'
                print(f"  Job ID: {j.id}")
                print(f"    Type: {job_type}")
                print(f"    Status: {status}")
                print(f"    Failure Reason: {failure}")
                print()
        else:
            print("\n  No offline data upload jobs found")
            print("  This suggests Salesforce is not actively uploading conversion data")
    except Exception as e:
        print(f"\n  Could not query offline jobs: {str(e)[:100]}")


def check_account_links():
    """Check all account links including CRM"""
    print("\n" + "=" * 80)
    print("5. ACCOUNT LINKS OVERVIEW")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    # Check Google Analytics links
    query_ga = '''
    SELECT
        google_ads_link.resource_name,
        google_ads_link.customer
    FROM google_ads_link
    '''

    # Check account links
    print("\n  Checking for linked accounts...")

    # Try to get customer client links (for MCC structure)
    query_customer = '''
    SELECT
        customer.id,
        customer.descriptive_name,
        customer.manager,
        customer.test_account
    FROM customer
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query_customer)
        for row in response:
            c = row.customer
            print(f"\n  Account: {c.descriptive_name}")
            print(f"    ID: {c.id}")
            print(f"    Is Manager: {c.manager}")
            print(f"    Is Test: {c.test_account}")
    except Exception as e:
        print(f"  Error: {str(e)[:100]}")


def provide_diagnosis():
    """Provide diagnosis and next steps"""
    print("\n" + "=" * 80)
    print("DIAGNOSIS & NEXT STEPS")
    print("=" * 80)

    print("""
  LIKELY ISSUE: Salesforce integration is not actively syncing data.

  POSSIBLE CAUSES:

  1. SALESFORCE CONNECTOR NOT SET UP
     - Go to Google Ads > Tools & Settings > Linked accounts
     - Look for "Salesforce" under "Third-party app analytics"
     - If not there, the integration was never completed

  2. GCLID NOT BEING CAPTURED
     - When users click ads, a 'gclid' parameter is added to the URL
     - Your website forms need to capture this and send to Salesforce
     - Check: Do your Salesforce Lead records have GCLID values?

  3. USING HUBSPOT AS MIDDLE LAYER
     - You have active HubSpot conversion uploads (HubSpot - Lead, HubSpot - MQL)
     - The Salesforce actions may be LEGACY from before HubSpot integration
     - HubSpot may now be the CRM sending conversion data to Google Ads

  RECOMMENDED ACTIONS:

  A. If using HubSpot as primary CRM integration:
     - DISABLE all Salesforce conversion actions
     - Keep HubSpot - Lead and HubSpot - MQL as primary
     - The Salesforce actions are orphaned/legacy

  B. If you want Salesforce integration to work:
     - Set up Salesforce connector in Google Ads
     - Add GCLID field to Salesforce Lead object
     - Configure forms to capture and pass GCLID
     - Map Salesforce lead stages to Google Ads conversion actions

  C. Quick fix (if Salesforce not needed):
     - Set all 13 Salesforce actions to HIDDEN or REMOVED
     - This cleans up your conversion actions list
     - Continue using HubSpot for offline conversion tracking
""")


if __name__ == '__main__':
    print("=" * 80)
    print("KIBO COMMERCE - SALESFORCE INTEGRATION DIAGNOSTIC")
    print(f"Account ID: {CUSTOMER_ID}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    check_salesforce_link()
    get_salesforce_conversion_details()
    check_salesforce_conversion_data()
    check_offline_conversion_uploads()
    check_account_links()
    provide_diagnosis()
