# Kibo Commerce Non-Brand Google Ads Audit Instructions

<project_overview>
<name>Kibo Commerce Non-Brand Google Ads Health Audit</name>
<client>Kibo Commerce</client>
<website>www.kibocommerce.com</website>
<scope>
- Landing Page Optimization (keyword-level with anchored URLs)
- Keyword Gap Analysis
- Ad Copy Recommendations (with DKI requirements)
</scope>
<campaign_filter>Campaign Name contains "Search - NonBrand" only</campaign_filter>
</project_overview>

<objectives>
<objective id="1">
<name>Landing Page Optimization</name>
<description>Map each non-brand keyword to the most relevant, conversion-oriented landing page using anchored URLs where applicable for sub-fold content</description>
</objective>
<objective id="2">
<name>Keyword Gap Analysis</name>
<description>Identify high-value non-brand keywords Kibo should be bidding on with corresponding landing pages</description>
</objective>
<objective id="3">
<name>Ad Copy Optimization</name>
<description>Improve existing ad copy and create new variants for all keywords, incorporating dynamic keyword insertion (DKI) in at least one headline</description>
</objective>
</objectives>

---

## Part A: Site Crawl & Page Inventory

<site_crawl>
<phase id="A1">
<name>Deep Site Crawl</name>
<target>www.kibocommerce.com</target>
<depth>4-5 levels</depth>
<extraction_requirements>
<field>Full URL</field>
<field>Page title</field>
<field>Meta description</field>
<field>H1, H2s, H3s</field>
<field>Primary CTA text and destination</field>
<field>Key content sections with corresponding anchor IDs for deep linking</field>
<field>Product/solution focus</field>
<field>Target persona signals</field>
<field>URL path structure</field>
</extraction_requirements>
<priority_paths>
<path>/platform/ and all subpages</path>
<path>/solutions/ and all subpages</path>
<path>/industries/ or vertical-specific pages</path>
<path>/products/ or feature pages</path>
<path>Demo, contact, pricing pages</path>
</priority_paths>
</phase>

