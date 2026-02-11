"""
Kibo Commerce Conversion Actions Audit Script

Pulls all conversion actions with metadata and metrics for last 90 days.
Categorizes conversions as HEALTHY, BROKEN, LEGACY_UA, UNUSED, DUPLICATE, or MISCONFIGURED.
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
from datetime import datetime, timedelta
import csv
from collections import defaultdict

CUSTOMER_ID = '9948697111'
OUTPUT_DIR = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data'


def get_conversion_actions():
    """Pull all conversion actions with full metadata"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        conversion_action.id,
        conversion_action.name,
        conversion_action.type,
        conversion_action.status,
        conversion_action.category,
        conversion_action.counting_type,
        conversion_action.include_in_conversions_metric,
        conversion_action.view_through_lookback_window_days,
        conversion_action.click_through_lookback_window_days,
        conversion_action.attribution_model_settings.attribution_model,
        conversion_action.value_settings.default_value,
        conversion_action.primary_for_goal
    FROM conversion_action
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    conversions = []
    for row in response:
        ca = row.conversion_action
        conversions.append({
            'id': ca.id,
            'name': ca.name,
            'type': ca.type.name if ca.type else 'UNKNOWN',
            'status': ca.status.name if ca.status else 'UNKNOWN',
            'category': ca.category.name if ca.category else 'UNKNOWN',
            'counting_type': ca.counting_type.name if ca.counting_type else 'UNKNOWN',
            'include_in_conversions': ca.include_in_conversions_metric,
            'view_through_lookback': ca.view_through_lookback_window_days,
            'click_through_lookback': ca.click_through_lookback_window_days,
            'attribution_model': ca.attribution_model_settings.attribution_model.name if ca.attribution_model_settings else 'UNKNOWN',
            'default_value': ca.value_settings.default_value if ca.value_settings else 0,
            'primary_for_goal': ca.primary_for_goal
        })

    return conversions


