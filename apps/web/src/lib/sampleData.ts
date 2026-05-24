import type { Article, Category, Tag, CompanyTicker, Author, Source, MediaAsset } from './types';

// ──────────────────────────────────────────────
// Authors
// ──────────────────────────────────────────────

const authorDesk: Author = {
  id: 'author-001',
  name: 'CapitalColumn Editorial Desk',
  slug: 'editorial-desk',
  bio: 'The CapitalColumn Editorial Desk curates and publishes AI-assisted financial coverage with human editorial oversight.',
  avatar_url: null,
  author_type: 'editorial_team',
};

const authorAI: Author = {
  id: 'author-002',
  name: 'CapitalColumn AI',
  slug: 'ai',
  bio: 'AI-generated financial analysis reviewed by our editorial team for accuracy and completeness.',
  avatar_url: null,
  author_type: 'ai_assisted',
};

const authorPriya: Author = {
  id: 'author-003',
  name: 'Priya Sharma',
  slug: 'priya-sharma',
  bio: 'Senior markets correspondent covering Indian equities, IPOs, and institutional flows.',
  avatar_url: 'https://media.capitalcolumn.in/avatars/priya-sharma.jpg',
  author_type: 'human',
};

const authorRahul: Author = {
  id: 'author-004',
  name: 'Rahul Menon',
  slug: 'rahul-menon',
  bio: 'Technology and semiconductors analyst with 12 years of experience covering global chip supply chains.',
  avatar_url: 'https://media.capitalcolumn.in/avatars/rahul-menon.jpg',
  author_type: 'human',
};

// ──────────────────────────────────────────────
// Categories
// ──────────────────────────────────────────────

export const sampleCategories: Category[] = [
  { id: 'cat-01', name: 'Markets', slug: 'markets', description: 'Stock market news, indices, and trading updates', parent_id: null, sort_order: 1, is_active: true },
  { id: 'cat-02', name: 'Earnings', slug: 'earnings', description: 'Quarterly and annual earnings reports and analysis', parent_id: null, sort_order: 2, is_active: true },
  { id: 'cat-03', name: 'Companies', slug: 'companies', description: 'Company-specific news, management changes, and corporate actions', parent_id: null, sort_order: 3, is_active: true },
  { id: 'cat-04', name: 'Technology', slug: 'technology', description: 'Technology sector coverage including AI, semiconductors, and software', parent_id: null, sort_order: 4, is_active: true },
  { id: 'cat-05', name: 'Banking & Finance', slug: 'banking-finance', description: 'Banking, NBFC, insurance, and fintech sector coverage', parent_id: null, sort_order: 5, is_active: true },
  { id: 'cat-06', name: 'Energy', slug: 'energy', description: 'Oil, gas, renewables, and energy transition coverage', parent_id: null, sort_order: 6, is_active: true },
  { id: 'cat-07', name: 'IPOs', slug: 'ipos', description: 'IPO filings, grey market premiums, listing analysis, and new issues', parent_id: null, sort_order: 7, is_active: true },
  { id: 'cat-08', name: 'Policy & Regulation', slug: 'policy-regulation', description: 'Government policy, RBI decisions, SEBI regulations, and tax updates', parent_id: null, sort_order: 8, is_active: true },
  { id: 'cat-09', name: 'Healthcare', slug: 'healthcare', description: 'Pharma, biotech, hospitals, and healthcare services', parent_id: null, sort_order: 9, is_active: true },
  { id: 'cat-10', name: 'Global Markets', slug: 'global-markets', description: 'International market coverage including US, EU, and Asian markets', parent_id: null, sort_order: 10, is_active: true },
  { id: 'cat-11', name: 'Consumer', slug: 'consumer', description: 'FMCG, retail, e-commerce, and consumer discretionary coverage', parent_id: null, sort_order: 11, is_active: true },
  { id: 'cat-12', name: 'Industrials', slug: 'industrials', description: 'Manufacturing, infrastructure, capital goods, and defence', parent_id: null, sort_order: 12, is_active: true },
];

// ──────────────────────────────────────────────
// Tags
// ──────────────────────────────────────────────

export const sampleTags: Tag[] = [
  { id: 'tag-01', name: 'AI', slug: 'ai' },
  { id: 'tag-02', name: 'EV', slug: 'ev' },
  { id: 'tag-03', name: 'Semiconductors', slug: 'semiconductors' },
  { id: 'tag-04', name: 'Interest Rates', slug: 'interest-rates' },
  { id: 'tag-05', name: 'Inflation', slug: 'inflation' },
  { id: 'tag-06', name: 'M&A', slug: 'mergers-acquisitions' },
  { id: 'tag-07', name: 'Quarterly Results', slug: 'quarterly-results' },
  { id: 'tag-08', name: 'Valuation', slug: 'valuation' },
  { id: 'tag-09', name: 'Debt', slug: 'debt' },
  { id: 'tag-10', name: 'Management Change', slug: 'management-change' },
];

// ──────────────────────────────────────────────
// Companies / Tickers
// ──────────────────────────────────────────────

export const sampleCompanies: CompanyTicker[] = [
  { id: 'co-01', name: 'Apple Inc.', ticker: 'AAPL', exchange: 'NASDAQ', country: 'US', sector: 'Technology', industry: 'Consumer Electronics', logo_url: null, company_page_slug: 'apple-aapl' },
  { id: 'co-02', name: 'Microsoft Corporation', ticker: 'MSFT', exchange: 'NASDAQ', country: 'US', sector: 'Technology', industry: 'Software', logo_url: null, company_page_slug: 'microsoft-msft' },
  { id: 'co-03', name: 'NVIDIA Corporation', ticker: 'NVDA', exchange: 'NASDAQ', country: 'US', sector: 'Technology', industry: 'Semiconductors', logo_url: null, company_page_slug: 'nvidia-nvda' },
  { id: 'co-04', name: 'Tesla Inc.', ticker: 'TSLA', exchange: 'NASDAQ', country: 'US', sector: 'Consumer Discretionary', industry: 'Electric Vehicles', logo_url: null, company_page_slug: 'tesla-tsla' },
  { id: 'co-05', name: 'JPMorgan Chase & Co.', ticker: 'JPM', exchange: 'NYSE', country: 'US', sector: 'Financials', industry: 'Banking', logo_url: null, company_page_slug: 'jpmorgan-jpm' },
  { id: 'co-06', name: 'HDFC Bank Ltd.', ticker: 'HDFCBANK', exchange: 'NSE', country: 'IN', sector: 'Financials', industry: 'Banking', logo_url: null, company_page_slug: 'hdfc-bank-hdfcbank' },
  { id: 'co-07', name: 'Tata Consultancy Services', ticker: 'TCS', exchange: 'NSE', country: 'IN', sector: 'Technology', industry: 'IT Services', logo_url: null, company_page_slug: 'tcs-tcs' },
  { id: 'co-08', name: 'Infosys Ltd.', ticker: 'INFY', exchange: 'NSE', country: 'IN', sector: 'Technology', industry: 'IT Services', logo_url: null, company_page_slug: 'infosys-infy' },
  { id: 'co-09', name: 'Reliance Industries Ltd.', ticker: 'RELIANCE', exchange: 'NSE', country: 'IN', sector: 'Energy', industry: 'Conglomerate', logo_url: null, company_page_slug: 'reliance-reliance' },
  { id: 'co-10', name: 'Amazon.com Inc.', ticker: 'AMZN', exchange: 'NASDAQ', country: 'US', sector: 'Consumer Discretionary', industry: 'E-Commerce', logo_url: null, company_page_slug: 'amazon-amzn' },
];

// ──────────────────────────────────────────────
// Helper — create ISO date strings relative to "now"
// ──────────────────────────────────────────────

function daysAgo(n: number, hours = 10): string {
  const d = new Date('2026-05-24T03:00:00+05:30');
  d.setDate(d.getDate() - n);
  d.setHours(hours, 0, 0, 0);
  return d.toISOString();
}

// ──────────────────────────────────────────────
// Featured images (placeholder dimensions)
// ──────────────────────────────────────────────

function makeFeatured(slug: string, alt: string, caption: string, credit: string): MediaAsset {
  return {
    id: `media-${slug}`,
    public_url: `https://media.capitalcolumn.in/articles/${slug}/featured.jpg`,
    alt_text: alt,
    caption,
    credit,
    width: 1600,
    height: 900,
  };
}

// ──────────────────────────────────────────────
// Articles
// ──────────────────────────────────────────────

