"""
Query Google Ads change history for keyword URL changes
to determine when keyword-level Final URLs were modified
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from google.ads.googleads.client import GoogleAdsClient
import csv

CUSTOMER_ID = '9948697111'
YAML_PATH = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

def query_keyword_url_changes():
    """Query change history for keyword Final URL changes"""
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    ga_service = client.get_service("GoogleAdsService")

    # Query change events for ad_group_criterion changes (keyword-level URL changes)
    query = '''
    SELECT
        change_event.change_date_time,
        change_event.change_resource_type,
        change_event.change_resource_name,
        change_event.changed_fields,
        change_event.old_resource,
        change_event.new_resource,
        change_event.resource_change_operation,
        change_event.user_email,
        campaign.name,
        ad_group.name
    FROM change_event
    WHERE change_event.change_resource_type = 'AD_GROUP_CRITERION'
        AND campaign.name = 'Search - NonBrand'
        AND change_event.change_date_time DURING LAST_30_DAYS
    ORDER BY change_event.change_date_time DESC
    LIMIT 1000
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

        changes = []
        for row in response:
            event = row.change_event
            change_info = {
                'date_time': event.change_date_time,
                'resource_type': event.change_resource_type.name,
                'resource_name': event.change_resource_name,
                'changed_fields': str(event.changed_fields),
                'operation': event.resource_change_operation.name,
                'user_email': event.user_email,
                'campaign': row.campaign.name,
                'ad_group': row.ad_group.name,
            }

            # Try to get old/new Final URLs from the resource
            if event.old_resource and hasattr(event.old_resource, 'ad_group_criterion'):
                old_criterion = event.old_resource.ad_group_criterion
                if old_criterion.final_urls:
                    change_info['old_urls'] = list(old_criterion.final_urls)

            if event.new_resource and hasattr(event.new_resource, 'ad_group_criterion'):
                new_criterion = event.new_resource.ad_group_criterion
                if new_criterion.final_urls:
                    change_info['new_urls'] = list(new_criterion.final_urls)
                if new_criterion.keyword and new_criterion.keyword.text:
                    change_info['keyword_text'] = new_criterion.keyword.text

            changes.append(change_info)

        return changes

    except Exception as e:
        print(f"Error querying change events: {e}")
        print(f"Error type: {type(e).__name__}")

        # Fallback: try change_status approach
        print("\nTrying alternative approach with change_status...")
        return query_keyword_changes_alternative(client, ga_service)


def query_keyword_changes_alternative(client, ga_service):
    """Alternative: query keywords and look for recently modified ones"""

    # Query keywords with their status and URLs to see which have keyword-level URLs set
    query = '''
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.criterion_id,
        ad_group_criterion.final_urls,
        ad_group_criterion.status,
        ad_group.name,
        campaign.name
    FROM ad_group_criterion
    WHERE campaign.name = 'Search - NonBrand'
        AND ad_group_criterion.type = 'KEYWORD'
        AND ad_group_criterion.status != 'REMOVED'
    ORDER BY ad_group.name
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    keywords_with_urls = []
    keywords_without_urls = []

    for row in response:
        criterion = row.ad_group_criterion
        kw_info = {
            'keyword': criterion.keyword.text,
            'match_type': criterion.keyword.match_type.name,
            'criterion_id': criterion.criterion_id,
            'final_urls': list(criterion.final_urls) if criterion.final_urls else [],
            'status': criterion.status.name,
            'ad_group': row.ad_group.name,
            'campaign': row.campaign.name,
        }

        if kw_info['final_urls']:
            keywords_with_urls.append(kw_info)
        else:
            keywords_without_urls.append(kw_info)

    return {
        'with_urls': keywords_with_urls,
        'without_urls': keywords_without_urls
    }


def query_campaign_status_changes():
    """Query when the campaign was unpaused"""
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    ga_service = client.get_service("GoogleAdsService")

    query = '''
    SELECT
        change_event.change_date_time,
        change_event.change_resource_type,
        change_event.changed_fields,
        change_event.resource_change_operation,
        change_event.user_email,
        campaign.name,
        campaign.status
    FROM change_event
    WHERE change_event.change_resource_type = 'CAMPAIGN'
        AND campaign.name = 'Search - NonBrand'
        AND change_event.change_date_time DURING LAST_30_DAYS
    ORDER BY change_event.change_date_time DESC
    LIMIT 100
    '''

    try:
        response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

        changes = []
        for row in response:
            event = row.change_event
            changes.append({
                'date_time': event.change_date_time,
                'changed_fields': str(event.changed_fields),
                'operation': event.resource_change_operation.name,
                'user_email': event.user_email,
                'campaign': row.campaign.name,
                'campaign_status': row.campaign.status.name,
            })
        return changes
    except Exception as e:
        print(f"Error querying campaign changes: {e}")
        return []


if __name__ == '__main__':
    print("=" * 70)
    print("KIBO COMMERCE - KEYWORD URL CHANGE HISTORY")
    print("=" * 70)

    # 1. Query campaign status changes (when was it unpaused?)
    print("\n--- Campaign Status Changes (Last 30 Days) ---")
    campaign_changes = query_campaign_status_changes()
    if campaign_changes:
        for c in campaign_changes:
            print(f"  {c['date_time']} | {c['operation']} | Fields: {c['changed_fields']} | By: {c['user_email']}")
    else:
        print("  No campaign-level changes found in last 30 days")

    # 2. Query keyword URL changes
    print("\n--- Keyword URL Changes (Last 30 Days) ---")
    result = query_keyword_url_changes()

    if isinstance(result, dict):
        # Alternative approach returned
        print(f"\n  Keywords WITH keyword-level Final URLs: {len(result['with_urls'])}")
        print(f"  Keywords WITHOUT keyword-level Final URLs: {len(result['without_urls'])}")

        print("\n  --- Keywords with URLs (likely recently updated) ---")
        for kw in sorted(result['with_urls'], key=lambda x: x['ad_group']):
            print(f"    [{kw['keyword']}] ({kw['match_type']}) | {kw['ad_group']} | URL: {kw['final_urls'][0] if kw['final_urls'] else 'None'}")

        # Save to CSV
        output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/keyword_url_change_audit.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['keyword', 'match_type', 'criterion_id', 'final_urls', 'status', 'ad_group', 'campaign'])
            writer.writeheader()
            for kw in result['with_urls']:
                kw_copy = kw.copy()
                kw_copy['final_urls'] = '; '.join(kw['final_urls'])
                writer.writerow(kw_copy)
        print(f"\n  Saved to: {output_file}")

    elif isinstance(result, list):
        # Change events returned
        url_changes = [c for c in result if 'final_urls' in str(c.get('changed_fields', ''))]
        print(f"\n  Total keyword changes: {len(result)}")
        print(f"  URL-specific changes: {len(url_changes)}")

        for c in result[:30]:
            keyword = c.get('keyword_text', 'Unknown')
            old_urls = c.get('old_urls', [])
            new_urls = c.get('new_urls', [])
            print(f"  {c['date_time']} | {c['operation']} | {c['ad_group']} | KW: {keyword}")
            if old_urls:
                print(f"    Old URLs: {old_urls}")
            if new_urls:
                print(f"    New URLs: {new_urls}")
            print(f"    Changed: {c['changed_fields']}")
            print(f"    By: {c['user_email']}")
            print()
