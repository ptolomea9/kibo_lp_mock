"""
Query existing keywords from Kibo Commerce Google Ads account
to map them to keyword IDs for updates
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
import csv

CUSTOMER_ID = '9948697111'

def query_nonbrand_keywords():
    """Query all keywords from Search - NonBrand campaigns"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.criterion_id,
        ad_group_criterion.final_urls,
        ad_group.name,
        ad_group.id,
        campaign.name,
        campaign.id
    FROM keyword_view
    WHERE campaign.name LIKE '%NonBrand%'
    AND ad_group_criterion.status = 'ENABLED'
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    keywords = []
    for row in response:
        keyword_text = row.ad_group_criterion.keyword.text
        match_type = row.ad_group_criterion.keyword.match_type.name
        criterion_id = row.ad_group_criterion.criterion_id
        final_urls = list(row.ad_group_criterion.final_urls) if row.ad_group_criterion.final_urls else []
        ad_group_name = row.ad_group.name
        ad_group_id = row.ad_group.id
        campaign_name = row.campaign.name
        campaign_id = row.campaign.id

        keywords.append({
            'keyword': keyword_text,
            'match_type': match_type,
            'criterion_id': criterion_id,
            'final_urls': final_urls,
            'ad_group_name': ad_group_name,
            'ad_group_id': ad_group_id,
            'campaign_name': campaign_name,
            'campaign_id': campaign_id
        })

    return keywords

if __name__ == '__main__':
    print("Querying NonBrand keywords from Kibo Commerce account...")
    keywords = query_nonbrand_keywords()

    print(f"\nFound {len(keywords)} keywords in NonBrand campaigns\n")
    print("Sample keywords:")
    for kw in keywords[:10]:
        urls = kw['final_urls'][0] if kw['final_urls'] else 'None'
        print(f"  [{kw['keyword']}] ({kw['match_type']}) - {kw['ad_group_name']}")
        print(f"    Criterion ID: {kw['criterion_id']}, Current URL: {urls}")

    # Save to CSV for reference
    output_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/current_keywords_with_ids.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['keyword', 'match_type', 'criterion_id', 'final_urls',
                                                'ad_group_name', 'ad_group_id', 'campaign_name', 'campaign_id'])
        writer.writeheader()
        writer.writerows(keywords)

    print(f"\n\nFull keyword list saved to: {output_file}")