export const sampleArticles: Article[] = [
  // ── 1. NVIDIA Earnings ──
  {
    id: 'art-001',
    external_id: null,
    slug: 'nvidia-q1-fy27-earnings-data-center-revenue-surges-41-billion',
    title: 'NVIDIA Q1 FY27: Data Center Revenue Surges Past $41 Billion as AI Demand Accelerates',
    dek: 'Jensen Huang's chipmaker posts another blockbuster quarter, but guidance hints at supply tightening for Blackwell Ultra.',
    summary: 'NVIDIA reported Q1 FY27 revenue of $52.1 billion, up 69% year-over-year, driven by record data center sales of $41.3 billion. Gross margins held at 78.4% despite the ongoing Blackwell ramp. The company guided Q2 revenue of $55–57 billion, above consensus estimates.',
    body_markdown: `## Data Center Dominance Continues

NVIDIA's data center segment delivered $41.3 billion in revenue during Q1 FY27, representing 79% of total company sales and a staggering 82% increase from the year-ago quarter. The growth was fueled by hyperscaler deployments of Blackwell GPUs and the early ramp of the Blackwell Ultra architecture.

CEO Jensen Huang characterized the demand environment as "insatiable," noting that cloud providers, sovereign AI initiatives, and enterprise customers are all expanding their GPU clusters simultaneously.

> "We are at the beginning of a new industrial revolution. Every data center in the world is being re-architected for accelerated computing and generative AI," Huang said during the earnings call.

## Financial Highlights

- **Revenue:** $52.1 billion (vs. $51.4B consensus), up 69% YoY
- **Data Center Revenue:** $41.3 billion, up 82% YoY
- **Gaming Revenue:** $3.8 billion, up 12% YoY
- **Gross Margin:** 78.4% GAAP, slightly above guidance of 77.5–78%
- **Net Income:** $29.4 billion, up 74% YoY
- **Diluted EPS:** $1.19 (vs. $1.14 consensus)

## Blackwell Ultra and Rubin Architecture

Management provided the first detailed timeline for the Blackwell Ultra GPU, expected to begin volume shipments in Q3 FY27. The next-generation Rubin architecture, built on TSMC's N3P process, remains on track for a 2027 calendar year introduction.

Huang emphasized that NVIDIA's annual product cadence — Blackwell, Blackwell Ultra, Rubin, Rubin Ultra — is designed to maintain the company's competitive moat against AMD's MI400 and custom silicon from hyperscalers.

## Supply Chain and Margins

CFO Colette Kress noted that CoWoS advanced packaging capacity remains the primary bottleneck, though TSMC has committed to a 60% capacity expansion by mid-2027. Despite higher NRE costs associated with the Blackwell Ultra ramp, gross margins are expected to remain above 77% through the fiscal year.

The company authorized an additional $25 billion share buyback program, bringing the total outstanding authorization to $38 billion.

## Outlook and Guidance

For Q2 FY27, NVIDIA guided revenue of $55–57 billion, implying continued sequential growth of 6–10%. The midpoint of $56 billion compares to the prior consensus estimate of $53.8 billion.

Analysts flagged potential risks including the Department of Commerce's updated AI chip export rules, which could affect sales to certain Middle Eastern and Southeast Asian markets. NVIDIA said it is working with regulators to ensure compliance while preserving market access.`,
    status: 'published',
    language: 'en',
    article_type: 'earnings',
    category: sampleCategories[1], // Earnings
    tags: [sampleTags[0], sampleTags[2], sampleTags[6]], // AI, Semiconductors, Quarterly Results
    tickers: [sampleCompanies[2]], // NVDA
    sources: [
      { id: 'src-001a', source_name: 'NVIDIA Q1 FY27 Press Release', source_url: 'https://nvidianews.nvidia.com/news/fy27-q1-earnings', source_type: 'press_release', publisher: 'NVIDIA Corporation', published_at: daysAgo(0, 6), accessed_at: daysAgo(0, 7), relevance_note: 'Primary earnings data', quote_used: null, is_primary_source: true },
      { id: 'src-001b', source_name: 'NVIDIA Q1 FY27 10-Q Filing', source_url: 'https://sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001045810', source_type: 'company_filing', publisher: 'SEC EDGAR', published_at: daysAgo(0, 6), accessed_at: daysAgo(0, 8), relevance_note: 'SEC filing for detailed financials', quote_used: null, is_primary_source: true },
      { id: 'src-001c', source_name: 'NVIDIA Earnings Call Transcript', source_url: 'https://seekingalpha.com/article/nvidia-q1-fy27-call-transcript', source_type: 'news_article', publisher: 'Seeking Alpha', published_at: daysAgo(0, 7), accessed_at: daysAgo(0, 9), relevance_note: 'Jensen Huang and Colette Kress quotes', quote_used: 'We are at the beginning of a new industrial revolution.', is_primary_source: false },
    ],
    author: authorAI,
    published_at: daysAgo(0, 8),
    scheduled_at: null,
    created_at: daysAgo(0, 5),
    updated_at: daysAgo(0, 8),
    reading_time_minutes: 7,
    featured_image: makeFeatured('nvidia-q1-fy27', 'NVIDIA Blackwell GPU server rack in a data center', 'NVIDIA's Blackwell GPUs continue to dominate enterprise AI deployments', 'NVIDIA Corporation'),
    seo_title: 'NVIDIA Q1 FY27 Earnings: Data Center Revenue $41B, Beats Estimates | CapitalColumn',
    seo_description: 'NVIDIA reports Q1 FY27 revenue of $52.1B, up 69% YoY. Data center revenue hits $41.3B. Blackwell Ultra timeline and Q2 guidance details.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'earnings-analyzer-v3',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.96,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'NVIDIA Q1 FY27 revenue of $52.1B beat consensus by $700M, driven by data center growth of 82% YoY.',
      'Blackwell Ultra GPUs expected to begin volume shipments in Q3 FY27; Rubin architecture on track for 2027.',
      'Gross margins held at 78.4% despite higher ramp costs, above the guided range.',
      'Q2 revenue guidance of $55–57B implies continued sequential momentum and exceeded Wall Street expectations.',
      'New $25B buyback authorization signals management confidence in sustained free cash flow generation.',
    ],
  },

  // ── 2. Sensex / Indian Markets ──
  {
    id: 'art-002',
    external_id: null,
    slug: 'sensex-nifty-record-highs-fii-inflows-may-2026',
    title: 'Sensex Breaches 87,000 for the First Time as FII Inflows Hit ₹18,400 Crore in May',
    dek: 'A broad-based rally led by banking and IT heavyweights pushes benchmark indices to uncharted territory.',
    summary: 'The BSE Sensex surged past the 87,000 mark for the first time on Friday, gaining 843 points to close at 87,126. The Nifty50 ended at 26,410, up 1.02%. Foreign institutional investors have poured ₹18,400 crore into Indian equities in May so far, reversing three months of net selling.',
    body_markdown: `## Record-Breaking Session

Indian equity benchmarks extended their winning streak to seven consecutive sessions on Friday, with the Sensex closing above 87,000 for the first time in history. The 30-share index gained 843.62 points (0.98%) to end at 87,126.14, while the broader Nifty50 added 268 points to settle at 26,410.35.

The rally was broad-based, with 2,417 stocks advancing against 1,089 declines on the BSE. Market breadth remained strongly positive throughout the session.

## What's Driving the Rally

Several factors converged to push markets higher:

- **FII flows reversal:** Foreign institutional investors have turned net buyers in May, pumping in ₹18,400 crore through May 23 after three consecutive months of outflows totaling ₹42,000 crore. Analysts attribute the reversal to India's relative outperformance versus other emerging markets and a weakening dollar.

- **Banking sector strength:** HDFC Bank (+2.8%), ICICI Bank (+2.1%), and SBI (+3.4%) led the advance as credit growth data for April showed a 14-month high of 13.2% year-over-year.

- **IT recovery:** TCS (+1.9%) and Infosys (+2.3%) gained on reports of accelerating deal pipeline activity in North American BFSI clients. Wipro hit a 52-week high.

- **Policy tailwinds:** The RBI's April rate cut of 25 basis points continues to feed through to lower lending rates, supporting consumer and corporate borrowing.

## Sectoral Performance

| Sector | Change |
|---|---|
| Nifty Bank | +1.4% |
| Nifty IT | +1.8% |
| Nifty Financial Services | +1.3% |
| Nifty Auto | +0.6% |
| Nifty Pharma | –0.2% |
| Nifty Metal | –0.5% |

## Expert Views

Veteran market strategist Ridham Desai of Morgan Stanley reiterated his year-end Sensex target of 95,000, calling the current rally "earnings-driven and sustainable." He noted that India's corporate profit-to-GDP ratio has climbed to 5.1%, the highest since 2008.

However, some caution remains. CLSA's Vikash Kumar Jain warned that valuations at 22.3x forward earnings leave limited room for disappointment in the upcoming Q1 FY27 results season beginning in July.

## Technical Outlook

The Nifty50 has decisively broken above its previous resistance at 26,200, which now becomes support. The next significant resistance lies at 26,800, a level derived from the 161.8% Fibonacci extension of the March–April correction. The 14-day RSI stands at 72.4, indicating overbought conditions that may prompt a short-term consolidation.

Market participants will watch Monday's session closely for follow-through buying, with all eyes on the US PCE inflation data due later that evening.`,
    status: 'published',
    language: 'en',
    article_type: 'market_update',
    category: sampleCategories[0], // Markets
    tags: [sampleTags[3], sampleTags[4]], // Interest Rates, Inflation
    tickers: [sampleCompanies[5], sampleCompanies[6], sampleCompanies[7]], // HDFCBANK, TCS, INFY
    sources: [
      { id: 'src-002a', source_name: 'BSE Market Statistics', source_url: 'https://www.bseindia.com/markets.html', source_type: 'market_data', publisher: 'BSE India', published_at: daysAgo(0, 16), accessed_at: daysAgo(0, 16), relevance_note: 'Official closing prices and breadth data', quote_used: null, is_primary_source: true },
      { id: 'src-002b', source_name: 'NSDL FII/FPI Data', source_url: 'https://www.fpi.nsdl.co.in/web/Reports/Latest.aspx', source_type: 'market_data', publisher: 'NSDL', published_at: daysAgo(0, 15), accessed_at: daysAgo(0, 16), relevance_note: 'FII monthly flow data for May 2026', quote_used: null, is_primary_source: true },
    ],
    author: authorPriya,
    published_at: daysAgo(0, 16),
    scheduled_at: null,
    created_at: daysAgo(0, 15),
    updated_at: daysAgo(0, 17),
    reading_time_minutes: 5,
    featured_image: makeFeatured('sensex-87000', 'BSE building in Mumbai with digital ticker showing Sensex at record high', 'The Sensex closed above 87,000 for the first time on May 23, 2026', 'BSE India'),
    seo_title: 'Sensex Crosses 87,000 First Time: FII Flows, Banking Rally | CapitalColumn',
    seo_description: 'BSE Sensex breaches 87,000 for the first time. FII inflows reach ₹18,400 crore in May. Banking and IT sectors lead the broad-based rally.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: false,
    is_editor_reviewed: true,
    ai_pipeline_name: null,
    ai_model_name: null,
    confidence_score: null,
    fact_check_status: 'human_checked',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Sensex closed above 87,000 for the first time, gaining 843 points to end at 87,126.',
      'FIIs have invested ₹18,400 crore in May, reversing three months of net selling.',
      'Banking sector led the rally on strong credit growth data at a 14-month high.',
      'Nifty50 at 22.3x forward earnings — valuations elevated but supported by earnings growth.',
    ],
  },

  // ── 3. HDFC Bank Analysis ──
  {
    id: 'art-003',
    external_id: null,
    slug: 'hdfc-bank-deposit-growth-strategy-casa-ratio-analysis',
    title: 'HDFC Bank's Deposit Mobilization Push Is Working — But the CASA Ratio Tells a Different Story',
    dek: 'Twelve months after the mega-merger, HDFC Bank is winning the deposit war but losing the low-cost funding battle.',
    summary: 'HDFC Bank has added ₹3.2 lakh crore in total deposits since the HDFC Ltd. merger, but its CASA ratio has declined from 42.8% to 37.4%. The bank is deploying branch expansion, digital fixed deposits, and salary account campaigns to rebuild its retail deposit franchise.',
    body_markdown: `## The Post-Merger Deposit Challenge

HDFC Bank's merger with HDFC Ltd. created India's largest private-sector bank by assets, but it also inherited a structural challenge: HDFC Ltd.'s ₹6.2 lakh crore loan book was primarily funded by wholesale borrowings and bonds, not retail deposits. Converting that funding mix has been CEO Sashidhar Jagdishan's top priority.

Twelve months in, the numbers tell a mixed story. Total deposits have grown 21% year-over-year to ₹24.8 lakh crore, a pace well ahead of the industry's 12% growth rate. However, the all-important CASA (Current Account Savings Account) ratio has slipped from 42.8% pre-merger to 37.4% as of March 2026.

## Why CASA Matters

The CASA ratio is the lifeblood of a retail bank's profitability. Current accounts pay zero interest; savings accounts pay 2.75–3.5%. In contrast, term deposits cost 6.5–7.25%. Every percentage point decline in CASA directly compresses net interest margins.

HDFC Bank's NIM stood at 3.46% in Q4 FY26, down from 3.67% a year ago. Management has guided for NIM stabilization at 3.50–3.60% by Q2 FY27 as deposit repricing works through the system.

## The Branch Expansion Strategy

To rebuild CASA, HDFC Bank is pursuing an aggressive branch expansion:

- **800 new branches** opened in FY26, taking the total to 9,200
- **Target of 12,000 branches** by March 2028
- Focus on Tier 2/3 cities where savings account growth rates are 2x urban markets
- New "Smart Branch" format with 30% lower operating costs

The bank has also launched **PayZapp 3.0**, a revamped digital banking app aimed at capturing salary accounts from the 10 million HDFC home loan customers who currently bank elsewhere.

## Competitive Landscape

HDFC Bank is not operating in a vacuum. ICICI Bank's CASA ratio stands at 44.2%, and Kotak Mahindra Bank leads private peers at 50.1%. SBI, the public sector behemoth, maintains a 40.8% CASA ratio backed by its 22,000-branch network.

Jefferies analyst Prakhar Agarwal notes: "HDFC Bank's deposit growth rate is impressive, but the quality of deposits matters more than volume. We need to see CASA back above 40% before we can call the integration fully successful."

## Investment Implications

Despite the CASA headwinds, HDFC Bank trades at 2.7x FY27E book value, a 15% discount to its 5-year average of 3.2x. Bulls argue that the CASA normalization is a matter of time, while bears point to compressed margins and rising competition from fintechs in the salary account space.

The stock has gained 18% year-to-date, outperforming the Nifty Bank index by 4 percentage points. Consensus target price implies 12% upside from current levels.`,
    status: 'published',
    language: 'en',
    article_type: 'analysis',
    category: sampleCategories[4], // Banking & Finance
    tags: [sampleTags[7], sampleTags[5]], // Valuation, M&A
    tickers: [sampleCompanies[5]], // HDFCBANK
    sources: [
      { id: 'src-003a', source_name: 'HDFC Bank FY26 Annual Report', source_url: 'https://www.hdfcbank.com/personal/about-us/investor-relations/annual-reports', source_type: 'company_filing', publisher: 'HDFC Bank', published_at: daysAgo(5), accessed_at: daysAgo(1), relevance_note: 'Deposit composition and CASA ratio data', quote_used: null, is_primary_source: true },
      { id: 'src-003b', source_name: 'Jefferies Initiating Coverage Note', source_url: 'https://www.jefferies.com/research/', source_type: 'news_article', publisher: 'Jefferies', published_at: daysAgo(3), accessed_at: daysAgo(1), relevance_note: 'Analyst quote on CASA normalization', quote_used: 'We need to see CASA back above 40% before we can call the integration fully successful.', is_primary_source: false },
      { id: 'src-003c', source_name: 'RBI Scheduled Commercial Banks Data', source_url: 'https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx', source_type: 'official_statement', publisher: 'Reserve Bank of India', published_at: daysAgo(7), accessed_at: daysAgo(1), relevance_note: 'Industry-level deposit and credit growth figures', quote_used: null, is_primary_source: false },
    ],
    author: authorPriya,
    published_at: daysAgo(1, 9),
    scheduled_at: null,
    created_at: daysAgo(2, 14),
    updated_at: daysAgo(1, 11),
    reading_time_minutes: 8,
    featured_image: makeFeatured('hdfc-bank-casa', 'HDFC Bank branch exterior in Mumbai', 'HDFC Bank aims to reach 12,000 branches by 2028 to boost its CASA ratio', 'CapitalColumn'),
    seo_title: 'HDFC Bank CASA Ratio Falls to 37.4%: Deposit Growth Analysis | CapitalColumn',
    seo_description: 'HDFC Bank post-merger deposit analysis. CASA ratio drops to 37.4% despite ₹3.2 lakh crore deposit addition. Branch expansion and NIM outlook.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'deep-analysis-v2',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.93,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'HDFC Bank deposits grew 21% YoY to ₹24.8 lakh crore, well above the industry average.',
      'CASA ratio declined from 42.8% to 37.4% post-merger, compressing net interest margins to 3.46%.',
      '800 new branches opened in FY26 with a target of 12,000 by March 2028.',
      'Stock trades at 2.7x book value, a 15% discount to its 5-year average.',
    ],
  },

  // ── 4. Tesla India Entry ──
  {
    id: 'art-004',
    external_id: null,
    slug: 'tesla-india-manufacturing-plant-maharashtra-ev-push',
    title: 'Tesla Confirms $2 Billion Maharashtra Manufacturing Plant, Aims to Sell Model 2 Under ₹25 Lakh',
    dek: 'Elon Musk's long-delayed India entry gets real with a Chakan plant announcement and aggressive localization targets.',
    summary: 'Tesla has signed an MoU with the Maharashtra government to set up a $2 billion manufacturing facility near Pune. The plant will produce the Model 2 compact sedan, targeting a sub-₹25 lakh price point through 60% local sourcing. Production is expected to begin in H2 2028.',
    body_markdown: `## The India Bet Finally Materializes

After years of false starts, import duty negotiations, and public back-and-forth between Elon Musk and Indian policymakers, Tesla Inc. has formally committed to manufacturing in India. The company signed a Memorandum of Understanding (MoU) with the Maharashtra Industrial Development Corporation (MIDC) on Thursday for a 500-acre site near Chakan, Pune.

The $2 billion investment will be phased over five years, with Phase 1 targeting annual capacity of 100,000 units. Tesla plans to manufacture the upcoming Model 2 compact sedan, a vehicle specifically designed for price-sensitive markets including India, Southeast Asia, and Latin America.

## Pricing Strategy: Sub-₹25 Lakh

Tesla's India-specific pricing strategy hinges on aggressive localization. The company has committed to sourcing 60% of components locally by volume within two years of production start, rising to 80% by 2031. Key localization targets include:

- **Battery packs:** Negotiations with Tata Group's Agratas (formerly Tata AutoComp) for local cell assembly
- **Electric motors:** Likely to be sourced from Bharat FIH or a JV partner
- **Body-in-white:** Gigacasting equipment to be installed at the Chakan plant
- **Electronics:** Semiconductor and sensor integration through existing Bosch India facilities

At a sub-₹25 lakh price point (approximately $29,000), the Model 2 would compete directly with the Tata Curvv EV, Mahindra BE 6, and Hyundai Creta Electric. However, Tesla's brand premium and supercharger network could command a meaningful differentiation.

## Government Incentives

Maharashtra is offering Tesla a customized incentive package under the state's EV policy:

- **Stamp duty exemption** for land acquisition
- **Electricity subsidy** of ₹1/unit for five years
- **Property tax holiday** for seven years
- **Additional PLI benefits** under the central government's ₹26,000 crore auto PLI scheme

Commerce Minister Piyush Goyal described the deal as "a watershed moment for India's EV ecosystem" and noted that Tesla's entry would catalyze the domestic EV supply chain.

## Skeptics Remain

Not everyone is convinced. Avik Chattopadhyay, a veteran auto industry consultant, cautioned that "Tesla's track record on international manufacturing timelines is poor — Gigafactory Berlin was delayed by two years. Indian infrastructure, land acquisition, and regulatory challenges could add further delays."

Market analysts also flag currency risk. If the rupee depreciates significantly against the dollar, Tesla's imported content costs could erode the sub-₹25 lakh pricing target.

## Impact on Incumbent EV Players

Tata Motors shares fell 3.2% on the announcement, while Mahindra & Mahindra dipped 1.8%. The Nifty Auto index underperformed the broader market by 1.1% on the day.

However, Goldman Sachs analyst Chandresh Singh argues that Tesla's entry is "net positive for the entire EV ecosystem" as it validates India as a manufacturing hub and will accelerate charging infrastructure buildout.`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[2], // Companies
    tags: [sampleTags[1]], // EV
    tickers: [sampleCompanies[3]], // TSLA
    sources: [
      { id: 'src-004a', source_name: 'Maharashtra Government Press Release', source_url: 'https://maharashtra.gov.in/press-releases/tesla-mou', source_type: 'press_release', publisher: 'Government of Maharashtra', published_at: daysAgo(1, 11), accessed_at: daysAgo(1, 12), relevance_note: 'Official MoU announcement with investment details', quote_used: null, is_primary_source: true },
      { id: 'src-004b', source_name: 'Tesla 8-K Filing', source_url: 'https://sec.gov/cgi-bin/browse-edgar?company=tesla&CIK=&type=8-K', source_type: 'company_filing', publisher: 'SEC EDGAR', published_at: daysAgo(1, 10), accessed_at: daysAgo(1, 12), relevance_note: 'SEC disclosure of India manufacturing commitment', quote_used: null, is_primary_source: true },
    ],
    author: authorDesk,
    published_at: daysAgo(1, 11),
    scheduled_at: null,
    created_at: daysAgo(1, 10),
    updated_at: daysAgo(1, 14),
    reading_time_minutes: 6,
    featured_image: makeFeatured('tesla-india-plant', 'Rendering of Tesla manufacturing plant in Chakan, Maharashtra', 'Tesla's planned Chakan facility will have initial annual capacity of 100,000 units', 'Tesla Inc.'),
    seo_title: 'Tesla India: $2B Maharashtra Plant, Model 2 Under ₹25 Lakh | CapitalColumn',
    seo_description: 'Tesla signs MoU for $2B manufacturing plant near Pune. Model 2 to be priced under ₹25 lakh with 60% local sourcing. Production from H2 2028.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'breaking-news-v2',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.91,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Tesla signs MoU with Maharashtra for a $2 billion manufacturing plant near Pune.',
      'Model 2 compact sedan to be priced under ₹25 lakh with 60% local component sourcing.',
      'Phase 1 capacity of 100,000 units annually; production expected to begin in H2 2028.',
      'Tata Motors and Mahindra shares dipped on the announcement as competition intensifies.',
    ],
  },

  // ── 5. TCS Deal Win ──
  {
    id: 'art-005',
    external_id: null,
    slug: 'tcs-wins-3-billion-boa-digital-transformation-deal',
    title: 'TCS Bags $3 Billion Multi-Year Deal with Bank of America for Cloud and AI Transformation',
    dek: 'India's largest IT services firm secures its biggest-ever contract, signaling a revival in large deal closures.',
    summary: 'Tata Consultancy Services has won a $3 billion, eight-year engagement with Bank of America covering cloud migration, AI-powered risk analytics, and core banking modernization. The deal is TCS's largest single contract and represents a significant win in the competitive BFSI vertical.',
    body_markdown: `## A Landmark Contract

TCS announced on Wednesday that it has been selected by Bank of America as its primary technology transformation partner in a deal valued at approximately $3 billion over eight years. The engagement encompasses three major workstreams:

1. **Cloud migration:** Moving 60% of Bank of America's on-premise workloads to a hybrid multi-cloud environment spanning Azure and private cloud infrastructure
2. **AI-powered risk analytics:** Building next-generation credit risk, market risk, and fraud detection models using TCS's proprietary ignio AIOps platform
3. **Core banking modernization:** Replacing legacy mainframe systems with a microservices-based architecture

The deal was signed after a competitive evaluation that included Accenture, Infosys, and IBM. TCS's combination of deep BFSI domain expertise, cost arbitrage, and AI platform capabilities reportedly differentiated its proposal.

## Financial Impact

At $3 billion over eight years, the contract translates to approximately $375 million in annual revenue — roughly 1.4% of TCS's trailing twelve-month revenue of $30.1 billion. While the immediate revenue impact is modest relative to TCS's scale, the deal carries significant strategic value:

- **Margin accretive:** Large annuity contracts typically carry operating margins 200–300 basis points above company average after the initial ramp
- **Reference win:** Bank of America is the second-largest US bank by assets, providing TCS a powerful reference in the competitive US BFSI market
- **Platform revenue:** The ignio AI deployment creates a sticky, high-margin platform revenue stream

## Deal Pipeline and Industry Context

TCS CEO K. Krithivasan noted during a media call that the deal is "emblematic of a broader shift in client spending patterns." After 18 months of discretionary spending cuts, large financial institutions are now committing to multi-year transformation programs rather than piecemeal projects.

TCS's order book for Q4 FY26 stood at $13.2 billion in total contract value (TCV), the highest in six quarters. Peer Infosys reported TCV of $8.3 billion in the same period.

## Stock Reaction

TCS shares rose 4.1% to ₹4,520 following the announcement, adding approximately ₹65,000 crore to its market capitalization. The stock is now up 22% year-to-date, making it the second-best performer in the Nifty IT index after Persistent Systems.

Brokerage Motilal Oswal upgraded TCS to "Buy" from "Neutral," raising the target price to ₹5,000, citing improved visibility on large deal momentum and margin expansion potential.`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[3], // Technology
    tags: [sampleTags[0], sampleTags[5]], // AI, M&A
    tickers: [sampleCompanies[6], sampleCompanies[7]], // TCS, INFY
    sources: [
      { id: 'src-005a', source_name: 'TCS Press Release', source_url: 'https://www.tcs.com/insights/press-releases/tcs-bank-of-america-deal', source_type: 'press_release', publisher: 'TCS', published_at: daysAgo(2, 9), accessed_at: daysAgo(2, 10), relevance_note: 'Official deal announcement', quote_used: null, is_primary_source: true },
      { id: 'src-005b', source_name: 'TCS BSE Filing', source_url: 'https://www.bseindia.com/corporates/anndet_new.aspx?newsid=', source_type: 'exchange_disclosure', publisher: 'BSE India', published_at: daysAgo(2, 8), accessed_at: daysAgo(2, 10), relevance_note: 'Exchange filing with deal value disclosure', quote_used: null, is_primary_source: true },
    ],
    author: authorRahul,
    published_at: daysAgo(2, 10),
    scheduled_at: null,
    created_at: daysAgo(2, 8),
    updated_at: daysAgo(2, 12),
    reading_time_minutes: 5,
    featured_image: makeFeatured('tcs-boa-deal', 'TCS logo alongside Bank of America signage', 'TCS wins its largest-ever contract with Bank of America', 'CapitalColumn'),
    seo_title: 'TCS Wins $3 Billion Bank of America Deal for Cloud & AI | CapitalColumn',
    seo_description: 'TCS secures $3B, 8-year contract with Bank of America for cloud migration, AI risk analytics, and core banking modernization.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: false,
    is_editor_reviewed: true,
    ai_pipeline_name: null,
    ai_model_name: null,
    confidence_score: null,
    fact_check_status: 'human_checked',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'TCS wins its largest-ever contract: $3 billion over 8 years with Bank of America.',
      'Deal covers cloud migration, AI risk analytics via ignio, and core banking modernization.',
      'Annual revenue contribution of ~$375M, roughly 1.4% of TCS trailing revenue.',
      'TCS shares rose 4.1% to ₹4,520; Motilal Oswal upgraded the stock to Buy with ₹5,000 target.',
    ],
  },

  // ── 6. Apple AI iPhone ──
  {
    id: 'art-006',
    external_id: null,
    slug: 'apple-intelligence-wwdc-2026-ios-20-on-device-ai',
    title: 'Apple Bets Big on On-Device AI at WWDC 2026: New M5 Neural Engine Powers "Personal Intelligence"',
    dek: 'Apple's AI strategy doubles down on privacy with a local-first approach that could redefine the smartphone upgrade cycle.',
    summary: 'At WWDC 2026, Apple unveiled "Personal Intelligence" — a suite of on-device AI capabilities powered by the M5 Neural Engine, running entirely on-device without cloud dependency. Features include real-time language translation, proactive health alerts, and AI-native app experiences in iOS 20.',
    body_markdown: `## A Privacy-First AI Vision

Apple's annual developer conference opened with a clear message: the future of AI is personal, private, and local. CEO Tim Cook introduced "Personal Intelligence" as Apple's next-generation AI platform, emphasizing that all core features run entirely on-device using the new M5 Neural Engine.

"We believe your personal data should power your personal intelligence — and it should never leave your device," Cook said during the keynote at Apple Park.

## iOS 20: AI-Native from the Ground Up

The most significant announcement was iOS 20, which integrates AI capabilities into every layer of the operating system:

- **Proactive Siri:** A completely rebuilt Siri that understands context across apps, maintains conversation history, and can execute multi-step actions like "Book my usual dinner reservation and text my wife the details"
- **Live Translation:** Real-time translation in 40 languages during phone calls and FaceTime, processed entirely on-device
- **Health Intelligence:** AI-powered analysis of Apple Watch health data that can detect early signs of atrial fibrillation, sleep apnea, and metabolic irregularities
- **Photo Intelligence:** Advanced photo search using natural language ("Find photos of Mom at the beach from last summer") and AI-generated photo albums

## The M5 Neural Engine

The M5 chip's Neural Engine delivers 45 TOPS (trillion operations per second), a 2.5x improvement over the M4. Apple claims this enables running a 7-billion parameter language model on-device at 30 tokens per second — fast enough for real-time conversational AI without cloud connectivity.

This is a direct competitive response to Google's Gemini Nano and Qualcomm's NPU-based on-device AI capabilities. However, Apple's tight hardware-software integration gives it an optimization advantage that third-party chip-OS combinations cannot easily match.

## Developer Implications

Apple released new frameworks for developers:

- **IntelligenceKit:** A framework for building AI-native app experiences using Apple's on-device models
- **ModelGarden:** A tool for developers to fine-tune Apple's base models with their own data, with training happening on-device
- **AIActions:** An API that allows third-party apps to expose functionality to Siri's new multi-step action capability

## Market Impact

Apple shares rose 2.8% in after-hours trading following the keynote. Analysts at Morgan Stanley estimate that AI-native iOS features could drive an iPhone upgrade super-cycle, with 350 million iPhones in the installed base more than 3 years old and eligible for upgrade.

The announcement puts pressure on Samsung and Google, which have relied on cloud-based AI features. Apple's privacy narrative could prove particularly compelling in the EU market, where data privacy regulations favor on-device processing.`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[3], // Technology
    tags: [sampleTags[0]], // AI
    tickers: [sampleCompanies[0], sampleCompanies[1]], // AAPL, MSFT
    sources: [
      { id: 'src-006a', source_name: 'Apple WWDC 2026 Keynote', source_url: 'https://www.apple.com/apple-events/wwdc-2026/', source_type: 'press_release', publisher: 'Apple Inc.', published_at: daysAgo(2, 20), accessed_at: daysAgo(2, 21), relevance_note: 'Official WWDC keynote announcements', quote_used: 'We believe your personal data should power your personal intelligence.', is_primary_source: true },
      { id: 'src-006b', source_name: 'Apple Developer Documentation', source_url: 'https://developer.apple.com/documentation/intelligencekit', source_type: 'official_statement', publisher: 'Apple Inc.', published_at: daysAgo(2, 20), accessed_at: daysAgo(2, 22), relevance_note: 'Technical details on IntelligenceKit and ModelGarden', quote_used: null, is_primary_source: true },
    ],
    author: authorRahul,
    published_at: daysAgo(2, 21),
    scheduled_at: null,
    created_at: daysAgo(2, 19),
    updated_at: daysAgo(2, 22),
    reading_time_minutes: 6,
    featured_image: makeFeatured('apple-wwdc-2026', 'Tim Cook on stage at Apple Park presenting Personal Intelligence features', 'Apple CEO Tim Cook unveils Personal Intelligence at WWDC 2026', 'Apple Inc.'),
    seo_title: 'Apple WWDC 2026: Personal Intelligence, M5 Neural Engine, iOS 20 | CapitalColumn',
    seo_description: 'Apple unveils Personal Intelligence at WWDC 2026. M5 Neural Engine delivers 45 TOPS for on-device AI. iOS 20 features AI-native Siri, health alerts.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'breaking-news-v2',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.94,
    fact_check_status: 'ai_checked',
    correction_note: 'Updated M5 Neural Engine TOPS figure from 42 to 45 based on Apple's corrected spec sheet.',
    last_corrected_at: daysAgo(2, 23),
    key_takeaways: [
      'Apple unveils "Personal Intelligence" — on-device AI running entirely without cloud dependency.',
      'M5 Neural Engine delivers 45 TOPS, enabling a 7B parameter language model at 30 tokens/second.',
      'iOS 20 includes rebuilt Siri with multi-step actions, live translation in 40 languages, and AI health alerts.',
      'New developer frameworks IntelligenceKit and ModelGarden enable third-party AI-native apps.',
      'Morgan Stanley estimates 350M upgrade-eligible iPhones could drive a super-cycle.',
    ],
  },

  // ── 7. Reliance Jio IPO ──
  {
    id: 'art-007',
    external_id: null,
    slug: 'reliance-jio-ipo-drhp-sebi-filing-2026',
    title: 'Reliance Jio Files DRHP with SEBI for ₹70,000 Crore IPO — India\'s Largest-Ever Public Offering',
    dek: 'Mukesh Ambani's telecom giant moves toward a long-anticipated listing that could value Jio Platforms at ₹12 lakh crore.',
    summary: 'Jio Platforms Ltd. has filed its Draft Red Herring Prospectus (DRHP) with SEBI for an IPO expected to raise ₹70,000 crore ($8.3 billion). The offering will include a ₹30,000 crore fresh issue and ₹40,000 crore offer for sale by Reliance Industries and pre-IPO investors.',
    body_markdown: `## The Filing

Jio Platforms Ltd., the digital services arm of Reliance Industries, filed its Draft Red Herring Prospectus with the Securities and Exchange Board of India on Tuesday. The IPO is structured as a combination of:

- **Fresh issue:** ₹30,000 crore to fund 5G densification, AI infrastructure, and JioAirFiber expansion
- **Offer for sale:** ₹40,000 crore, with Reliance Industries selling ₹25,000 crore and pre-IPO investors (Meta, Google, KKR, Silver Lake, and others) selling ₹15,000 crore

At the upper end of the expected price band, Jio Platforms would be valued at approximately ₹12 lakh crore ($143 billion), making it India's third most valuable company after Reliance Industries itself and TCS.

## Key Financials from the DRHP

| Metric | FY26 | FY25 | Growth |
|---|---|---|---|
| Revenue | ₹1,18,500 Cr | ₹1,02,300 Cr | 15.8% |
| EBITDA | ₹53,200 Cr | ₹45,800 Cr | 16.2% |
| EBITDA Margin | 44.9% | 44.8% | +10 bps |
| Net Profit | ₹26,400 Cr | ₹21,900 Cr | 20.5% |
| Subscribers | 498 million | 472 million | 5.5% |
| ARPU | ₹198.5 | ₹182.3 | 8.9% |

## Subscriber Metrics and 5G Leadership

Jio ended FY26 with 498 million subscribers, of which 182 million are on 5G plans. The company claims 68% population coverage with its 5G standalone network, ahead of Bharti Airtel's 55%. True 5G (SA) coverage is a key differentiator, as Jio's network is built on a standalone architecture versus Airtel's non-standalone deployment.

Average Revenue Per User (ARPU) has climbed steadily from ₹182.3 to ₹198.5 following two rounds of tariff hikes in FY26. Management has indicated that ARPU of ₹250 is needed for "healthy return on capital" and further hikes are likely in FY27.

## Use of Proceeds

The ₹30,000 crore fresh issue will be deployed across:

- **5G network densification:** ₹12,000 crore for additional cell towers and small cells in urban areas
- **AI and cloud infrastructure:** ₹8,000 crore for Jio AI Cloud, the company's enterprise cloud offering
- **JioAirFiber expansion:** ₹5,000 crore to take fixed wireless access to 100 million households
- **General corporate purposes:** ₹5,000 crore

## Market Implications

The Jio IPO would surpass LIC's ₹21,000 crore offering in 2022 as India's largest-ever public offering. Bankers estimate the issue could attract retail oversubscription of 8–10x, requiring significant allocation planning.

Reliance Industries shares rose 1.8% on the filing news. Analysts note that a successful Jio listing would crystallize value for Reliance shareholders and potentially trigger a re-rating of the parent company's conglomerate discount.

Goldman Sachs estimates Reliance Industries' sum-of-the-parts value at ₹3,650 per share versus the current market price of ₹3,120, implying 17% upside if Jio, Retail, and O2C are valued at fair multiples.`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[6], // IPOs
    tags: [sampleTags[7]], // Valuation
    tickers: [sampleCompanies[8]], // RELIANCE
    sources: [
      { id: 'src-007a', source_name: 'Jio Platforms DRHP', source_url: 'https://www.sebi.gov.in/filings/public-issues.html', source_type: 'company_filing', publisher: 'SEBI', published_at: daysAgo(3, 10), accessed_at: daysAgo(3, 11), relevance_note: 'Draft Red Herring Prospectus with full financial data', quote_used: null, is_primary_source: true },
      { id: 'src-007b', source_name: 'Reliance Industries BSE Filing', source_url: 'https://www.bseindia.com/corporates/anndet_new.aspx', source_type: 'exchange_disclosure', publisher: 'BSE India', published_at: daysAgo(3, 10), accessed_at: daysAgo(3, 11), relevance_note: 'Parent company disclosure of Jio IPO filing', quote_used: null, is_primary_source: true },
    ],
    author: authorDesk,
    published_at: daysAgo(3, 10),
    scheduled_at: null,
    created_at: daysAgo(3, 8),
    updated_at: daysAgo(3, 12),
    reading_time_minutes: 7,
    featured_image: makeFeatured('jio-ipo-filing', 'Jio Platforms logo with SEBI building in background', 'Jio Platforms files for India\'s largest-ever IPO at ₹70,000 crore', 'CapitalColumn'),
    seo_title: 'Reliance Jio IPO: ₹70,000 Crore DRHP Filed with SEBI | CapitalColumn',
    seo_description: 'Jio Platforms files DRHP for ₹70,000 crore IPO. Valuation at ₹12 lakh crore. Key financials, subscriber data, and use of proceeds.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'breaking-news-v2',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.95,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Jio Platforms files DRHP with SEBI for ₹70,000 crore IPO — India\'s largest-ever.',
      'Offering splits into ₹30,000 crore fresh issue and ₹40,000 crore OFS.',
      'FY26 revenue of ₹1.18 lakh crore with 44.9% EBITDA margin and 498 million subscribers.',
      'Fresh issue proceeds to fund 5G, AI cloud infrastructure, and JioAirFiber expansion.',
      'Implied valuation of ₹12 lakh crore (~$143 billion) would make Jio India\'s third-most-valuable company.',
    ],
  },

  // ── 8. JPMorgan AI Trading ──
  {
    id: 'art-008',
    external_id: null,
    slug: 'jpmorgan-ai-trading-desk-gemini-powered-equities',
    title: 'JPMorgan Deploys AI-Powered Trading Desk Across Equities Division, Cuts Execution Costs by 40%',
    dek: 'The bank's proprietary LOXM-3 system handles 35% of cash equities flow, raising questions about the future of human traders.',
    summary: 'JPMorgan Chase has expanded its AI trading system LOXM-3 to handle 35% of its global cash equities execution, up from 12% a year ago. The system has reduced execution costs by 40% and improved fill rates by 18 basis points, according to the bank\'s technology division.',
    body_markdown: `## The Rise of LOXM-3

JPMorgan Chase's quantitative research division revealed that its proprietary AI trading system, LOXM-3, now handles 35% of the bank's global cash equities execution flow. The system, which uses reinforcement learning and large language models to optimize trade execution, has been rolled out across all major markets including New York, London, Tokyo, and Mumbai.

LOXM-3 represents the third generation of JPMorgan's AI execution platform. Unlike its predecessors, which focused primarily on VWAP and TWAP algorithms, LOXM-3 can:

- **Interpret market microstructure** in real-time, adjusting order placement based on order book dynamics
- **Read and incorporate** news headlines, earnings releases, and social media sentiment into execution decisions
- **Learn from institutional flow patterns** to predict short-term liquidity shifts
- **Adapt execution strategy** mid-trade based on changing market conditions

## Performance Metrics

The bank disclosed impressive performance statistics:

| Metric | Before LOXM-3 | After LOXM-3 | Improvement |
|---|---|---|---|
| Execution Cost (bps) | 4.2 | 2.5 | –40% |
| Fill Rate | 94.1% | 95.9% | +1.8% |
| Market Impact (bps) | 3.8 | 2.1 | –45% |
| Average Latency | 12ms | 3ms | –75% |

These improvements translate to hundreds of millions of dollars in annual savings for JPMorgan's institutional clients, who include sovereign wealth funds, pension funds, and hedge funds.

## Implications for the Trading Floor

The expansion of LOXM-3 has reignited the debate about AI's impact on financial sector employment. JPMorgan currently employs approximately 3,200 equities traders globally. While the bank insists that AI is "augmenting, not replacing" human traders, industry sources suggest that headcount in cash equities execution has declined 15% over the past two years through attrition.

JPMorgan's head of equities trading, Troy Rohrbaugh, pushed back on the replacement narrative: "Our best traders are now working alongside LOXM-3. They focus on complex block trades, client relationships, and situations that require judgment. The AI handles the routine flow."

## Competitive Landscape

JPMorgan is not alone in the AI trading arms race. Goldman Sachs has deployed its own system called Marquee AI across fixed income markets, while Morgan Stanley's AskResearch platform uses AI to surface trading ideas for its salesforce.

However, JPMorgan's scale advantage is significant — the bank's equities division processes approximately $2.8 trillion in daily notional volume, providing the AI system with an unmatched training dataset.

## Regulatory Considerations

The SEC has signaled increased scrutiny of AI-driven trading systems, particularly around issues of market stability, fairness, and transparency. New proposed rules would require broker-dealers to disclose when AI systems are making autonomous execution decisions, though lobbying from major banks has delayed the rulemaking timeline.

European regulators under MiFID III are taking a stricter approach, requiring AI trading systems to maintain human oversight with the ability to immediately halt autonomous execution.`,
    status: 'published',
    language: 'en',
    article_type: 'analysis',
    category: sampleCategories[4], // Banking & Finance
    tags: [sampleTags[0], sampleTags[9]], // AI, Management Change
    tickers: [sampleCompanies[4]], // JPM
    sources: [
      { id: 'src-008a', source_name: 'JPMorgan AI Research Publication', source_url: 'https://www.jpmorgan.com/technology/artificial-intelligence/research', source_type: 'official_statement', publisher: 'JPMorgan Chase', published_at: daysAgo(3, 14), accessed_at: daysAgo(3, 15), relevance_note: 'LOXM-3 performance data and deployment details', quote_used: null, is_primary_source: true },
      { id: 'src-008b', source_name: 'SEC AI Trading Proposed Rulemaking', source_url: 'https://www.sec.gov/rules/proposed.shtml', source_type: 'official_statement', publisher: 'SEC', published_at: daysAgo(10), accessed_at: daysAgo(3, 16), relevance_note: 'Regulatory context for AI trading systems', quote_used: null, is_primary_source: false },
    ],
    author: authorAI,
    published_at: daysAgo(3, 14),
    scheduled_at: null,
    created_at: daysAgo(3, 12),
    updated_at: daysAgo(3, 16),
    reading_time_minutes: 7,
    featured_image: makeFeatured('jpmorgan-ai-trading', 'JPMorgan trading floor with AI-powered screens', 'JPMorgan's LOXM-3 AI system now handles 35% of global cash equities execution', 'JPMorgan Chase'),
    seo_title: 'JPMorgan AI Trading: LOXM-3 Cuts Costs 40%, Handles 35% of Equities Flow | CapitalColumn',
    seo_description: 'JPMorgan expands LOXM-3 AI trading across global equities. Execution costs cut 40%, fill rates up 18bps. Impact on employment and regulation.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'deep-analysis-v2',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.92,
    fact_check_status: 'ai_checked',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'JPMorgan\'s LOXM-3 AI trading system now handles 35% of global cash equities flow, up from 12%.',
      'Execution costs reduced by 40% and fill rates improved by 18 basis points.',
      'System uses reinforcement learning and LLMs to optimize real-time trade execution.',
      'Equities headcount has declined 15% through attrition despite "augmentation" messaging.',
      'SEC and EU regulators increasing scrutiny of autonomous AI trading systems.',
    ],
  },

  // ── 9. Infosys Wage Hike ──
  {
    id: 'art-009',
    external_id: null,
    slug: 'infosys-q1-fy27-wage-hike-4-percent-attrition-drops',
    title: 'Infosys Rolls Out 4–8% Wage Hikes Effective July 2026, Attrition Falls to 11.2%',
    dek: 'India's second-largest IT firm balances talent retention with margin preservation as the demand environment improves.',
    summary: 'Infosys has announced wage hikes of 4–8% effective July 1, 2026, with higher increments for top performers and employees in AI/cloud skills. The company also reported that trailing twelve-month attrition has fallen to 11.2%, the lowest since Q2 FY22.',
    body_markdown: `## Wage Hike Details

Infosys CEO Salil Parekh confirmed on Thursday that the company will implement annual salary increments effective July 1, 2026. The hikes are structured as follows:

- **Junior employees (0–3 years):** 6–8% average increment
- **Mid-level employees (3–7 years):** 5–7% average increment
- **Senior employees (7+ years):** 4–6% average increment
- **Top performers (top 15%):** Additional 2–3% on top of band-level hikes
- **Critical skills premium:** Employees in AI/ML, cloud architecture, and cybersecurity receive an additional 1–2% premium

The overall wage bill impact is estimated at 150–180 basis points on operating margins in Q2 FY27, which will be partially offset by operating leverage and pyramid optimization.

## Attrition Trends

The more significant story is the continued decline in attrition. Infosys's trailing twelve-month voluntary attrition rate fell to 11.2% in Q4 FY26, down from 14.6% a year ago and a peak of 28.4% during the post-pandemic talent war of FY22.

Chief Human Resources Officer Shaji Mathew attributed the improvement to several factors:

- **Improved career frameworks:** New role-based career paths that provide visibility into 3–5 year growth trajectories
- **Skills-based compensation:** Premium pay for employees who complete certified AI and cloud training programs
- **Hybrid work stabilization:** 3-day office, 2-day remote policy now well-established after initial resistance
- **Industry normalization:** The broader IT industry has seen demand-supply dynamics normalize after the pandemic hiring frenzy

## Margin Implications

Infosys guided FY27 operating margins of 21–23%, consistent with its medium-term target. The Q1 FY27 margin impact from wage hikes is expected to be offset by:

- Lower subcontracting costs as bench strength normalizes
- Pricing improvements in select large deals
- Automation-driven productivity gains, particularly from Infosys Topaz AI platform deployments
- Depreciation of the Indian rupee, which provides a 30–40 bps tailwind per 1% depreciation

## Industry Comparison

| Company | Attrition (TTM) | Wage Hike | Margin Guidance |
|---|---|---|---|
| Infosys | 11.2% | 4–8% | 21–23% |
| TCS | 12.1% | 4–7% | 26–28% |
| Wipro | 14.8% | 3–6% | 16–17.5% |
| HCL Tech | 12.8% | 5–8% | 18–19% |

## Outlook

Parekh reiterated Infosys's FY27 revenue growth guidance of 4–7% in constant currency, noting that the deal pipeline is "healthy across all verticals and geographies." The company's total contract value (TCV) of large deals stood at $8.3 billion in FY26, up 22% from FY25.`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[3], // Technology
    tags: [sampleTags[6], sampleTags[9]], // Quarterly Results, Management Change
    tickers: [sampleCompanies[7]], // INFY
    sources: [
      { id: 'src-009a', source_name: 'Infosys Q4 FY26 Results Presentation', source_url: 'https://www.infosys.com/investors/reports-filings.html', source_type: 'company_filing', publisher: 'Infosys Ltd.', published_at: daysAgo(4, 8), accessed_at: daysAgo(4, 10), relevance_note: 'Attrition data and margin guidance', quote_used: null, is_primary_source: true },
      { id: 'src-009b', source_name: 'Infosys Press Conference Transcript', source_url: 'https://www.infosys.com/newsroom/', source_type: 'press_release', publisher: 'Infosys Ltd.', published_at: daysAgo(4, 9), accessed_at: daysAgo(4, 10), relevance_note: 'Salil Parekh quotes on wage hikes and revenue guidance', quote_used: null, is_primary_source: true },
    ],
    author: authorDesk,
    published_at: daysAgo(4, 10),
    scheduled_at: null,
    created_at: daysAgo(4, 8),
    updated_at: daysAgo(4, 12),
    reading_time_minutes: 5,
    featured_image: makeFeatured('infosys-wage-hike', 'Infosys campus in Bangalore with employees', 'Infosys implements 4–8% wage hikes effective July 2026', 'CapitalColumn'),
    seo_title: 'Infosys Wage Hike 4–8% July 2026, Attrition Falls to 11.2% | CapitalColumn',
    seo_description: 'Infosys announces 4–8% salary hikes from July 2026. Attrition drops to 11.2%, lowest since FY22. Margin impact and industry comparison.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: false,
    is_editor_reviewed: true,
    ai_pipeline_name: null,
    ai_model_name: null,
    confidence_score: null,
    fact_check_status: 'human_checked',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Infosys wage hikes of 4–8% effective July 1, 2026 with AI/cloud skills premiums.',
      'Attrition falls to 11.2% TTM, lowest since Q2 FY22, down from 28.4% peak.',
      'Margin impact of 150–180 bps expected, offset by operating leverage and rupee tailwinds.',
      'FY27 revenue growth guidance maintained at 4–7% in constant currency.',
    ],
  },

  // ── 10. Amazon India Fintech ──
  {
    id: 'art-010',
    external_id: null,
    slug: 'amazon-india-nbfc-license-digital-lending-push',
    title: 'Amazon Secures NBFC License from RBI, Plans to Launch Digital Lending Products for SMEs',
    dek: 'The e-commerce giant deepens its financial services play in India with a focus on merchant lending and Buy Now Pay Later.',
    summary: 'Amazon India has received an NBFC license from the Reserve Bank of India, enabling it to directly originate loans for its marketplace sellers and consumers. The company plans to launch working capital loans, merchant cash advances, and a revamped BNPL product in Q3 2026.',
    body_markdown: `## The NBFC License

Amazon India's financial services subsidiary, Amazon Pay (India) Pvt Ltd., has received an NBFC-ND (Non-Banking Financial Company — Non-Deposit) license from the Reserve Bank of India. The license, granted after a 14-month review process, allows Amazon to directly originate and hold loans on its balance sheet.

Previously, Amazon operated as a loan facilitator through partnerships with Capital Float (now acquired by Amazon), and IDFC First Bank. The NBFC license removes the intermediary layer, allowing Amazon to:

- Set its own underwriting criteria
- Retain the full net interest margin
- Build proprietary credit scoring models using marketplace transaction data
- Offer more competitive rates to sellers

## Product Roadmap

Amazon plans to launch three lending products by Q3 2026:

### 1. Seller Working Capital Loans
- Loan amounts: ₹50,000 to ₹1 crore
- Tenure: 3–12 months
- Interest rates: 12–18% per annum (risk-based pricing)
- Underwriting: Based on Amazon marketplace sales data, fulfillment metrics, and customer ratings

### 2. Merchant Cash Advances
- Automatic daily repayment deducted from seller settlements
- No fixed EMI — repayment scales with sales volume
- Designed for seasonal businesses needing quick access to capital

### 3. Consumer BNPL (Buy Now, Pay Later)
- Revamped Amazon Pay Later with higher limits (up to ₹5 lakh)
- 0% interest for 30 days; 14–16% APR for longer tenures
- Credit assessment using Amazon purchase history and Pay transaction data

## Data Advantage

Amazon's most significant competitive advantage is its proprietary transaction data. With 12 lakh active sellers and 300 million registered customers in India, the company has deep visibility into business cash flows, consumer spending patterns, and credit behavior.

An Amazon executive (speaking on condition of anonymity) noted: "We know a seller's daily sales, return rates, inventory turnover, and customer satisfaction scores. Traditional banks can't match this level of real-time underwriting insight."

## Regulatory and Competitive Context

The RBI has been tightening regulations around digital lending, with recent guidelines requiring full disclosure of loan terms, restrictions on automatic deductions, and mandatory cooling-off periods. Amazon's NBFC structure ensures full regulatory compliance, unlike some fintech platforms that have faced RBI enforcement actions.

Competitors in the SME lending space include Flipkart's lending arm (through Aditya Birla Finance), Google Pay's partnership with banks, and standalone fintech lenders like Lendingkart and NeoGrowth.

## Market Impact

Amazon India's parent, Amazon.com Inc., did not see a material stock price reaction as the India lending business remains a small fraction of global operations. However, analysts note that India's $700 billion SME credit gap represents a massive addressable market, and Amazon's platform-integrated lending model is well-positioned to capture share.`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[4], // Banking & Finance
    tags: [sampleTags[8]], // Debt
    tickers: [sampleCompanies[9]], // AMZN
    sources: [
      { id: 'src-010a', source_name: 'RBI NBFC License Registry', source_url: 'https://www.rbi.org.in/Scripts/NBFCList.aspx', source_type: 'official_statement', publisher: 'Reserve Bank of India', published_at: daysAgo(4, 12), accessed_at: daysAgo(4, 14), relevance_note: 'Official NBFC license grant confirmation', quote_used: null, is_primary_source: true },
      { id: 'src-010b', source_name: 'Amazon India Blog Post', source_url: 'https://www.aboutamazon.in/news/innovations/amazon-india-financial-services', source_type: 'press_release', publisher: 'Amazon India', published_at: daysAgo(4, 11), accessed_at: daysAgo(4, 14), relevance_note: 'Product roadmap and seller lending details', quote_used: null, is_primary_source: true },
    ],
    author: authorAI,
    published_at: daysAgo(4, 13),
    scheduled_at: null,
    created_at: daysAgo(4, 11),
    updated_at: daysAgo(4, 15),
    reading_time_minutes: 6,
    featured_image: makeFeatured('amazon-nbfc', 'Amazon India office with RBI logo overlay', 'Amazon secures NBFC license from RBI for direct lending operations', 'CapitalColumn'),
    seo_title: 'Amazon India Gets NBFC License: SME Lending and BNPL Plans | CapitalColumn',
    seo_description: 'Amazon India receives RBI NBFC license. Plans seller working capital loans, merchant cash advances, and revamped BNPL. Product details and market impact.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'breaking-news-v2',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.90,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Amazon India receives NBFC-ND license from RBI for direct loan origination.',
      'Three lending products planned: seller working capital, merchant cash advances, and consumer BNPL.',
      'Amazon\'s marketplace data provides unique underwriting advantages over traditional banks.',
      'India\'s $700 billion SME credit gap represents a massive addressable market.',
    ],
  },

  // ── 11. Microsoft Azure Earnings ──
  {
    id: 'art-011',
    external_id: null,
    slug: 'microsoft-q3-fy26-azure-ai-revenue-beats-expectations',
    title: 'Microsoft Q3 FY26: Azure Revenue Grows 38% as AI Services Contribute $4.2 Billion Quarterly Run Rate',
    dek: 'Satya Nadella calls AI "the most significant platform shift since the cloud" as Copilot adoption accelerates across enterprise.',
    summary: 'Microsoft reported Q3 FY26 revenue of $68.7 billion, up 16% year-over-year. Azure and cloud services grew 38%, with AI services contributing 12 percentage points. The company raised its FY26 capital expenditure guidance to $62 billion to meet data center demand.',
    body_markdown: `## Cloud Momentum Accelerates

Microsoft delivered a strong Q3 FY26, with revenue of $68.7 billion exceeding the consensus estimate of $67.2 billion. The outperformance was driven primarily by Azure and cloud services, which grew 38% in constant currency — the fastest growth rate in eight quarters.

The critical new disclosure: AI services within Azure contributed 12 percentage points to the segment's overall growth, implying an annualized AI revenue run rate of approximately $4.2 billion. This is up from 8 percentage points contribution in Q2 and 6 points in Q1.

CEO Satya Nadella framed the opportunity in expansive terms: "AI is the most significant platform shift since the cloud itself. We're seeing customers move from experimentation to production deployment at unprecedented speed."

## Segment Performance

| Segment | Revenue | Growth YoY |
|---|---|---|
| Intelligent Cloud | $28.4B | +23% |
| Productivity & Business | $22.1B | +13% |
| More Personal Computing | $18.2B | +9% |

### Intelligent Cloud
Azure growth of 38% beat the guided range of 34–35%. Management attributed the upside to:
- Large enterprise migrations accelerating as contracts signed in FY25 enter the deployment phase
- Azure OpenAI Service adoption across financial services, healthcare, and manufacturing verticals
- Growing adoption of Copilot Studio for custom AI agent development

### Productivity & Business
Office 365 commercial revenue grew 15%, driven by seat growth and higher ARPU from Copilot for Microsoft 365 subscriptions ($30/user/month). Microsoft disclosed that 800,000 organizations have now adopted Copilot, up from 400,000 last quarter.

### More Personal Computing
Windows OEM revenue was flat as the PC market showed no signs of a refresh cycle. Gaming revenue grew 4% on Xbox Game Pass subscriber growth, partially offset by lower console sales.

## Capital Expenditure Surge

Microsoft raised its FY26 capex guidance from $55 billion to $62 billion, reflecting accelerated data center construction to meet AI workload demand. CFO Amy Hood noted that the company has 40 data center projects under construction across 18 countries.

The capex increase initially concerned investors, with shares dipping 2% after-hours before recovering as analysts digested the revenue implications. At a 38% Azure growth rate, the incremental capex generates attractive returns within 3–4 years.

## Competitive Position

Microsoft's AI cloud momentum creates a significant challenge for Amazon Web Services, which reported 19% growth in its most recent quarter. Google Cloud grew 28% but from a much smaller base. Microsoft's advantage lies in its enterprise distribution — companies already embedded in the Microsoft ecosystem (Office, Teams, Dynamics) find it natural to adopt Azure and Copilot together.

The stock closed up 3.4% the day after earnings, adding $100 billion to Microsoft's market capitalization and bringing it to $3.8 trillion.`,
    status: 'published',
    language: 'en',
    article_type: 'earnings',
    category: sampleCategories[1], // Earnings
    tags: [sampleTags[0], sampleTags[6]], // AI, Quarterly Results
    tickers: [sampleCompanies[1], sampleCompanies[9]], // MSFT, AMZN
    sources: [
      { id: 'src-011a', source_name: 'Microsoft Q3 FY26 Earnings Release', source_url: 'https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/press-release-webcast', source_type: 'press_release', publisher: 'Microsoft Corporation', published_at: daysAgo(5, 17), accessed_at: daysAgo(5, 18), relevance_note: 'Official earnings data and segment breakdown', quote_used: null, is_primary_source: true },
      { id: 'src-011b', source_name: 'Microsoft 10-Q Filing', source_url: 'https://sec.gov/cgi-bin/browse-edgar?company=microsoft&CIK=&type=10-Q', source_type: 'company_filing', publisher: 'SEC EDGAR', published_at: daysAgo(5, 17), accessed_at: daysAgo(5, 19), relevance_note: 'Detailed financial statements and capex data', quote_used: null, is_primary_source: true },
      { id: 'src-011c', source_name: 'Microsoft Earnings Call Transcript', source_url: 'https://seekingalpha.com/article/microsoft-q3-fy26-call', source_type: 'news_article', publisher: 'Seeking Alpha', published_at: daysAgo(5, 18), accessed_at: daysAgo(5, 19), relevance_note: 'Nadella and Hood quotes', quote_used: 'AI is the most significant platform shift since the cloud itself.', is_primary_source: false },
    ],
    author: authorRahul,
    published_at: daysAgo(5, 18),
    scheduled_at: null,
    created_at: daysAgo(5, 16),
    updated_at: daysAgo(5, 20),
    reading_time_minutes: 7,
    featured_image: makeFeatured('microsoft-q3-earnings', 'Microsoft campus with Azure cloud branding', 'Microsoft\'s Azure AI services now generate a $4.2 billion quarterly run rate', 'Microsoft Corporation'),
    seo_title: 'Microsoft Q3 FY26 Earnings: Azure Grows 38%, AI at $4.2B Run Rate | CapitalColumn',
    seo_description: 'Microsoft Q3 FY26 revenue $68.7B beats estimates. Azure grows 38% with AI contributing 12pp. Capex guidance raised to $62B. Copilot adoption doubles.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'earnings-analyzer-v3',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.95,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Microsoft Q3 FY26 revenue of $68.7B beats consensus by $1.5B; Azure grows 38%.',
      'AI services contribute 12pp to Azure growth, implying ~$4.2B quarterly run rate.',
      'Copilot adopted by 800K organizations, doubling in one quarter.',
      'FY26 capex guidance raised from $55B to $62B for data center expansion.',
      'Stock gains 3.4%, adding $100B in market cap to reach $3.8 trillion.',
    ],
  },

  // ── 12. RBI Policy ──
  {
    id: 'art-012',
    external_id: null,
    slug: 'rbi-holds-repo-rate-june-2026-mpc-decision',
    title: 'RBI Holds Repo Rate at 6% in June MPC Meeting, Signals One More Cut in August',
    dek: 'The central bank pauses after back-to-back cuts, citing global uncertainty and the need to assess transmission of previous easing.',
    summary: 'The RBI Monetary Policy Committee voted 4-2 to hold the repo rate at 6.00% in its June 2026 meeting, after cutting rates by a cumulative 50 basis points since February. Governor Malhotra signaled the possibility of one more 25 bps cut in August if inflation remains within the 4% target.',
    body_markdown: `## The Decision

The Reserve Bank of India's six-member Monetary Policy Committee (MPC) voted 4-2 to keep the benchmark repo rate unchanged at 6.00% at its June 4–6, 2026 meeting. Two external members — Ashima Goyal and Jayanth Varma — voted for a 25 basis point cut to 5.75%.

The decision was widely expected. A Reuters poll of 45 economists showed 38 predicting a hold, with the remaining 7 expecting a cut. The RBI had cut rates twice in succession — 25 bps in February and 25 bps in April — bringing the repo rate down from 6.50% to 6.00%.

## Why the Pause?

Governor Sanjay Malhotra outlined three reasons for the pause:

1. **Transmission assessment:** The RBI wants to evaluate how effectively the previous 50 bps of cuts have transmitted to lending rates. Data shows that weighted average lending rates on fresh loans have declined only 22 bps, indicating incomplete pass-through by banks.

2. **Global uncertainty:** The US Federal Reserve has signaled a "higher for longer" stance, with the fed funds rate at 4.75–5.00%. Cutting too aggressively could widen the India-US rate differential and put pressure on the rupee.

3. **Food inflation volatility:** While headline CPI inflation stood at 3.8% in May, food inflation remains sticky at 5.2%, driven by vegetable and pulse prices. The RBI wants to see food inflation moderate before easing further.

## Growth-Inflation Balance

The RBI revised its FY27 GDP growth projection marginally higher to 6.7% from 6.5%, citing stronger-than-expected Q4 FY26 growth data. The inflation projection was maintained at 4.0% for FY27.

| Forecast | Previous | Revised |
|---|---|---|
| FY27 GDP Growth | 6.5% | 6.7% |
| Q1 FY27 CPI | 3.8% | 3.6% |
| Q2 FY27 CPI | 4.2% | 4.0% |
| FY27 Average CPI | 4.0% | 4.0% |

## Forward Guidance

Malhotra's most significant signal came during the press conference: "The MPC remains accommodative in its stance and will evaluate the evolving inflation-growth dynamics in August. If the monsoon progresses normally and food prices moderate as expected, there is room for further calibrated action."

Market participants interpreted this as a clear signal of a 25 bps cut in August, bringing the repo rate to 5.75% — the lowest since the pandemic era.

## Market Reaction

Bond markets rallied on the dovish forward guidance. The 10-year government bond yield fell 6 basis points to 6.38%, the lowest since March 2022. The BSE Sensex gained 286 points, led by interest rate-sensitive banking and real estate stocks.

HDFC Bank (+1.8%), SBI (+2.1%), and DLF (+3.4%) were among the top gainers. The Nifty Realty index outperformed, rising 2.9%.

## What to Watch

The August MPC meeting (August 5–7, 2026) will be the key event. Market consensus has shifted toward a terminal repo rate of 5.50% by March 2027, implying two more 25 bps cuts from the current level.

Key data points to watch include June and July CPI prints, the progress of the monsoon (critical for food prices), and the Fed's July 29–30 FOMC decision.`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[7], // Policy & Regulation
    tags: [sampleTags[3], sampleTags[4]], // Interest Rates, Inflation
    tickers: [sampleCompanies[5]], // HDFCBANK
    sources: [
      { id: 'src-012a', source_name: 'RBI Monetary Policy Statement June 2026', source_url: 'https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx', source_type: 'official_statement', publisher: 'Reserve Bank of India', published_at: daysAgo(5, 11), accessed_at: daysAgo(5, 12), relevance_note: 'Official MPC decision and policy statement', quote_used: null, is_primary_source: true },
      { id: 'src-012b', source_name: 'RBI Governor Press Conference Transcript', source_url: 'https://rbi.org.in/Scripts/Pressconference.aspx', source_type: 'official_statement', publisher: 'Reserve Bank of India', published_at: daysAgo(5, 12), accessed_at: daysAgo(5, 13), relevance_note: 'Governor Malhotra forward guidance quotes', quote_used: 'If the monsoon progresses normally and food prices moderate as expected, there is room for further calibrated action.', is_primary_source: true },
    ],
    author: authorPriya,
    published_at: daysAgo(5, 12),
    scheduled_at: null,
    created_at: daysAgo(5, 11),
    updated_at: daysAgo(5, 14),
    reading_time_minutes: 6,
    featured_image: makeFeatured('rbi-june-mpc', 'RBI headquarters in Mumbai with Indian flag', 'RBI holds repo rate at 6% in June MPC, signals August cut', 'Reserve Bank of India'),
    seo_title: 'RBI MPC June 2026: Repo Rate Held at 6%, August Cut Signaled | CapitalColumn',
    seo_description: 'RBI MPC votes 4-2 to hold repo rate at 6.00% in June 2026. Governor signals 25 bps cut in August. GDP forecast raised to 6.7%. Bond yields drop.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: false,
    is_editor_reviewed: true,
    ai_pipeline_name: null,
    ai_model_name: null,
    confidence_score: null,
    fact_check_status: 'human_checked',
    correction_note: 'Earlier version stated the vote was 5-1. Corrected to 4-2 after RBI published individual member votes.',
    last_corrected_at: daysAgo(5, 15),
    key_takeaways: [
      'RBI MPC votes 4-2 to hold repo rate at 6.00% after two consecutive 25 bps cuts.',
      'Governor Malhotra signals "room for further calibrated action" in August if food inflation moderates.',
      'GDP growth forecast raised to 6.7%; inflation projection maintained at 4.0% for FY27.',
      '10-year bond yield falls to 6.38%, lowest since March 2022; banking stocks rally.',
      'Market consensus expects terminal repo rate of 5.50% by March 2027.',
    ],
  },

  // ── 13. Bonus article — Global / Semiconductor ──
  {
    id: 'art-013',
    external_id: null,
    slug: 'tsmc-arizona-fab-begins-volume-production-us-chips-act',
    title: 'TSMC Arizona Fab Begins Volume Production of 4nm Chips, Marking US Semiconductor Manufacturing Milestone',
    dek: 'The $40 billion Arizona facility produces its first commercial wafers for Apple and AMD, easing geopolitical supply concerns.',
    summary: 'TSMC\'s first Arizona fabrication facility has achieved volume production of 4nm chips, delivering commercial wafers to customers including Apple and AMD. The milestone represents the first advanced-node semiconductor manufacturing on US soil and a key deliverable under the $52 billion CHIPS Act.',
    body_markdown: `## Volume Production Achieved

Taiwan Semiconductor Manufacturing Company confirmed on Monday that its Fab 21 facility in Phoenix, Arizona has achieved volume production on its N4P (4-nanometer) process technology. The first commercial wafers have been shipped to lead customers Apple Inc. and Advanced Micro Devices.

TSMC Chairman C.C. Wei described the achievement as "a historic moment for the global semiconductor industry" during a media briefing at the facility. The fab is currently running at approximately 60% of its 20,000 wafers-per-month nameplate capacity, with full utilization expected by Q4 2026.

## CHIPS Act Milestone

The volume production milestone triggers the second tranche of TSMC's federal funding under the CHIPS and Science Act. The company has received commitments totaling $6.6 billion in direct subsidies and $5 billion in low-interest loans. With the first tranche of $2.2 billion already disbursed, Monday's milestone unlocks an additional $2 billion.

Commerce Secretary Gina Raimondo called the achievement "exactly what the CHIPS Act was designed to deliver — advanced semiconductor manufacturing returning to American soil."

## Fab 21 Specifications

| Parameter | Details |
|---|---|
| Location | Phoenix, Arizona |
| Process Node | N4P (4nm) |
| Capacity | 20,000 WPM |
| Investment | $12 billion (Phase 1) |
| Employees | 4,500+ |
| Lead Customers | Apple, AMD |
| Full Utilization Target | Q4 2026 |

## What This Means for Supply Chain Resilience

The Arizona fab addresses a critical geopolitical vulnerability. Prior to Fab 21, 100% of the world's most advanced chips (sub-7nm) were manufactured in Taiwan, a region subject to increasing cross-strait tensions. With Arizona production, Apple and AMD can source a portion of their most advanced chips from US soil.

However, industry analysts caution that Fab 21's capacity represents less than 5% of TSMC's total advanced-node output. The bulk of production — including NVIDIA's AI GPUs — will continue to come from Taiwan's Fab 18 complex in Tainan.

## Phase 2 and Beyond

TSMC's Arizona investment extends beyond the current facility:

- **Phase 2 (under construction):** A second fab targeting N3E (3nm) process, expected to begin production in late 2027, with $15 billion investment
- **Phase 3 (announced):** An N2 (2nm) fab with $13 billion investment, targeting 2029 production start
- **Total Arizona investment:** $40 billion across three phases

The three-phase buildout would make Arizona TSMC's largest manufacturing site outside Taiwan, though still smaller than its Tainan Science Park complex.

## Industry Implications

Intel, which is building its own advanced fabs in Ohio and Germany under the IDM 2.0 strategy, faces increased competitive pressure. TSMC's Arizona fab demonstrates that the Taiwanese company can replicate its manufacturing excellence outside Taiwan, potentially undermining Intel's pitch to western governments about the need for domestic fab alternatives.

Samsung's planned Taylor, Texas fab (targeting 4nm production in 2025) has faced delays and is now expected to begin volume production in mid-2026, putting it behind TSMC's Arizona timeline.

TSMC shares rose 2.1% in Taipei trading following the announcement.`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[9], // Global Markets
    tags: [sampleTags[2]], // Semiconductors
    tickers: [sampleCompanies[0], sampleCompanies[2]], // AAPL, NVDA
    sources: [
      { id: 'src-013a', source_name: 'TSMC Press Release', source_url: 'https://pr.tsmc.com/english/news', source_type: 'press_release', publisher: 'TSMC', published_at: daysAgo(6, 8), accessed_at: daysAgo(6, 10), relevance_note: 'Official volume production announcement', quote_used: null, is_primary_source: true },
      { id: 'src-013b', source_name: 'US Department of Commerce Statement', source_url: 'https://www.commerce.gov/news/press-releases', source_type: 'official_statement', publisher: 'US Department of Commerce', published_at: daysAgo(6, 10), accessed_at: daysAgo(6, 11), relevance_note: 'CHIPS Act funding tranche confirmation', quote_used: 'Exactly what the CHIPS Act was designed to deliver.', is_primary_source: true },
    ],
    author: authorRahul,
    published_at: daysAgo(6, 10),
    scheduled_at: null,
    created_at: daysAgo(6, 7),
    updated_at: daysAgo(6, 12),
    reading_time_minutes: 6,
    featured_image: makeFeatured('tsmc-arizona-fab', 'TSMC Fab 21 facility exterior in Phoenix, Arizona', 'TSMC\'s Fab 21 in Arizona achieves volume production on 4nm process', 'TSMC'),
    seo_title: 'TSMC Arizona Fab Begins 4nm Volume Production: CHIPS Act Milestone | CapitalColumn',
    seo_description: 'TSMC Fab 21 in Arizona achieves volume production of 4nm chips for Apple and AMD. CHIPS Act funding unlocked. Three-phase $40B investment details.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'breaking-news-v2',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.94,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'TSMC Arizona Fab 21 achieves volume production of 4nm chips for Apple and AMD.',
      'Milestone unlocks $2 billion in additional CHIPS Act funding for TSMC.',
      'Fab running at 60% capacity; full utilization expected by Q4 2026.',
      'Three-phase Arizona investment totals $40 billion, including upcoming 3nm and 2nm fabs.',
      'Intel and Samsung face increased competitive pressure from TSMC\'s US manufacturing success.',
    ],
  },

  // ── 14. Bonus — Healthcare / Pharma ──
  {
    id: 'art-014',
    external_id: null,
    slug: 'sun-pharma-usfda-approval-cancer-drug-tildrakizumab',
    title: 'Sun Pharma Gets USFDA Breakthrough Therapy Designation for Novel Oncology Compound SUN-247',
    dek: 'India's largest pharma company moves closer to blockbuster status with a promising immuno-oncology pipeline candidate.',
    summary: 'Sun Pharmaceutical Industries received Breakthrough Therapy Designation from the US FDA for SUN-247, a novel bispecific antibody targeting PD-L1 and VEGF in advanced non-small cell lung cancer. The designation accelerates the regulatory pathway and positions Sun Pharma for a potential $2 billion peak sales opportunity.',
    body_markdown: `## The Breakthrough Designation

Sun Pharmaceutical Industries announced that the US Food and Drug Administration has granted Breakthrough Therapy Designation (BTD) to SUN-247, its internally developed bispecific antibody, for the treatment of advanced non-small cell lung cancer (NSCLC) in patients who have progressed on prior checkpoint inhibitor therapy.

BTD is reserved for drugs that show substantial improvement over existing therapies for serious conditions. It provides several advantages:

- Intensive FDA guidance on drug development
- Eligibility for priority review and accelerated approval
- Rolling review of the Biologics License Application (BLA)

## Clinical Data

The designation was based on results from the Phase 2 ILLUMINATE-Lung trial, which enrolled 187 patients with advanced NSCLC who had progressed on or after PD-1/PD-L1 inhibitor therapy:

- **Objective Response Rate (ORR):** 34.2% (vs. 12–15% for standard chemotherapy in this setting)
- **Median Progression-Free Survival:** 7.8 months (vs. 3.5 months for docetaxel)
- **Median Overall Survival:** 15.2 months (mature data pending)
- **Grade 3+ Adverse Events:** 22% (manageable safety profile)

The bispecific mechanism — simultaneously blocking PD-L1 and VEGF — addresses two key resistance pathways that limit the efficacy of current checkpoint inhibitors. This dual-targeting approach has been validated by encouraging data from similar molecules in development at Roche and Akeso.

## Commercial Opportunity

Analysts estimate a peak sales opportunity of $1.5–2.0 billion for SUN-247 if it achieves approval in NSCLC and subsequent label expansions. The global NSCLC second-line treatment market is valued at approximately $12 billion, and a 15% market share capture would align with historical precedent for breakthrough-designated oncology drugs.

Sun Pharma plans to commercialize SUN-247 independently in the US through its existing specialty oncology salesforce. For ex-US markets, the company is evaluating partnership models.

## Financial Impact

Sun Pharma's current revenue of $5.8 billion is primarily driven by its generics and specialty dermatology business. SUN-247 represents the company's first potential blockbuster in oncology and could transform its revenue mix toward higher-margin innovative products.

The company has invested approximately $450 million in SUN-247 development to date, with an estimated additional $300 million needed to complete Phase 3 trials and regulatory filings.

Sun Pharma shares rose 6.8% to ₹1,845 on the announcement, adding ₹32,000 crore to its market capitalization. The stock hit a new 52-week high.

ICICI Securities initiated coverage with a "Buy" rating and ₹2,100 target price, calling SUN-247 a "potential game-changer that re-rates Sun Pharma from a generics compounder to an innovation-driven pharma major."`,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: sampleCategories[8], // Healthcare
    tags: [sampleTags[7]], // Valuation
    tickers: [],
    sources: [
      { id: 'src-014a', source_name: 'Sun Pharma BSE Filing', source_url: 'https://www.bseindia.com/corporates/anndet_new.aspx', source_type: 'exchange_disclosure', publisher: 'BSE India', published_at: daysAgo(6, 9), accessed_at: daysAgo(6, 10), relevance_note: 'Official BTD announcement and clinical data summary', quote_used: null, is_primary_source: true },
      { id: 'src-014b', source_name: 'US FDA Breakthrough Therapy Database', source_url: 'https://www.fda.gov/patients/fast-track-breakthrough-therapy-accelerated-approval-priority-review', source_type: 'official_statement', publisher: 'US FDA', published_at: daysAgo(6, 9), accessed_at: daysAgo(6, 11), relevance_note: 'FDA confirmation of BTD grant', quote_used: null, is_primary_source: true },
    ],
    author: authorDesk,
    published_at: daysAgo(6, 10),
    scheduled_at: null,
    created_at: daysAgo(6, 8),
    updated_at: daysAgo(6, 12),
    reading_time_minutes: 6,
    featured_image: makeFeatured('sun-pharma-btd', 'Sun Pharma research laboratory with scientists working on antibody development', 'Sun Pharma receives FDA Breakthrough Therapy Designation for SUN-247', 'Sun Pharmaceutical Industries'),
    seo_title: 'Sun Pharma Gets FDA Breakthrough Therapy for Lung Cancer Drug SUN-247 | CapitalColumn',
    seo_description: 'Sun Pharma receives USFDA Breakthrough Therapy Designation for SUN-247 bispecific antibody in NSCLC. Phase 2 data shows 34% response rate.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'breaking-news-v2',
    ai_model_name: 'gpt-4.5-turbo',
    confidence_score: 0.91,
    fact_check_status: 'ai_checked',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Sun Pharma receives FDA Breakthrough Therapy Designation for SUN-247 in advanced NSCLC.',
      'Phase 2 data shows 34.2% response rate vs. 12–15% for standard chemotherapy.',
      'Peak sales estimated at $1.5–2.0 billion in a $12 billion addressable market.',
      'Stock rises 6.8% to a new 52-week high of ₹1,845.',
      'Approximately $750 million total investment needed through Phase 3 and regulatory approval.',
    ],
  },
];