def get_conversion_metrics():
    """Pull conversion metrics for last 90 days by conversion action"""
    ga_service = get_googleads_service('GoogleAdsService')

    # Calculate date range (last 90 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    date_range = f"segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'"

    query = f'''
    SELECT
        segments.conversion_action_name,
        segments.conversion_action,
        metrics.conversions,
        metrics.conversions_value,
        metrics.all_conversions,
        metrics.all_conversions_value
    FROM customer
    WHERE {date_range}
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    # Aggregate by conversion action name
    metrics_by_name = defaultdict(lambda: {
        'conversions': 0,
        'conversions_value': 0,
        'all_conversions': 0,
        'all_conversions_value': 0
    })

    for row in response:
        conv_name = row.segments.conversion_action_name
        metrics_by_name[conv_name]['conversions'] += row.metrics.conversions
        metrics_by_name[conv_name]['conversions_value'] += row.metrics.conversions_value
        metrics_by_name[conv_name]['all_conversions'] += row.metrics.all_conversions
        metrics_by_name[conv_name]['all_conversions_value'] += row.metrics.all_conversions_value

    return dict(metrics_by_name)


def categorize_conversion(conv, metrics):
    """Categorize a conversion action based on its state and metrics"""
    name = conv['name']
    status = conv['status']
    conv_type = conv['type']
    include = conv['include_in_conversions']

    conv_count = metrics.get('conversions', 0)
    all_conv_count = metrics.get('all_conversions', 0)

    # Priority order for categorization

    # 1. Legacy UA goals (highest priority - should be removed)
    if conv_type == 'UNIVERSAL_ANALYTICS_GOAL':
        return 'LEGACY_UA', 'Universal Analytics goal - UA sunset July 2023, remove'

    # 2. Already removed/hidden - just needs cleanup
    if status in ['REMOVED', 'HIDDEN']:
        return 'UNUSED', f'Status is {status} - can be fully deleted if no longer needed'

    # 3. Enabled but zero conversions - potentially broken
    if status == 'ENABLED' and all_conv_count == 0:
        if include:
            return 'BROKEN_PRIMARY', 'CRITICAL: Enabled + included in conversions but 0 conversions in 90 days'
        else:
            return 'BROKEN_SECONDARY', 'Enabled but 0 conversions in 90 days - investigate or remove'

    # 4. Include in conversions mismatch
    if include and conv_count == 0 and all_conv_count > 0:
        return 'MISCONFIGURED', 'Included in conversions but only has "all_conversions" - check attribution'

    # 5. Healthy - enabled with conversions
    if status == 'ENABLED' and all_conv_count > 0:
        return 'HEALTHY', 'Active and tracking conversions'

    return 'REVIEW', 'Needs manual review'


def find_duplicates(conversions):
    """Find potential duplicate conversion actions by name pattern"""
    # Normalize names for comparison
    name_groups = defaultdict(list)

    for conv in conversions:
        # Create normalized key: lowercase, remove special chars, etc.
        name = conv['name'].lower()
        # Remove common suffixes that indicate duplicates
        for suffix in [' (1)', ' (2)', ' copy', '_old', '_new', 'v1', 'v2']:
            name = name.replace(suffix, '')
        name = name.strip()
        name_groups[name].append(conv['name'])

    duplicates = {}
    for base_name, names in name_groups.items():
        if len(names) > 1:
            for name in names:
                duplicates[name] = f"Potential duplicate group: {names}"

    return duplicates


def run_audit():
    """Run the full conversion audit"""
    print("=" * 80)
    print("Kibo Commerce Conversion Actions Audit")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    # Step 1: Get all conversion actions
    print("\n[1/4] Fetching conversion actions metadata...")
    conversions = get_conversion_actions()
    print(f"      Found {len(conversions)} conversion actions")

    # Step 2: Get metrics for last 90 days
    print("\n[2/4] Fetching conversion metrics (last 90 days)...")
    metrics = get_conversion_metrics()
    print(f"      Found metrics for {len(metrics)} conversion actions")

    # Step 3: Find potential duplicates
    print("\n[3/4] Analyzing for duplicates...")
    duplicates = find_duplicates(conversions)
    print(f"      Found {len(duplicates)} potential duplicates")

    # Step 4: Categorize and enrich data
    print("\n[4/4] Categorizing conversion actions...")

    audit_results = []
    category_counts = defaultdict(int)

    for conv in conversions:
        name = conv['name']
        conv_metrics = metrics.get(name, {
            'conversions': 0,
            'conversions_value': 0,
            'all_conversions': 0,
            'all_conversions_value': 0
        })

        category, reason = categorize_conversion(conv, conv_metrics)

        # Check for duplicate flag
        if name in duplicates:
            if category == 'HEALTHY':
                category = 'DUPLICATE'
                reason = duplicates[name]

        category_counts[category] += 1

        audit_results.append({
            'id': conv['id'],
            'name': name,
            'type': conv['type'],
            'status': conv['status'],
            'category_audit': category,
            'reason': reason,
            'include_in_conversions': conv['include_in_conversions'],
            'primary_for_goal': conv['primary_for_goal'],
            'conv_category': conv['category'],
            'counting_type': conv['counting_type'],
            'attribution_model': conv['attribution_model'],
            'click_lookback': conv['click_through_lookback'],
            'view_lookback': conv['view_through_lookback'],
            'default_value': conv['default_value'],
            'conversions_90d': conv_metrics['conversions'],
            'conversions_value_90d': conv_metrics['conversions_value'],
            'all_conversions_90d': conv_metrics['all_conversions'],
            'all_conversions_value_90d': conv_metrics['all_conversions_value']
        })

    # Print summary
    print("\n" + "=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)

    priority_order = ['BROKEN_PRIMARY', 'BROKEN_SECONDARY', 'LEGACY_UA', 'MISCONFIGURED',
                      'DUPLICATE', 'UNUSED', 'REVIEW', 'HEALTHY']

    for cat in priority_order:
        if cat in category_counts:
            emoji = {'HEALTHY': '[OK]', 'LEGACY_UA': '[!!]', 'BROKEN_PRIMARY': '[!!]',
                    'BROKEN_SECONDARY': '[!]', 'UNUSED': '[-]', 'DUPLICATE': '[?]',
                    'MISCONFIGURED': '[!]', 'REVIEW': '[?]'}.get(cat, '   ')
            print(f"  {emoji} {cat}: {category_counts[cat]}")

    print(f"\n  Total: {len(audit_results)}")

    # Save to CSV
    output_file = f"{OUTPUT_DIR}/conversion_audit_report.csv"
    fieldnames = ['id', 'name', 'type', 'status', 'category_audit', 'reason',
                  'include_in_conversions', 'primary_for_goal', 'conv_category',
                  'counting_type', 'attribution_model', 'click_lookback', 'view_lookback',
                  'default_value', 'conversions_90d', 'conversions_value_90d',
                  'all_conversions_90d', 'all_conversions_value_90d']

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # Sort by category priority then by name
        sorted_results = sorted(audit_results,
                               key=lambda x: (priority_order.index(x['category_audit'])
                                            if x['category_audit'] in priority_order else 99,
                                            x['name']))
        writer.writerows(sorted_results)

    print(f"\n[OK] Full audit saved to: {output_file}")

    # Print critical issues
    critical = [r for r in audit_results if r['category_audit'] in ['BROKEN_PRIMARY', 'LEGACY_UA']]
    if critical:
        print("\n" + "=" * 80)
        print("CRITICAL ISSUES (Immediate Action Required)")
        print("=" * 80)
        for r in critical[:15]:  # Show top 15
            print(f"\n  [{r['category_audit']}] {r['name']}")
            print(f"    Type: {r['type']} | Status: {r['status']}")
            print(f"    Include in Conversions: {r['include_in_conversions']}")
            print(f"    90-Day Conversions: {r['conversions_90d']:.1f}")
            print(f"    Reason: {r['reason']}")

    return audit_results, category_counts


if __name__ == '__main__':
    audit_results, category_counts = run_audit()

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
    1. Review conversion_audit_report.csv for full details
    2. Address BROKEN_PRIMARY conversions first (included in bidding but not firing)
    3. Remove LEGACY_UA conversions (Universal Analytics sunset)
    4. Investigate BROKEN_SECONDARY conversions (may be seasonal or misconfigured)
    5. Clean up UNUSED conversions (REMOVED/HIDDEN status)
    6. Consolidate DUPLICATE conversions
    """)
