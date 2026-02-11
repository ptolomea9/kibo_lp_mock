"""
Check if gap keywords exist in the account (including paused)
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

from ads_mcp.utils import get_googleads_service
import csv

CUSTOMER_ID = '9948697111'

def get_all_keywords():
    """Get ALL keywords including paused ones"""
    ga_service = get_googleads_service('GoogleAdsService')

    query = '''
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.status,
        ad_group.name,
        campaign.name
    FROM keyword_view
    '''

    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

    keywords = {}
    for row in response:
        kw_text = row.ad_group_criterion.keyword.text.lower()
        status = row.ad_group_criterion.status.name
        if kw_text not in keywords:
            keywords[kw_text] = []
        keywords[kw_text].append({
            'status': status,
            'match_type': row.ad_group_criterion.keyword.match_type.name,
            'ad_group': row.ad_group.name,
            'campaign': row.campaign.name
        })
    return keywords

def load_gap_keywords(filepath):
    """Load gap keyword recommendations"""
    gaps = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw = row['Gap Keyword'].strip('[]').lower()
            gaps.append({
                'keyword': kw,
                'priority': row['Priority'],
                'product': row['Product Alignment'],
                'url': row['Recommended URL (with anchor)']
            })
    return gaps

if __name__ == '__main__':
    print("=" * 70)
    print("Gap Keyword Analysis - Checking Against Account")
    print("=" * 70)

    print("\nLoading all keywords from account (including paused)...")
    all_keywords = get_all_keywords()
    print(f"  Found {len(all_keywords)} unique keywords in account")

    print("\nLoading gap keyword recommendations...")
    gap_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/keyword_gap_opportunities.csv'
    gap_keywords = load_gap_keywords(gap_file)
    print(f"  Loaded {len(gap_keywords)} gap keyword recommendations")

    # Check each gap keyword against account
    exists_active = []
    exists_paused = []
    truly_new = []

    for gap in gap_keywords:
        kw = gap['keyword']
        if kw in all_keywords:
            instances = all_keywords[kw]
            statuses = [i['status'] for i in instances]
            if 'ENABLED' in statuses:
                exists_active.append({**gap, 'instances': instances})
            else:
                exists_paused.append({**gap, 'instances': instances})
        else:
            truly_new.append(gap)

    # Report results
    print("\n" + "=" * 70)
    print("ANALYSIS RESULTS")
    print("=" * 70)

    print(f"\n=== Summary ===")
    print(f"   Already Active: {len(exists_active)} keywords")
    print(f"   Paused (can reactivate): {len(exists_paused)} keywords")
    print(f"   Truly New: {len(truly_new)} keywords")

    if exists_active:
        print(f"\n[ALREADY ACTIVE] ({len(exists_active)}):")
        for kw in exists_active:
            instances = kw['instances']
            campaigns = set(i['campaign'] for i in instances if i['status'] == 'ENABLED')
            print(f"   [{kw['keyword']}] - Active in: {', '.join(list(campaigns)[:2])}")

    if exists_paused:
        print(f"\n[PAUSED - can be reactivated] ({len(exists_paused)}):")
        for kw in exists_paused:
            instances = kw['instances']
            campaigns = set(i['campaign'] for i in instances)
            statuses = set(i['status'] for i in instances)
            print(f"   [{kw['keyword']}] - Status: {', '.join(statuses)} in {', '.join(list(campaigns)[:2])}")

    if truly_new:
        print(f"\n[TRULY NEW KEYWORDS] ({len(truly_new)}):")
        by_priority = {'High': [], 'Medium': [], 'Low': []}
        for kw in truly_new:
            by_priority[kw['priority']].append(kw)

        print(f"\n   High Priority ({len(by_priority['High'])}):")
        for kw in by_priority['High'][:10]:
            print(f"     [{kw['keyword']}] - {kw['product']}")
        if len(by_priority['High']) > 10:
            print(f"     ... and {len(by_priority['High']) - 10} more")

        print(f"\n   Medium Priority ({len(by_priority['Medium'])}):")
        for kw in by_priority['Medium'][:5]:
            print(f"     [{kw['keyword']}] - {kw['product']}")
        if len(by_priority['Medium']) > 5:
            print(f"     ... and {len(by_priority['Medium']) - 5} more")
