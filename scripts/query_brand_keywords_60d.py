"""
Query active Brand keywords from Kibo Commerce Google Ads account
with impressions > 0 in the last 60 days.

This identifies Brand keywords that are actively serving but may be missing Final URLs.
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
import csv
from datetime import datetime, timedelta

CUSTOMER_ID = '9948697111'

def query_brand_keywords_60d():
    """Query keywords with impressions > 0 in last 60 days from Brand campaigns"""
    ga_service = get_googleads_service('GoogleAdsService')

    # Calculate date range for last 60 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    query = f'''
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.criterion_id,
        ad_group_criterion.final_urls,
        ad_group.name,
        ad_group.id,
        campaign.name,
        campaign.id,
        metrics.impressions,
        metrics.clicks
    FROM keyword_view
    WHERE campaign.name LIKE '%Brand%'
    AND ad_group_criterion.status = 'ENABLED'
    AND segments.date BETWEEN '{start_str}' AND '{end_str}'
    AND metrics.impressions > 0
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    # Aggregate metrics since we're querying with date segment
    keyword_data = {}

    for row in response:
        keyword_text = row.ad_group_criterion.keyword.text
        criterion_id = row.ad_group_criterion.criterion_id

        # Use criterion_id as unique key
        key = criterion_id

        if key not in keyword_data:
            keyword_data[key] = {
                'keyword': keyword_text,
                'match_type': row.ad_group_criterion.keyword.match_type.name,
                'criterion_id': criterion_id,
                'final_urls': list(row.ad_group_criterion.final_urls) if row.ad_group_criterion.final_urls else [],
                'ad_group_name': row.ad_group.name,
                'ad_group_id': row.ad_group.id,
                'campaign_name': row.campaign.name,
                'campaign_id': row.campaign.id,
                'impressions': 0,
                'clicks': 0
            }

        # Aggregate metrics
        keyword_data[key]['impressions'] += row.metrics.impressions
        keyword_data[key]['clicks'] += row.metrics.clicks

    return list(keyword_data.values())

if __name__ == '__main__':
    print("=" * 70)
    print("Querying Active BRAND Keywords (Last 60 Days) - Kibo Commerce")
    print("=" * 70)

    print("\nQuerying Brand keywords with impressions > 0 in last 60 days...")
    keywords = query_brand_keywords_60d()

    print(f"\nFound {len(keywords)} active keywords in Brand campaigns")

    # Count keywords with and without URLs
    with_urls = [k for k in keywords if k['final_urls']]
    without_urls = [k for k in keywords if not k['final_urls']]

    print(f"  - With Final URLs: {len(with_urls)}")
    print(f"  - Without Final URLs: {len(without_urls)}")

    # Sort by impressions descending
    keywords.sort(key=lambda x: x['impressions'], reverse=True)

    print("\nTop 10 keywords by impressions:")
    for i, kw in enumerate(keywords[:10], 1):
        url_status = kw['final_urls'][0] if kw['final_urls'] else 'NO URL'
        print(f"  {i}. [{kw['keyword']}] ({kw['match_type']}) - {kw['impressions']:,} impr, {kw['clicks']} clicks")
        print(f"      Ad Group: {kw['ad_group_name']}")
        print(f"      URL: {url_status}")

    # Show keywords by ad group
    print("\n" + "-" * 70)
    print("Keywords by Ad Group:")
    print("-" * 70)

    ad_group_keywords = {}
    for kw in keywords:
        ag = kw['ad_group_name']
        if ag not in ad_group_keywords:
            ad_group_keywords[ag] = {'with_url': [], 'without_url': []}
        if kw['final_urls']:
            ad_group_keywords[ag]['with_url'].append(kw)
        else:
            ad_group_keywords[ag]['without_url'].append(kw)

    for ag, data in sorted(ad_group_keywords.items()):
        total = len(data['with_url']) + len(data['without_url'])
        missing = len(data['without_url'])
        print(f"\n  {ag} ({total} keywords, {missing} missing URLs):")

        # Show sample keywords
        all_kws = data['with_url'] + data['without_url']
        all_kws.sort(key=lambda x: x['impressions'], reverse=True)
        for kw in all_kws[:3]:
            url_indicator = '[OK]' if kw['final_urls'] else '[NO URL]'
            print(f"    {url_indicator} [{kw['keyword']}] ({kw['impressions']:,} impr)")
        if len(all_kws) > 3:
            print(f"    ... and {len(all_kws) - 3} more")

    # Save to CSV
    output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/brand_keywords_60d.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'keyword', 'match_type', 'criterion_id', 'final_urls',
            'ad_group_name', 'ad_group_id', 'campaign_name', 'campaign_id',
            'impressions', 'clicks'
        ])
        writer.writeheader()
        for kw in keywords:
            row = kw.copy()
            row['final_urls'] = ';'.join(kw['final_urls']) if kw['final_urls'] else ''
            writer.writerow(row)

    print(f"\n\nFull keyword list saved to: {output_file}")
