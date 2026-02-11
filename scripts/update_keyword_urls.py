"""
Update keyword Final URLs based on the landing page audit recommendations

This script:
1. Reads the audit recommendations
2. Matches keywords to their Google Ads criterion IDs
3. Updates Final URLs in bulk using the Google Ads API
"""

import sys
sys.path.insert(0, 'C:/Users/shawh/google-ads-mcp')
import os
os.environ['GOOGLE_ADS_YAML_PATH'] = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

import csv
from google.ads.googleads.client import GoogleAdsClient

CUSTOMER_ID = '9948697111'
YAML_PATH = 'C:/Users/shawh/google-ads-mcp/google-ads.yaml'

def load_audit_recommendations(filepath):
    """Load keyword landing page recommendations from CSV"""
    recommendations = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean keyword text - remove brackets if present
            keyword = row['Keyword'].strip('[]')
            recommendations.append({
                'keyword': keyword,
                'ad_group': row['Ad Group'],
                'match_type': row['Match Type'].upper(),
                'recommended_url': row['Recommended URL (with anchor if applicable)'],
                'priority': row['Priority']
            })
    return recommendations

def load_current_keywords(filepath):
    """Load current keywords with IDs from CSV"""
    keywords = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create key: keyword_text + match_type + ad_group
            key = (row['keyword'].lower(), row['match_type'], row['ad_group_name'])
            keywords[key] = {
                'criterion_id': row['criterion_id'],
                'ad_group_id': row['ad_group_id'],
                'current_urls': row['final_urls']
            }
    return keywords

def match_recommendations_to_ids(recommendations, current_keywords):
    """Match audit recommendations to keyword criterion IDs"""
    matched = []
    unmatched = []

    for rec in recommendations:
        # Try to find matching keyword
        key = (rec['keyword'].lower(), rec['match_type'], rec['ad_group'])

        if key in current_keywords:
            matched.append({
                **rec,
                'criterion_id': current_keywords[key]['criterion_id'],
                'ad_group_id': current_keywords[key]['ad_group_id'],
                'current_urls': current_keywords[key]['current_urls']
            })
        else:
            # Try fuzzy match - just keyword and match type
            found = False
            for (kw, mt, ag), data in current_keywords.items():
                if kw == rec['keyword'].lower() and mt == rec['match_type']:
                    matched.append({
                        **rec,
                        'criterion_id': data['criterion_id'],
                        'ad_group_id': data['ad_group_id'],
                        'current_urls': data['current_urls'],
                        'note': f'Matched to ad group: {ag}'
                    })
                    found = True
                    break
            if not found:
                unmatched.append(rec)

    return matched, unmatched

def update_keyword_urls(matched_keywords, dry_run=True):
    """Update Final URLs for matched keywords using Google Ads API"""
    from google.protobuf import field_mask_pb2

    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    operations = []

    for kw in matched_keywords:
        # Create the operation
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.update

        # Set the resource name
        criterion.resource_name = client.get_service("AdGroupCriterionService").ad_group_criterion_path(
            CUSTOMER_ID, kw['ad_group_id'], kw['criterion_id']
        )

        # Clear existing and add new final URL
        criterion.final_urls.append(kw['recommended_url'])

        # Create field mask for the update
        operation.update_mask.CopyFrom(
            field_mask_pb2.FieldMask(paths=["final_urls"])
        )

        operations.append(operation)

    if dry_run:
        print(f"\n[DRY RUN] Would update {len(operations)} keywords:")
        for i, kw in enumerate(matched_keywords[:10]):
            print(f"  {i+1}. [{kw['keyword']}] -> {kw['recommended_url']}")
        if len(matched_keywords) > 10:
            print(f"  ... and {len(matched_keywords) - 10} more")
        return None
    else:
        # Execute the updates
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=CUSTOMER_ID,
            operations=operations
        )
        return response

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true', help='Execute updates (default is dry run)')
    parser.add_argument('--input', type=str, help='Path to input CSV with URL mappings (default: keyword_landing_page_audit.csv)')
    args = parser.parse_args()

    print("=" * 60)
    print("Keyword URL Update Script")
    print("=" * 60)

    # Load data
    default_audit = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/keyword_landing_page_audit.csv'
    audit_file = args.input if args.input else default_audit
    current_file = 'C:/Users/shawh/OneDrive/Desktop/Kibo Commerce/data/current_keywords_with_ids.csv'

    print(f"\nLoading audit recommendations from: {audit_file}")
    recommendations = load_audit_recommendations(audit_file)
    print(f"  Loaded {len(recommendations)} recommendations")

    print("\nLoading current keywords...")
    current_keywords = load_current_keywords(current_file)
    print(f"  Loaded {len(current_keywords)} current keywords")

    print("\nMatching recommendations to keyword IDs...")
    matched, unmatched = match_recommendations_to_ids(recommendations, current_keywords)
    print(f"  Matched: {len(matched)} keywords")
    print(f"  Unmatched: {len(unmatched)} keywords")

    if unmatched:
        print("\n  Unmatched keywords (may need manual review):")
        for kw in unmatched[:5]:
            print(f"    - [{kw['keyword']}] ({kw['match_type']}) in {kw['ad_group']}")
        if len(unmatched) > 5:
            print(f"    ... and {len(unmatched) - 5} more")

    # Show matched keywords by priority
    high_priority = [k for k in matched if k['priority'] == 'High']
    medium_priority = [k for k in matched if k['priority'] == 'Medium']
    low_priority = [k for k in matched if k['priority'] == 'Low']

    print(f"\n  By Priority:")
    print(f"    High: {len(high_priority)}")
    print(f"    Medium: {len(medium_priority)}")
    print(f"    Low: {len(low_priority)}")

    # Update URLs
    if args.execute:
        print("\n" + "=" * 60)
        print("EXECUTING URL UPDATES")
        print("=" * 60)
        response = update_keyword_urls(matched, dry_run=False)
        if response:
            print(f"\nSuccessfully updated {len(response.results)} keywords!")
            for result in response.results[:5]:
                print(f"  Updated: {result.resource_name}")
            if len(response.results) > 5:
                print(f"  ... and {len(response.results) - 5} more")
    else:
        print("\n" + "=" * 60)
        print("DRY RUN MODE (use --execute to apply changes)")
        print("=" * 60)
        update_keyword_urls(matched, dry_run=True)

        print("\nSample updates by URL target:")
        url_groups = {}
        for kw in matched:
            url = kw['recommended_url']
            if url not in url_groups:
                url_groups[url] = []
            url_groups[url].append(kw['keyword'])

        for url, keywords in sorted(url_groups.items(), key=lambda x: -len(x[1]))[:5]:
            print(f"\n  {url}")
            print(f"    Keywords ({len(keywords)}): {', '.join(keywords[:3])}" +
                  (f"... +{len(keywords)-3} more" if len(keywords) > 3 else ""))