<phase id="A2">
<name>Anchor ID Mapping</name>
<description>For each high-intent page, document all defined anchor IDs for deep linking capability</description>
<extract_per_anchor>
<field>Anchor ID (#section-name)</field>
<field>Content topic of anchored section</field>
<field>Content type (feature details, use cases, benefits, CTAs)</field>
</extract_per_anchor>
<output_example>
| Page URL | Anchor ID | Section Topic | Content Type |
|----------|-----------|---------------|--------------|
| /platform/order-management/ | #distributed-oms | Distributed order management | Feature detail |
| /platform/order-management/ | #ship-from-store | Ship from store capabilities | Use case |
| /solutions/omnichannel/ | #bopis | Buy online pickup in store | Feature detail |
</output_example>
</phase>

<phase id="A3">
<name>Page Classification</name>
<intent_levels>
<level name="HIGH">Platform pages, product pages, demo, pricing, contact, solutions with strong CTAs</level>
<level name="MEDIUM">Case studies, comparisons, ROI tools, industry verticals</level>
<level name="LOW">Blog, resources, whitepapers, webinars, ebooks</level>
</intent_levels>
<master_inventory_columns>
<column>URL</column>
<column>Full URL with Anchors Available</column>
<column>Intent Level</column>
<column>Primary Topic</column>
<column>Secondary Topics</column>
<column>CTA Type</column>
<column>Personas</column>
</master_inventory_columns>
</phase>
</site_crawl>

---

## Part B: Current Non-Brand Keyword Audit

<keyword_audit>
<data_filter>
<include>Campaign Name contains "Search - NonBrand"</include>
<exclude>Brand campaigns, DSA, PMax, all other campaign types</exclude>
</data_filter>

<phase id="B1">
<name>Keyword-Level Landing Page Mapping</name>
<process>
<step order="1">
<name>Analyze keyword intent and topic</name>
<substeps>
<substep>Identify primary theme (OMS, headless, fulfillment, etc.)</substep>
<substep>Identify specific feature or use case referenced</substep>
<substep>Determine buyer stage (awareness, consideration, decision)</substep>
</substeps>
</step>

<step order="2">
<name>Identify optimal landing page</name>
<substeps>
<substep>Start with highest-intent page matching primary theme</substep>
<substep>If keyword references specific feature/capability, check if content exists on relevant page</substep>
<substep>If content is below fold, use anchored URL (e.g., /platform/oms/#ship-from-store)</substep>
<substep>Prioritize pages with CTAs aligned to keyword intent</substep>
</substeps>
</step>

<step order="3">
<name>Apply selection hierarchy</name>
<hierarchy>
<priority order="1">Exact topic match + high intent + anchor to specific section</priority>
<priority order="2">Exact topic match + high intent (no anchor needed)</priority>
<priority order="3">Parent solution page + anchor to relevant section</priority>
<priority order="4">Broader solution page (if no specific match)</priority>
<priority order="5">Flag as content gap if no suitable page exists</priority>
</hierarchy>
</step>

<step order="4">
<name>Document rationale for each recommendation</name>
</step>
</process>
</phase>

<phase id="B2">
<name>Output - Keyword-Level LP Audit</name>
<filename>keyword_landing_page_audit.csv</filename>
<columns>
<column>Keyword</column>
<column>Ad Group</column>
<column>Campaign</column>
<column>Match Type</column>
<column>Current URL</column>
<column>Current Intent Level</column>
<column>Recommended URL (with anchor if applicable)</column>
<column>Recommended Intent Level</column>
<column>Anchor Section Topic</column>
<column>Relevance Score (1-10)</column>
<column>CTA on Page</column>
<column>Rationale</column>
<column>Gap Flag</column>
<column>Priority</column>
</columns>
<sorting>
<sort order="1">Gap flags first</sort>
<sort order="2">Largest intent mismatch (low to high opportunity)</sort>
<sort order="3">By spend/volume if provided</sort>
</sorting>
</phase>
</keyword_audit>

---

## Part C: Keyword Gap Analysis

<gap_analysis>
<phase id="C1">
<name>Define Keyword Universe from Site Content</name>
<keyword_themes>
<theme name="Product/Platform Terms">
<examples>
<example>Order management, OMS, distributed order management</example>
<example>Ecommerce platform, unified commerce, composable commerce</example>
<example>Headless commerce, MACH architecture</example>
<example>Inventory management, real-time inventory</example>
</examples>
</theme>

<theme name="Feature-Specific Terms">
<examples>
<example>Ship from store, BOPIS, curbside pickup</example>
<example>Endless aisle, order routing, fulfillment optimization</example>
<example>Subscription management, recurring orders</example>
</examples>
</theme>

<theme name="Use Case/Outcome Terms">
<examples>
<example>Omnichannel fulfillment, inventory visibility</example>
<example>Reduce shipping costs, faster delivery</example>
<example>Single view of inventory</example>
</examples>
</theme>

<theme name="Industry/Vertical Terms">
<examples>
<example>B2B ecommerce, wholesale commerce</example>
<example>Retail order management, D2C fulfillment</example>
<example>Manufacturing ecommerce</example>
</examples>
</theme>
</keyword_themes>
<instruction>Generate long-tail variations and combinations from site content</instruction>
</phase>

<phase id="C2">
<name>Gap Identification</name>
<process>
<step>Compare generated keyword universe against current keyword list</step>
<step>Remove terms already covered (exact, phrase, close variants)</step>
<step>Prioritize remaining gaps by commercial intent strength, alignment with Kibo products, and landing page availability</step>
</process>
</phase>

<phase id="C3">
<name>Map Gap Keywords to Landing Pages</name>
<instructions>
<instruction>Apply same keyword-level LP mapping logic as Part B</instruction>
<instruction>Use anchored URLs where specific content exists below fold</instruction>
<instruction>Flag gaps requiring new page development</instruction>
</instructions>
<filename>keyword_gap_opportunities.csv</filename>
<columns>
<column>Gap Keyword</column>
<column>Intent Category</column>
<column>Product Alignment</column>
<column>Recommended URL (with anchor)</column>
<column>Page Exists (Y/N)</column>
<column>Anchor Section</column>
<column>Relevance Score</column>
<column>Suggested Match Type</column>
<column>Suggested Ad Group</column>
<column>Rationale</column>
<column>Priority</column>
</columns>
</phase>
</gap_analysis>

---

## Part D: Ad Copy Recommendations

<ad_copy>
<requirements>
<requirement type="mandatory">At least ONE headline must use Dynamic Keyword Insertion (DKI)</requirement>
<requirement type="format">DKI format: {KeyWord:Default Text}</requirement>
<requirement type="character_limits">
<limit element="Headlines">30 characters max</limit>
<limit element="Descriptions">90 characters max</limit>
</requirement>
<requirement type="structure">RSA format: 15 headlines, 4 descriptions per ad</requirement>
<requirement type="pinning">Pin DKI headline to position 1 or 2 for visibility</requirement>
</requirements>

<phase id="D1">
<name>Existing Ad Copy Audit</name>
<condition>If ad copy data is provided</condition>
<evaluation_criteria>
<criteria type="headlines">
<item>Does it include keyword/theme relevance?</item>
<item>Is there a clear value prop?</item>
<item>Is there a CTA headline?</item>
<item>Is DKI currently used?</item>
</criteria>
<criteria type="descriptions">
<item>Features vs. benefits balance</item>
<item>Specificity to keyword intent</item>
<item>CTA clarity</item>
</criteria>
<criteria type="improvement_opportunities">
<item>Missing DKI</item>
<item>Generic messaging that could be more specific</item>
<item>Weak CTAs</item>
<item>Missing proof points (stats, awards, customer count if available)</item>
</criteria>
</evaluation_criteria>
</phase>

<phase id="D2">
<name>Ad Copy Recommendations - Existing Keywords</name>
<rsa_structure>
<headlines count="15" max_chars="30">
<headline position="1" pin="position_1" type="DKI">
<format>{KeyWord:Default Text}</format>
<example>{KeyWord:Order Management}</example>
</headline>
<headline position="2-3" type="value_prop">Value prop headlines specific to keyword theme</headline>
<headline position="4-5" type="feature_benefit">Feature/benefit headlines</headline>
<headline position="6-7" type="CTA">CTA headlines (Get Demo, See Platform, Request Pricing)</headline>
<headline position="8-10" type="proof_trust">Proof/trust headlines if applicable</headline>
<headline position="11-15" type="variants">Variants and secondary angles</headline>
</headlines>

<descriptions count="4" max_chars="90">
<description position="1">Primary value prop + CTA aligned to keyword intent</description>
<description position="2">Feature-focused description</description>
<description position="3">Outcome/benefit-focused description</description>
<description position="4">Differentiator or trust signal</description>
</descriptions>
</rsa_structure>
<include_in_output>
<item>Recommended pin positions</item>
<item>Rationale for DKI default text choice</item>
</include_in_output>
</phase>

<phase id="D3">
<name>Ad Copy for Gap Keywords</name>
<instructions>
<instruction>Create full RSA following same structure as D2</instruction>
<instruction>Ensure DKI default text is relevant if keyword is truncated</instruction>
<instruction>Align messaging to recommended landing page content</instruction>
<instruction>Match CTA to page CTA for consistency</instruction>
</instructions>
</phase>

<phase id="D4">
<name>Output - Ad Copy</name>
<files>
<file>
<filename>ad_copy_recommendations.csv</filename>
<columns>
<column>Keyword</column>
<column>Ad Group</column>
<column>Type (Existing/Gap)</column>
<column>Headline 1 (DKI)</column>
<column>H1 Pin Position</column>
<column>Headline 2</column>
<column>Headline 3</column>
<column>Headline 4</column>
<column>Headline 5</column>
<column>Headline 6</column>
<column>Headline 7</column>
<column>Headline 8</column>
<column>Headline 9</column>
<column>Headline 10</column>
<column>Headline 11</column>
<column>Headline 12</column>
<column>Headline 13</column>
<column>Headline 14</column>
<column>Headline 15</column>
<column>Description 1</column>
<column>Description 2</column>
<column>Description 3</column>
<column>Description 4</column>
<column>D1 Pin Position</column>
<column>Rationale</column>
<column>Landing Page URL</column>
</columns>
</file>
<file>
<filename>ad_copy_by_theme.md</filename>
<description>Grouped ad copy templates by product/solution theme for easier review</description>
</file>
</files>
</phase>
</ad_copy>

---

## Part E: Deliverables & Summary

<deliverables>
<file>
<name>site_crawl_inventory.csv</name>
<description>All pages with anchors, intent levels, topics</description>
</file>
<file>
<name>keyword_landing_page_audit.csv</name>
<description>Current keyword LP analysis with anchored recommendations</description>
</file>
<file>
<name>keyword_gap_opportunities.csv</name>
<description>Net-new keywords with LP mapping</description>
</file>
<file>
<name>ad_copy_recommendations.csv</name>
<description>Full RSA recommendations for all keywords</description>
</file>
<file>
<name>ad_copy_by_theme.md</name>
<description>Organized ad copy grouped by solution area</description>
</file>
<file>
<name>content_gaps.md</name>
<description>Recommended new landing pages to build</description>
</file>
<file>
<name>executive_summary.md</name>
<description>Strategic overview with prioritized actions</description>
</file>
</deliverables>

<executive_summary_structure>
<section id="1">
<name>Current Non-Brand Health</name>
<items>
<item>Total keywords analyzed</item>
<item>% on low-intent pages (resources/blog)</item>
<item>% with suboptimal LP relevance (could use better anchor/page)</item>
<item>Top issues identified</item>
</items>
</section>

<section id="2">
<name>Landing Page Optimization Impact</name>
<items>
<item># keywords with new LP recommendations</item>
<item># using anchored URLs for improved relevance</item>
<item># content gaps requiring new pages</item>
<item>Priority actions</item>
</items>
</section>

<section id="3">
<name>Keyword Gap Opportunities</name>
<items>
<item>Total net-new keywords identified</item>
<item>Breakdown by theme/category</item>
<item># with existing LP coverage vs. needing new pages</item>
<item>Top 20 priority additions</item>
</items>
</section>

<section id="4">
<name>Ad Copy Improvements</name>
<items>
<item># ads currently missing DKI</item>
<item># ads with generic/weak messaging</item>
<item>Summary of copy themes and angles recommended</item>
</items>
</section>

<section id="5">
<name>Prioritized Action Plan</name>
<items>
<item>Immediate: LP URL updates (with anchors)</item>
<item>Week 1-2: Ad copy refreshes</item>
<item>Week 2-4: Gap keyword buildout</item>
<item>Ongoing: New page development roadmap</item>
</items>
</section>
</executive_summary_structure>

---

## Technical Parameters

<technical_requirements>
<crawl>
<requirement>Respect robots.txt</requirement>
<requirement>Use 1-2 second delays between requests</requirement>
<requirement>Capture all anchor IDs in page HTML</requirement>
<requirement>Handle JS-rendered content</requirement>
</crawl>

<ad_copy>
<requirement>Validate all character counts before output</requirement>
<requirement>Ensure DKI default text fits within 30 characters</requirement>
<requirement>Flag any headlines over 30 chars or descriptions over 90 chars</requirement>
</ad_copy>

<export>
<requirement>CSV format, Google Ads Editor compatible</requirement>
<requirement>UTF-8 encoding</requirement>
<requirement>Include all columns even if empty for consistency</requirement>
</export>
</technical_requirements>

---

## Input Required

<required_inputs>
<input type="mandatory">
<name>Non-Brand Keyword Export</name>
<description>Google Ads keyword report filtered to "Search - NonBrand" campaigns</description>
<preferred_columns>
<column>Keyword</column>
<column>Campaign</column>
<column>Ad Group</column>
<column>Match Type</column>
<column>Final URL</column>
<column>Impressions</column>
<column>Clicks</column>
<column>Cost</column>
<column>Conversions</column>
</preferred_columns>
</input>

<input type="optional">
<name>Existing Ad Copy Export</name>
<description>Current RSA ads for audit and improvement recommendations</description>
</input>
</required_inputs>
