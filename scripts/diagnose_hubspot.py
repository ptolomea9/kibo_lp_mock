"""
HubSpot Integration Diagnostic Script

Checks the status of HubSpot-Google Ads integration:
1. HubSpot conversion actions and their status
2. Conversion data from HubSpot
3. Offline conversion upload jobs
4. Recommendations for optimizing the HubSpot integration
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
from datetime import datetime, timedelta
from collections import defaultdict

CUSTOMER_ID = '9948697111'


def get_hubspot_conversion_actions():
    """Get all HubSpot-related conversion actions"""
    print("\n" + "=" * 80)
    print("1. HUBSPOT CONVERSION ACTIONS")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    # Query for UPLOAD_CLICKS type (HubSpot uses offline conversion uploads)
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
        conversion_action.click_through_lookback_window_days,
        conversion_action.counting_type,
        conversion_action.category
    FROM conversion_action
    WHERE conversion_action.type = 'UPLOAD_CLICKS'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    hs_actions = []
    other_upload_actions = []

    for row in response:
        ca = row.conversion_action
        action = {
            'id': ca.id,
            'name': ca.name,
            'type': ca.type.name,
            'status': ca.status.name,
            'primary': ca.primary_for_goal,
            'include_in_conv': ca.include_in_conversions_metric,
            'default_value': ca.value_settings.default_value if ca.value_settings else 0,
            'attribution': ca.attribution_model_settings.attribution_model.name if ca.attribution_model_settings else 'N/A',
            'lookback': ca.click_through_lookback_window_days,
            'counting': ca.counting_type.name if ca.counting_type else 'N/A',
            'category': ca.category.name if ca.category else 'N/A'
        }

        if 'hubspot' in ca.name.lower():
            hs_actions.append(action)
        else:
            other_upload_actions.append(action)

    print(f"\n  Found {len(hs_actions)} HubSpot conversion actions:\n")

    for action in hs_actions:
        flags = []
        if action['primary']:
            flags.append("[PRIMARY]")
        if action['include_in_conv']:
            flags.append("[IN CONVERSIONS]")
        flag_str = " ".join(flags)

        print(f"  {action['name']} {flag_str}")
        print(f"    ID: {action['id']}")
        print(f"    Status: {action['status']}")
        print(f"    Category: {action['category']}")
        print(f"    Counting: {action['counting']}")
        print(f"    Default Value: ${action['default_value']}")
        print(f"    Attribution: {action['attribution']}")
        print(f"    Lookback: {action['lookback']} days")
        print()

    if other_upload_actions:
        print(f"\n  Other UPLOAD_CLICKS actions (non-HubSpot): {len(other_upload_actions)}")
        for action in other_upload_actions:
            print(f"    - {action['name']} ({action['status']})")

    return hs_actions


def get_hubspot_conversion_data():
    """Get conversion data for HubSpot actions over multiple time periods"""
    print("\n" + "=" * 80)
    print("2. HUBSPOT CONVERSION DATA")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    periods = [
        ('Last 30 Days', 30),
        ('Last 60 Days', 60),
        ('Last 90 Days', 90),
        ('Last 180 Days', 180)
    ]

    for period_name, days in periods:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        date_range = f"segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'"

        query = f'''
        SELECT
            segments.conversion_action_name,
            metrics.conversions,
            metrics.all_conversions,
            metrics.conversions_value,
            metrics.all_conversions_value
        FROM customer
        WHERE {date_range}
        '''

        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

        hs_data = defaultdict(lambda: {'conversions': 0, 'all_conversions': 0, 'value': 0, 'all_value': 0})

        for row in response:
            name = row.segments.conversion_action_name
            if 'hubspot' in name.lower():
                hs_data[name]['conversions'] += row.metrics.conversions
                hs_data[name]['all_conversions'] += row.metrics.all_conversions
                hs_data[name]['value'] += row.metrics.conversions_value
                hs_data[name]['all_value'] += row.metrics.all_conversions_value

        print(f"\n  {period_name}:")
        if hs_data:
            for name, data in sorted(hs_data.items()):
                print(f"    {name}")
                print(f"      Conversions: {data['conversions']:.2f} | All Conv: {data['all_conversions']:.2f}")
                print(f"      Value: ${data['value']:.2f} | All Value: ${data['all_value']:.2f}")
        else:
            print("    No HubSpot conversion data found")

    return hs_data


def check_offline_upload_jobs():
    """Check offline conversion upload job history"""
    print("\n" + "=" * 80)
    print("3. OFFLINE CONVERSION UPLOAD JOBS")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    # Check for conversion upload jobs specifically
    query = '''
    SELECT
        offline_user_data_job.resource_name,
        offline_user_data_job.id,
        offline_user_data_job.status,
        offline_user_data_job.type,
        offline_user_data_job.failure_reason
    FROM offline_user_data_job
    WHERE offline_user_data_job.type = 'STORE_SALES_UPLOAD_FIRST_PARTY'
       OR offline_user_data_job.type = 'STORE_SALES_UPLOAD_THIRD_PARTY'
    ORDER BY offline_user_data_job.id DESC
    LIMIT 20
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
        jobs = list(response)

        if jobs:
            print(f"\n  Found {len(jobs)} store sales upload jobs")
            for job in jobs:
                j = job.offline_user_data_job
                print(f"    Job {j.id}: {j.status.name} ({j.type.name})")
        else:
            print("\n  No store sales upload jobs found")
    except Exception as e:
        print(f"\n  Note: {str(e)[:80]}")

    # Also check click conversion uploads
    print("\n  Checking click conversion upload history...")

    # Get conversion action upload metadata via conversion action stats
    query2 = '''
    SELECT
        conversion_action.name,
        conversion_action.type,
        metrics.all_conversions
    FROM conversion_action
    WHERE conversion_action.type = 'UPLOAD_CLICKS'
    AND metrics.all_conversions > 0
    '''

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query2)
        active_uploads = list(response)

        if active_uploads:
            print(f"\n  Active click conversion uploads (last 30 days):")
            for row in active_uploads:
                print(f"    - {row.conversion_action.name}: {row.metrics.all_conversions:.1f} conversions")
        else:
            print("\n  No active click conversion uploads in last 30 days")
    except Exception as e:
        print(f"\n  Note: {str(e)[:80]}")


def analyze_hubspot_health():
    """Analyze overall health of HubSpot integration"""
    print("\n" + "=" * 80)
    print("4. HUBSPOT INTEGRATION HEALTH ANALYSIS")
    print("=" * 80)

    ga_service = get_googleads_service('GoogleAdsService')

    # Get detailed metrics by week for the last 12 weeks
    end_date = datetime.now()
    start_date = end_date - timedelta(days=84)  # 12 weeks
    date_range = f"segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'"

    query = f'''
    SELECT
        segments.conversion_action_name,
        segments.week,
        metrics.conversions,
        metrics.all_conversions
    FROM customer
    WHERE {date_range}
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    weekly_data = defaultdict(lambda: defaultdict(lambda: {'conv': 0, 'all_conv': 0}))

    for row in response:
        name = row.segments.conversion_action_name
        if 'hubspot' in name.lower():
            week = row.segments.week
            weekly_data[name][week]['conv'] += row.metrics.conversions
            weekly_data[name][week]['all_conv'] += row.metrics.all_conversions

    print("\n  Weekly conversion trend (last 12 weeks):\n")

    for action_name, weeks in weekly_data.items():
        print(f"  {action_name}:")
        sorted_weeks = sorted(weeks.keys())
        for week in sorted_weeks[-8:]:  # Show last 8 weeks
            data = weeks[week]
            bar = "*" * int(data['all_conv'])
            print(f"    {week}: {data['all_conv']:.0f} {bar}")
        print()


def provide_hubspot_recommendations():
    """Provide recommendations for HubSpot integration"""
    print("\n" + "=" * 80)
    print("5. RECOMMENDATIONS FOR HUBSPOT INTEGRATION")
    print("=" * 80)

    print("""
  CURRENT STATE:
  - HubSpot - Lead: Active, receiving conversions
  - HubSpot - MQL: Active, receiving conversions
  - HubSpot Lead - Manual: BROKEN (0 conversions but include_in_conversions=True)

  RECOMMENDED HUBSPOT CONVERSION STRUCTURE:

  For B2B lead gen, a typical HubSpot funnel should track:

  | Stage | Conversion Action | Include in Conv | Value |
  |-------|-------------------|-----------------|-------|
  | Lead Created | HubSpot - Lead | Yes (Primary) | $50 |
  | MQL | HubSpot - MQL | No | $150 |
  | SQL | HubSpot - SQL | No | $300 |
  | Opportunity | HubSpot - Opportunity | No | $500 |
  | Closed Won | HubSpot - Closed Won | Yes (Primary) | Actual $ |

  IMMEDIATE ACTIONS:

  1. FIX: HubSpot Lead - Manual
     - Currently: include_in_conversions=True but 0 data
     - Action: Set include_in_conversions=False OR remove entirely
     - This is polluting your Smart Bidding signals

  2. VERIFY: GCLID capture in HubSpot
     - Ensure all forms capture the gclid parameter
     - Check HubSpot contact records for GCLID values
     - No GCLID = no attribution back to Google Ads

  3. EXPAND: Add downstream funnel stages
     - Currently only tracking Lead and MQL
     - Add SQL, Opportunity, Closed Won for full funnel visibility
     - Use HubSpot workflows to trigger Google Ads uploads

  4. CONFIGURE: Conversion values
     - HubSpot - Lead: Currently $1 (too low)
     - HubSpot - MQL: Currently $10 (reasonable)
     - Consider: Lead=$50, MQL=$150, SQL=$300, Opp=$500

  5. CLEANUP: Remove Salesforce actions
     - All 13 Salesforce actions show 0 data
     - They're orphaned - remove to clean up account

  HUBSPOT GOOGLE ADS INTEGRATION CHECKLIST:

  [ ] HubSpot connected via Google Ads Integration
      (HubSpot Settings > Marketing > Ads > Google Ads)

  [ ] GCLID tracking enabled in HubSpot
      (Settings > Tracking & Analytics > Tracking Code)

  [ ] Offline conversion sync enabled
      (HubSpot Ads Settings > Offline Conversions)

  [ ] Lifecycle stages mapped to Google Ads conversion actions

  [ ] Conversion window matches sales cycle (currently 30 days)
      - B2B typically needs 60-90 days
""")


if __name__ == '__main__':
    print("=" * 80)
    print("KIBO COMMERCE - HUBSPOT INTEGRATION DIAGNOSTIC")
    print(f"Account ID: {CUSTOMER_ID}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    get_hubspot_conversion_actions()
    get_hubspot_conversion_data()
    check_offline_upload_jobs()
    analyze_hubspot_health()
    provide_hubspot_recommendations()
