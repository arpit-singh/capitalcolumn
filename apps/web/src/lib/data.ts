import type { Article, Category, Tag, CompanyTicker, Source, Author, MediaAsset } from './types';

// ─── Mock Authors ─────────────────────────────────────────
const authors: Record<string, Author> = {
  editorial: {
    id: 'author-1',
    name: 'CapitalColumn Editorial Desk',
    slug: 'editorial-desk',
    bio: 'The CapitalColumn Editorial Desk combines AI-powered analysis with human editorial oversight to deliver accurate, timely financial news.',
    avatar_url: null,
    author_type: 'ai_assisted',
  },
  markets: {
    id: 'author-2',
    name: 'Markets Intelligence',
    slug: 'markets-intelligence',
    bio: 'AI-assisted market coverage with editorial review.',
    avatar_url: null,
    author_type: 'ai_assisted',
  },
};

// ─── Mock Categories ──────────────────────────────────────
export const categories: Category[] = [
  { id: 'cat-1', name: 'Markets', slug: 'markets', description: 'Market movements, indices, and trading insights covering Indian and global equity markets.', parent_id: null, sort_order: 1, is_active: true },
  { id: 'cat-2', name: 'Earnings', slug: 'earnings', description: 'Quarterly results, earnings surprises, and financial performance analysis of listed companies.', parent_id: null, sort_order: 2, is_active: true },
  { id: 'cat-3', name: 'Companies', slug: 'companies', description: 'In-depth company coverage, corporate actions, management changes, and strategic developments.', parent_id: null, sort_order: 3, is_active: true },
  { id: 'cat-4', name: 'Technology', slug: 'technology', description: 'Technology sector news, IT services, SaaS companies, and digital transformation in finance.', parent_id: null, sort_order: 4, is_active: true },
  { id: 'cat-5', name: 'Banking', slug: 'banking', description: 'Banking sector coverage including RBI policy, credit growth, NPA trends, and fintech developments.', parent_id: null, sort_order: 5, is_active: true },
  { id: 'cat-6', name: 'IPOs', slug: 'ipos', description: 'Initial public offerings, listing performance, and upcoming IPO analysis.', parent_id: null, sort_order: 6, is_active: true },
];

// ─── Mock Tags ────────────────────────────────────────────
export const tags: Tag[] = [
  { id: 'tag-1', name: 'Nifty 50', slug: 'nifty-50' },
  { id: 'tag-2', name: 'Sensex', slug: 'sensex' },
  { id: 'tag-3', name: 'Q4 Results', slug: 'q4-results' },
  { id: 'tag-4', name: 'RBI Policy', slug: 'rbi-policy' },
  { id: 'tag-5', name: 'FII Activity', slug: 'fii-activity' },
  { id: 'tag-6', name: 'AI & ML', slug: 'ai-ml' },
  { id: 'tag-7', name: 'Semiconductor', slug: 'semiconductor' },
  { id: 'tag-8', name: 'Electric Vehicles', slug: 'electric-vehicles' },
  { id: 'tag-9', name: 'IPO Watch', slug: 'ipo-watch' },
  { id: 'tag-10', name: 'Mergers & Acquisitions', slug: 'mergers-acquisitions' },
  { id: 'tag-11', name: 'Largecap', slug: 'largecap' },
  { id: 'tag-12', name: 'Midcap', slug: 'midcap' },
];

// ─── Mock Companies ───────────────────────────────────────
export const companies: CompanyTicker[] = [
  { id: 'co-1', name: 'Reliance Industries', ticker: 'RELIANCE', exchange: 'NSE', country: 'IN', sector: 'Energy', industry: 'Oil & Gas Refining', logo_url: null, company_page_slug: 'reliance' },
  { id: 'co-2', name: 'Tata Consultancy Services', ticker: 'TCS', exchange: 'NSE', country: 'IN', sector: 'Technology', industry: 'IT Services', logo_url: null, company_page_slug: 'tcs' },
  { id: 'co-3', name: 'HDFC Bank', ticker: 'HDFCBANK', exchange: 'NSE', country: 'IN', sector: 'Financials', industry: 'Private Banking', logo_url: null, company_page_slug: 'hdfcbank' },
  { id: 'co-4', name: 'Infosys', ticker: 'INFY', exchange: 'NSE', country: 'IN', sector: 'Technology', industry: 'IT Services', logo_url: null, company_page_slug: 'infy' },
  { id: 'co-5', name: 'Bharti Airtel', ticker: 'BHARTIARTL', exchange: 'NSE', country: 'IN', sector: 'Telecom', industry: 'Telecommunications', logo_url: null, company_page_slug: 'bhartiartl' },
  { id: 'co-6', name: 'ICICI Bank', ticker: 'ICICIBANK', exchange: 'NSE', country: 'IN', sector: 'Financials', industry: 'Private Banking', logo_url: null, company_page_slug: 'icicibank' },
  { id: 'co-7', name: 'Wipro', ticker: 'WIPRO', exchange: 'NSE', country: 'IN', sector: 'Technology', industry: 'IT Services', logo_url: null, company_page_slug: 'wipro' },
  { id: 'co-8', name: 'Tata Motors', ticker: 'TATAMOTORS', exchange: 'NSE', country: 'IN', sector: 'Automobiles', industry: 'Auto Manufacturing', logo_url: null, company_page_slug: 'tatamotors' },
];

// ─── Mock Sources ─────────────────────────────────────────
function makeSources(names: string[]): Source[] {
  return names.map((name, i) => ({
    id: `src-${i}`,
    source_name: name,
    source_url: `https://example.com/source/${i}`,
    source_type: i === 0 ? 'company_filing' as const : 'news_article' as const,
    publisher: name.split(' ')[0],
    published_at: new Date(Date.now() - i * 3600000).toISOString(),
    accessed_at: new Date().toISOString(),
    relevance_note: `Referenced for key data points in this article.`,
    quote_used: null,
    is_primary_source: i === 0,
  }));
}

// ─── Mock Featured Images ─────────────────────────────────
const imageMap: Record<number, { file: string; alt: string }> = {
  1: { file: '/images/articles/hero-markets.png', alt: 'Stock market trading floor showing green screens' },
  2: { file: '/images/articles/hero-corporate.png', alt: 'TCS corporate headquarters building' },
  3: { file: '/images/articles/hero-banking.png', alt: 'Reserve Bank of India headquarters' },
  4: { file: '/images/articles/hero-technology.png', alt: 'Cloud computing data center servers' },
  5: { file: '/images/articles/hero-earnings.png', alt: 'HDFC Bank branch exterior' },
  6: { file: '/images/articles/hero-ev.png', alt: 'Tata Nexon EV on road' },
  7: { file: '/images/articles/hero-corporate.png', alt: 'Modern bank building with glass facade' },
  8: { file: '/images/articles/hero-telecom.png', alt: '5G tower and telecommunications infrastructure' },
  9: { file: '/images/articles/hero-ipo.png', alt: 'Solar panel manufacturing facility' },
  10: { file: '/images/articles/hero-earnings.png', alt: 'Corporate board meeting room' },
  11: { file: '/images/articles/hero-digital-banking.png', alt: 'Digital banking on smartphone' },
};

function makeImage(id: number, alt: string): MediaAsset {
  const img = imageMap[id] || { file: '/images/articles/hero-markets.png', alt };
  return {
    id: `img-${id}`,
    public_url: img.file,
    alt_text: img.alt || alt,
    caption: alt,
    credit: 'CapitalColumn',
    width: 1200,
    height: 675,
  };
}

// ─── Helper: generate date offsets ────────────────────────
function hoursAgo(h: number): string {
  return new Date(Date.now() - h * 3600000).toISOString();
}

// ─── Mock Articles ────────────────────────────────────────
export const articles: Article[] = [
  {
    id: 'art-1',
    external_id: null,
    slug: 'nifty-50-hits-all-time-high-broad-based-rally',
    title: 'Nifty 50 Hits All-Time High as Broad-Based Rally Lifts Sentiment',
    dek: 'The benchmark index surged past 24,000 for the first time, driven by strong earnings and sustained foreign fund inflows.',
    summary: 'Indian equity markets hit record highs on Monday as the Nifty 50 crossed the 24,000 mark for the first time. Banking and IT heavyweights led the charge with HDFC Bank and TCS contributing the most points.',
    body_markdown: `Indian equity markets witnessed a historic session on Monday as the Nifty 50 index surged past the 24,000 mark for the first time, closing at 24,167 — a gain of 1.4% on the day.\n\n## What Drove the Rally\n\nThe advance was broad-based, with 42 of the 50 index constituents closing in the green. Banking stocks led the charge, with HDFC Bank rising 2.8% and ICICI Bank gaining 2.1%.\n\nForeign institutional investors (FIIs) were net buyers for the eighth consecutive session, pumping in ₹4,200 crore on Monday alone. Domestic institutional investors added another ₹1,800 crore.\n\n## Sector Performance\n\n- **Banking**: Nifty Bank rose 1.9%, with private banks outperforming PSU banks\n- **IT**: The Nifty IT index gained 1.5% on improved guidance from TCS and Infosys\n- **Auto**: Tata Motors surged 3.2% ahead of its quarterly results\n- **Energy**: Reliance Industries added 1.1%, contributing 45 points to the Nifty\n\n## Global Cues\n\nPositive global cues also supported sentiment, with the S&P 500 closing at a record high on Friday. Expectations of a Federal Reserve rate cut in September boosted risk appetite globally.\n\n> "The breadth of this rally is encouraging. Unlike previous highs that were driven by a handful of stocks, today's advance was supported across sectors," noted a senior market strategist.\n\n## What's Ahead\n\nMarket participants will closely watch the upcoming Q4 earnings season, with several Nifty heavyweights scheduled to report this week. The RBI monetary policy decision on June 6 is another key event on the horizon.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'market_update',
    category: categories[0],
    tags: [tags[0], tags[1], tags[4], tags[10]],
    tickers: [companies[2], companies[1], companies[5]],
    sources: makeSources(['NSE India', 'Bloomberg', 'SEBI FII Data']),
    author: authors.markets,
    published_at: hoursAgo(2),
    scheduled_at: null,
    created_at: hoursAgo(4),
    updated_at: hoursAgo(2),
    reading_time_minutes: 4,
    featured_image: makeImage(1, 'Stock market trading floor showing green screens'),
    seo_title: 'Nifty 50 Hits All-Time High — Broad Rally Analysis',
    seo_description: 'Nifty 50 crosses 24,000 for the first time as banking and IT stocks lead a broad-based rally. FIIs net buyers for 8th straight session.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'market-update-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.94,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Nifty 50 crossed 24,000 for the first time, closing at 24,167 (+1.4%)',
      'FIIs were net buyers for the 8th consecutive session with ₹4,200 crore inflow',
      '42 of 50 Nifty constituents closed in the green',
      'Banking and IT sectors led the rally; HDFC Bank rose 2.8%',
    ],
  },
  {
    id: 'art-2',
    external_id: null,
    slug: 'tcs-q4-results-beat-estimates-revenue-growth',
    title: 'TCS Q4 Results Beat Street Estimates; Revenue Grows 5.3% YoY',
    dek: 'India\'s largest IT services firm reported strong quarterly numbers with improved deal wins and margin expansion.',
    summary: 'Tata Consultancy Services reported Q4 FY26 revenue of ₹64,259 crore, beating analyst estimates. Operating margins improved 80 basis points to 26.4%.',
    body_markdown: `Tata Consultancy Services (TCS) reported its fourth-quarter results for FY2025-26, delivering a revenue growth of 5.3% year-on-year that surpassed consensus expectations.\n\n## Key Numbers\n\nThe company reported revenue of ₹64,259 crore for Q4 FY26, compared to ₹61,028 crore in the year-ago period. Net profit came in at ₹12,434 crore, up 8.1% from ₹11,501 crore.\n\nOperating profit margin (EBIT) expanded 80 basis points year-on-year to 26.4%, beating the Street estimate of 25.8%.\n\n## Deal Pipeline\n\nTCS reported total contract value (TCV) of $12.2 billion for the quarter, the highest in six quarters. Large deal TCV stood at $4.6 billion, reflecting strong demand in cloud transformation and AI-led initiatives.\n\n## Management Commentary\n\n"We are seeing a gradual improvement in the demand environment, particularly in North America and Europe. Our investments in AI and GenAI services are beginning to translate into meaningful revenue," said the CEO during the earnings call.\n\n## Sector Impact\n\nThe strong results are expected to set a positive tone for the broader IT sector. Infosys and Wipro, which report later this week, may benefit from the improved sentiment.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'earnings',
    category: categories[1],
    tags: [tags[2], tags[10]],
    tickers: [companies[1], companies[3], companies[6]],
    sources: makeSources(['BSE Filing', 'TCS Investor Relations', 'Moneycontrol']),
    author: authors.editorial,
    published_at: hoursAgo(5),
    scheduled_at: null,
    created_at: hoursAgo(7),
    updated_at: hoursAgo(5),
    reading_time_minutes: 5,
    featured_image: makeImage(2, 'TCS corporate headquarters building'),
    seo_title: 'TCS Q4 FY26 Results: Revenue Growth Beats Estimates',
    seo_description: 'TCS Q4 FY26 results: Revenue grows 5.3% YoY to ₹64,259 crore, beating estimates. Operating margins expand to 26.4%.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'earnings-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.96,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Q4 FY26 revenue at ₹64,259 crore — 5.3% YoY growth, beating estimates',
      'Operating margins expanded 80 bps to 26.4%',
      'TCV of $12.2 billion — highest in 6 quarters',
      'AI and GenAI services driving new deal wins',
    ],
  },
  {
    id: 'art-3',
    external_id: null,
    slug: 'rbi-holds-rates-steady-shifts-stance-neutral',
    title: 'RBI Holds Rates Steady, Shifts Stance to Neutral Amid Easing Inflation',
    dek: 'The central bank maintained the repo rate at 6.5% but signaled a potential pivot with its change in monetary policy stance.',
    summary: 'The Reserve Bank of India kept the repo rate unchanged at 6.5% for the eighth consecutive meeting but shifted its stance from "withdrawal of accommodation" to "neutral," opening the door for future rate cuts.',
    body_markdown: `The Reserve Bank of India (RBI) monetary policy committee voted unanimously to keep the benchmark repo rate at 6.5% in its June policy review, while shifting its stance to "neutral" — a significant signal that rate cuts may be on the horizon.\n\n## The Decision\n\nThe MPC voted 6-0 to hold rates, marking the eighth consecutive pause. However, the change in stance from "withdrawal of accommodation" to "neutral" was the key takeaway for markets.\n\n## Why It Matters\n\nA neutral stance means the RBI is no longer biased towards tightening and could move in either direction depending on incoming data. With CPI inflation moderating to 4.2% in May — well within the RBI's 4% target — conditions are aligning for a potential rate cut as early as August.\n\n## Growth Outlook\n\nThe RBI retained its GDP growth projection at 7.2% for FY27, citing robust domestic demand and improving export prospects. However, it flagged global uncertainties and crude oil volatility as downside risks.\n\n## Market Reaction\n\nBond yields fell sharply following the announcement, with the 10-year benchmark yield dropping 8 basis points to 6.88%. Bank stocks rallied, with the Nifty Bank index gaining 1.2%.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: categories[4],
    tags: [tags[3], tags[0]],
    tickers: [companies[2], companies[5]],
    sources: makeSources(['RBI Press Release', 'RBI MPC Statement', 'Reuters']),
    author: authors.editorial,
    published_at: hoursAgo(8),
    scheduled_at: null,
    created_at: hoursAgo(10),
    updated_at: hoursAgo(8),
    reading_time_minutes: 4,
    featured_image: makeImage(3, 'Reserve Bank of India headquarters'),
    seo_title: 'RBI Policy June 2026: Rates Held, Stance Shifts to Neutral',
    seo_description: 'RBI keeps repo rate at 6.5%, shifts stance to neutral. Inflation easing to 4.2% opens door for potential rate cuts.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'news-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.95,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Repo rate unchanged at 6.5% — 8th consecutive pause',
      'Stance shifted to "neutral" from "withdrawal of accommodation"',
      'CPI inflation at 4.2%, within RBI\'s comfort zone',
      'Bond yields fell 8 bps; Nifty Bank rallied 1.2%',
    ],
  },
  {
    id: 'art-4',
    external_id: null,
    slug: 'reliance-jio-ai-cloud-platform-launch',
    title: 'Reliance Jio Unveils AI-Powered Cloud Platform for Enterprise',
    dek: 'The telecom giant\'s new cloud offering targets Indian enterprises with sovereign AI capabilities and competitive pricing.',
    summary: 'Reliance Jio announced the launch of JioCloud AI, a sovereign cloud platform offering AI-as-a-service capabilities tailored for Indian enterprises, priced 40% below global cloud competitors.',
    body_markdown: `Reliance Jio has launched JioCloud AI, a sovereign cloud computing platform designed to serve Indian enterprises with artificial intelligence capabilities at competitive pricing.\n\n## The Platform\n\nJioCloud AI leverages Jio's network of 12 data centers across India to offer cloud compute, storage, and AI-as-a-service solutions. The platform supports major AI frameworks including PyTorch, TensorFlow, and Hugging Face models.\n\n## Pricing Strategy\n\nJio is positioning the platform at approximately 40% below comparable offerings from AWS, Azure, and Google Cloud for the Indian market. The company cited its infrastructure advantage and scale economics.\n\n## Enterprise Focus\n\nInitial partnerships include integrations with SAP, Salesforce, and Oracle for enterprise workloads. The platform also offers sector-specific AI solutions for banking, healthcare, and manufacturing.\n\n## Analyst Reaction\n\nAnalysts view the launch as a strategic move to capture India's growing cloud market, estimated at $15 billion by 2027. The sovereign AI angle could appeal to government and regulated sector customers.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: categories[3],
    tags: [tags[5], tags[10]],
    tickers: [companies[0]],
    sources: makeSources(['Jio Press Release', 'Economic Times', 'Gartner Research']),
    author: authors.editorial,
    published_at: hoursAgo(12),
    scheduled_at: null,
    created_at: hoursAgo(14),
    updated_at: hoursAgo(12),
    reading_time_minutes: 3,
    featured_image: makeImage(4, 'Cloud computing data center servers'),
    seo_title: 'Jio Launches AI-Powered Cloud Platform for Indian Enterprises',
    seo_description: 'Reliance Jio launches JioCloud AI, a sovereign cloud platform with AI services priced 40% below global competitors.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'news-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.92,
    fact_check_status: 'human_checked',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'JioCloud AI launched with 12 data centers across India',
      'Priced ~40% below AWS, Azure, and Google Cloud',
      'Supports major AI frameworks: PyTorch, TensorFlow, Hugging Face',
      'Targeting $15B Indian cloud market by 2027',
    ],
  },
  {
    id: 'art-5',
    external_id: null,
    slug: 'hdfc-bank-credit-growth-accelerates-q4',
    title: 'HDFC Bank Credit Growth Accelerates to 17.8% in Q4, Deposit Gap Narrows',
    dek: 'India\'s largest private lender showed improving deposit mobilization as the post-merger integration progresses.',
    summary: 'HDFC Bank reported credit growth of 17.8% YoY in Q4 FY26, with advances reaching ₹26.4 lakh crore. The critical credit-deposit ratio improved by 120 basis points.',
    body_markdown: `HDFC Bank, India's largest private sector lender by market cap, reported accelerating credit growth in Q4 FY26 as its post-merger integration with HDFC Ltd continues to bear fruit.\n\n## Credit Growth\n\nAdvances grew 17.8% year-on-year to ₹26.4 lakh crore, up from 15.2% growth in Q3. Retail loans and corporate credit both contributed to the acceleration.\n\n## Deposit Mobilization\n\nDeposits grew 19.1% YoY, outpacing credit growth for the first time since the merger. The credit-deposit ratio improved by 120 basis points sequentially to 104.2%.\n\n## Profitability\n\nNet interest income grew 12.4% to ₹30,800 crore. Net profit was ₹17,200 crore, up 22% YoY. Asset quality remained stable with gross NPA at 1.24%.\n\n## Merger Integration\n\nManagement indicated that 85% of the technology integration is complete, with full integration expected by September 2026.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'earnings',
    category: categories[1],
    tags: [tags[2], tags[10]],
    tickers: [companies[2]],
    sources: makeSources(['HDFC Bank BSE Filing', 'HDFC Bank Investor Presentation']),
    author: authors.editorial,
    published_at: hoursAgo(16),
    scheduled_at: null,
    created_at: hoursAgo(18),
    updated_at: hoursAgo(16),
    reading_time_minutes: 4,
    featured_image: makeImage(5, 'HDFC Bank branch exterior'),
    seo_title: 'HDFC Bank Q4 FY26: Credit Growth Hits 17.8%, Deposits Improve',
    seo_description: 'HDFC Bank Q4 FY26: Credit growth accelerates to 17.8% YoY, deposit mobilization outpaces advances for first time post-merger.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'earnings-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.95,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Credit growth accelerated to 17.8% YoY from 15.2% in Q3',
      'Deposits grew 19.1% — outpacing credit for first time since merger',
      'Net profit up 22% YoY to ₹17,200 crore',
      '85% of tech integration complete; full merger by Sept 2026',
    ],
  },
  {
    id: 'art-6',
    external_id: null,
    slug: 'tata-motors-ev-sales-surge-market-share-gains',
    title: 'Tata Motors EV Sales Surge 62% in May; Market Share Hits Record 73%',
    dek: 'The Nexon EV and Punch EV drove volumes as Tata consolidates its dominance in India\'s electric vehicle market.',
    summary: 'Tata Motors sold 12,800 electric vehicles in May 2026, a 62% increase YoY, commanding a record 73% share of India\'s passenger EV market.',
    body_markdown: `Tata Motors continued its electric vehicle dominance in May 2026, selling 12,800 units — a 62% surge from the year-ago period — and capturing a record 73% share of India's passenger EV market.\n\n## Volume Breakdown\n\nThe Nexon EV remained the top seller with 5,400 units, followed by the Punch EV at 4,200 units. The Tiago EV contributed 2,100 units while the Harrier EV added 1,100 units in its first full month.\n\n## Market Dynamics\n\nOverall passenger EV sales in India grew 38% in May, with total industry volume at 17,500 units. Tata's 73% share is up from 68% a year ago, despite new entries from Hyundai and Mahindra.\n\n## Infrastructure Push\n\nTata also announced it has crossed 5,000 fast chargers across India through its Tata Power subsidiary, with plans to reach 10,000 by March 2027.\n\n## Outlook\n\nWith the Curvv EV launch planned for Q3, analysts expect Tata's EV sales run rate to exceed 15,000 units per month by end of FY27.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: categories[2],
    tags: [tags[7], tags[11]],
    tickers: [companies[7]],
    sources: makeSources(['FADA Sales Data', 'Tata Motors Press Release', 'SIAM Monthly Report']),
    author: authors.editorial,
    published_at: hoursAgo(20),
    scheduled_at: null,
    created_at: hoursAgo(22),
    updated_at: hoursAgo(20),
    reading_time_minutes: 3,
    featured_image: makeImage(6, 'Tata Nexon EV on road'),
    seo_title: 'Tata Motors EV Sales May 2026: 62% Surge, 73% Market Share',
    seo_description: 'Tata Motors EV sales surge 62% in May 2026. Nexon EV and Punch EV lead as Tata captures record 73% passenger EV market share.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'news-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.93,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'May EV sales: 12,800 units — 62% YoY growth',
      'Market share hit record 73% of passenger EV segment',
      'Nexon EV led with 5,400 units, Punch EV sold 4,200',
      'Tata Power crossed 5,000 fast chargers nationwide',
    ],
  },
  {
    id: 'art-7',
    external_id: null,
    slug: 'infosys-wins-2-billion-deal-european-bank',
    title: 'Infosys Bags $2 Billion Deal from Major European Bank',
    dek: 'The multi-year engagement covers cloud migration, cybersecurity, and AI-driven analytics for one of Europe\'s top 10 banks.',
    summary: 'Infosys announced its largest-ever deal win — a $2 billion, 7-year engagement with a leading European bank covering cloud transformation and AI analytics.',
    body_markdown: `Infosys has secured a landmark $2 billion deal from a top-10 European bank, marking the largest single contract in the company's history. The seven-year engagement covers end-to-end digital transformation.\n\n## Deal Scope\n\nThe engagement spans cloud migration of core banking systems, implementation of AI-driven analytics for risk management, cybersecurity modernization, and digital customer experience platforms.\n\n## Strategic Significance\n\nThe deal validates Infosys's push into large transformational engagements and its AI capabilities. The company has been investing heavily in generative AI tools and platforms.\n\n## Financial Impact\n\nAt $2 billion over 7 years, the deal implies an annual revenue run rate of approximately $285 million, which would represent about 1.5% of Infosys's current annual revenue.\n\n## Stock Reaction\n\nInfosys shares rose 4.2% following the announcement, touching a 52-week high of ₹1,892.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: categories[3],
    tags: [tags[5], tags[9], tags[10]],
    tickers: [companies[3]],
    sources: makeSources(['BSE Corporate Filing', 'Infosys Press Release']),
    author: authors.editorial,
    published_at: hoursAgo(24),
    scheduled_at: null,
    created_at: hoursAgo(26),
    updated_at: hoursAgo(24),
    reading_time_minutes: 3,
    featured_image: makeImage(7, 'Modern bank building with glass facade'),
    seo_title: 'Infosys Secures Record $2B Deal from European Bank',
    seo_description: 'Infosys wins its largest-ever deal: $2 billion, 7-year engagement with a top European bank for cloud, AI, and cybersecurity transformation.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'news-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.94,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Largest deal in Infosys history: $2B over 7 years',
      'Covers cloud, AI analytics, cybersecurity, and digital CX',
      'Implies ~$285M annual revenue run rate',
      'Infosys shares hit 52-week high at ₹1,892',
    ],
  },
  {
    id: 'art-8',
    external_id: null,
    slug: 'airtel-5g-subscriber-base-crosses-100-million',
    title: 'Bharti Airtel\'s 5G Subscriber Base Crosses 100 Million Milestone',
    dek: 'The telecom operator is now monetizing its 5G network with ARPU uplift visible in premium subscriber segments.',
    summary: 'Bharti Airtel announced that its 5G subscriber base has crossed 100 million, with the company reporting meaningful ARPU improvement in 5G-enabled circles.',
    body_markdown: `Bharti Airtel has crossed the 100-million mark for 5G subscribers, becoming the first private telecom operator in India to achieve this milestone.\n\n## The Numbers\n\n5G subscribers reached 102 million as of end-May 2026, up from 75 million at the end of December 2025. The company's 5G network now covers 5,000+ cities and towns.\n\n## ARPU Impact\n\nCrucially, Airtel reported that 5G users have an average revenue per user (ARPU) of ₹265, compared to ₹198 for its overall subscriber base — a 34% premium.\n\n## Network Investment\n\nAirtel has invested ₹42,000 crore in its 5G rollout since the spectrum auction, with the network running on a standalone architecture in metro circles.\n\n## Competitive Landscape\n\nJio leads in absolute 5G subscribers with an estimated 180 million users, but Airtel's higher ARPU reflects its premium positioning strategy.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: categories[3],
    tags: [tags[10]],
    tickers: [companies[4]],
    sources: makeSources(['Airtel Investor Update', 'TRAI Data', 'Airtel Press Release']),
    author: authors.markets,
    published_at: hoursAgo(28),
    scheduled_at: null,
    created_at: hoursAgo(30),
    updated_at: hoursAgo(28),
    reading_time_minutes: 3,
    featured_image: makeImage(8, '5G tower and telecommunications infrastructure'),
    seo_title: 'Airtel 5G Subscribers Cross 100M — ARPU Premium Visible',
    seo_description: 'Bharti Airtel crosses 100 million 5G subscribers. 5G ARPU at ₹265 vs ₹198 overall — 34% premium drives monetization.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: false,
    ai_pipeline_name: 'news-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.91,
    fact_check_status: 'ai_checked',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      '5G subscribers crossed 102 million milestone',
      '5G ARPU at ₹265 — 34% premium over overall ARPU',
      '₹42,000 crore invested in 5G rollout',
      'Coverage spans 5,000+ cities and towns',
    ],
  },
  {
    id: 'art-9',
    external_id: null,
    slug: 'premier-energies-ipo-oversubscribed-42-times',
    title: 'Premier Energies IPO Oversubscribed 42 Times; Grey Market Premium Soars',
    dek: 'The solar cell manufacturer\'s IPO attracted massive retail and institutional demand amid India\'s renewable energy push.',
    summary: 'Premier Energies\' IPO received bids worth ₹1.2 lakh crore, with the issue oversubscribed 42 times on the final day. QIB portion was subscribed 68 times.',
    body_markdown: `Premier Energies, one of India's largest integrated solar cell and module manufacturers, saw its initial public offering oversubscribed 42 times on the final day of bidding.\n\n## Subscription Details\n\nThe IPO received total bids of ₹1.2 lakh crore against an issue size of ₹2,830 crore:\n- **QIB**: 68.2x subscribed\n- **NII (HNI)**: 52.4x subscribed\n- **Retail**: 18.7x subscribed\n\n## Company Profile\n\nPremier Energies is India's second-largest integrated solar cell and module manufacturer with a capacity of 4 GW. The company plans to use IPO proceeds for capacity expansion to 8 GW.\n\n## Grey Market Sentiment\n\nThe grey market premium (GMP) surged to ₹180 over the issue price of ₹450, indicating expected listing gains of approximately 40%.\n\n## Sector Tailwinds\n\nIndia's solar manufacturing sector is benefiting from the PLI scheme and increasing emphasis on energy security and domestic manufacturing.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: categories[5],
    tags: [tags[8]],
    tickers: [],
    sources: makeSources(['BSE IPO Data', 'Premier Energies DRHP', 'SEBI Filing']),
    author: authors.editorial,
    published_at: hoursAgo(32),
    scheduled_at: null,
    created_at: hoursAgo(34),
    updated_at: hoursAgo(32),
    reading_time_minutes: 3,
    featured_image: makeImage(9, 'Solar panel manufacturing facility'),
    seo_title: 'Premier Energies IPO: 42x Oversubscribed — Full Breakdown',
    seo_description: 'Premier Energies IPO oversubscribed 42 times with ₹1.2 lakh crore in bids. QIBs at 68x, grey market premium at 40%.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'ipo-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.94,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'IPO oversubscribed 42x with ₹1.2 lakh crore in total bids',
      'QIB portion subscribed 68.2 times',
      'Grey market premium at ₹180 (40% over issue price)',
      'Proceeds to fund capacity expansion from 4 GW to 8 GW',
    ],
  },
  {
    id: 'art-10',
    external_id: null,
    slug: 'wipro-announces-stock-buyback-12000-crore',
    title: 'Wipro Board Approves ₹12,000 Crore Buyback at 25% Premium',
    dek: 'The IT major announced its fourth buyback in five years, offering a 25% premium to current market price.',
    summary: 'Wipro\'s board approved a ₹12,000 crore share buyback at ₹580 per share, representing a 25% premium to the current market price of ₹464.',
    body_markdown: `Wipro Limited announced a share buyback worth ₹12,000 crore at a price of ₹580 per share through the tender offer route.\n\n## Buyback Details\n\nThe buyback price of ₹580 represents a 25% premium to the current market price of approximately ₹464. The company will buy back up to 20.7 crore shares, representing about 3.9% of the total equity.\n\n## Capital Return Track Record\n\nThis is Wipro's fourth buyback in five years. Including dividends, the company has returned over ₹45,000 crore to shareholders since FY22.\n\n## Market Reaction\n\nWipro shares surged 5.8% following the announcement, closing at ₹491. Analysts noted the buyback signals management confidence in the company's cash flow generation.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'news',
    category: categories[2],
    tags: [tags[10]],
    tickers: [companies[6]],
    sources: makeSources(['BSE Filing', 'Wipro Investor Relations']),
    author: authors.editorial,
    published_at: hoursAgo(36),
    scheduled_at: null,
    created_at: hoursAgo(38),
    updated_at: hoursAgo(36),
    reading_time_minutes: 3,
    featured_image: makeImage(10, 'Corporate board meeting room'),
    seo_title: 'Wipro ₹12,000 Crore Buyback: Price, Premium, Timeline',
    seo_description: 'Wipro announces ₹12,000 crore share buyback at ₹580/share — 25% premium to current price. Fourth buyback in five years.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'news-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.95,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Buyback at ₹580/share — 25% premium to market price',
      '₹12,000 crore total outlay covering ~3.9% of equity',
      'Fourth buyback in five years',
      'Over ₹45,000 crore returned to shareholders since FY22',
    ],
  },
  {
    id: 'art-11',
    external_id: null,
    slug: 'icici-bank-digital-transactions-record-high',
    title: 'ICICI Bank Digital Transactions Hit Record ₹18 Lakh Crore in FY26',
    dek: 'Digital channels now account for 94% of all transactions as the bank\'s technology investments pay off.',
    summary: 'ICICI Bank reported record digital transaction volumes of ₹18 lakh crore in FY26, with digital channels accounting for 94% of all transactions.',
    body_markdown: `ICICI Bank reported a record year for digital banking, with total digital transaction value reaching ₹18 lakh crore in FY26 — a 35% increase from the previous year.\n\n## Digital Penetration\n\nDigital channels accounted for 94% of all savings account transactions, up from 89% in FY25. The iMobile Pay app crossed 65 million monthly active users.\n\n## Technology Investments\n\nThe bank invested ₹3,200 crore in technology during FY26, focusing on AI-driven fraud detection, personalized banking experiences, and cloud-native core banking modules.\n\n## Business Impact\n\nDigital channels drove 78% of new personal loan originations, 65% of credit card applications, and 82% of fixed deposit bookings. The cost-to-income ratio improved by 150 basis points.`,
    body_html: undefined,
    status: 'published',
    language: 'en',
    article_type: 'analysis',
    category: categories[4],
    tags: [tags[5], tags[10]],
    tickers: [companies[5]],
    sources: makeSources(['ICICI Bank Annual Report FY26', 'ICICI Bank Investor Day Presentation']),
    author: authors.editorial,
    published_at: hoursAgo(40),
    scheduled_at: null,
    created_at: hoursAgo(42),
    updated_at: hoursAgo(40),
    reading_time_minutes: 3,
    featured_image: makeImage(11, 'Digital banking on smartphone'),
    seo_title: 'ICICI Bank FY26: Digital Transactions Hit ₹18L Crore Record',
    seo_description: 'ICICI Bank digital transactions reach ₹18 lakh crore in FY26, up 35% YoY. 94% of transactions now digital.',
    canonical_url: null,
    noindex: false,
    is_ai_generated: true,
    is_editor_reviewed: true,
    ai_pipeline_name: 'analysis-v2',
    ai_model_name: 'gpt-4o',
    confidence_score: 0.93,
    fact_check_status: 'source_verified',
    correction_note: null,
    last_corrected_at: null,
    key_takeaways: [
      'Digital transactions: ₹18 lakh crore — up 35% YoY',
      '94% of savings account transactions are now digital',
      'iMobile Pay crossed 65M monthly active users',
      'Tech investment of ₹3,200 crore in FY26',
    ],
  },
];

// ═══════════════════════════════════════════════════════════
// Live API Access Functions
// ═══════════════════════════════════════════════════════════

// Fallback to the production API if no env var is set
const API_URL = import.meta.env.API_BASE_URL || process.env.API_BASE_URL || 'http://api.capitalcolumn.in';

/**
 * Generic fetch wrapper for API calls
 */
async function fetchAPI(endpoint: string, params: Record<string, string> = {}) {
  try {
    const url = new URL(`${API_URL}${endpoint}`);
    Object.entries(params).forEach(([k, v]) => {
      if (v) url.searchParams.append(k, v);
    });
    
    const res = await fetch(url.toString(), {
      // Small timeout to prevent hanging forever
      signal: AbortSignal.timeout(5000),
      headers: {
        'Accept': 'application/json'
      }
    });

    if (!res.ok) {
      if (res.status === 404) return null;
      console.error(`API Error: ${res.status} ${res.statusText} fetching ${endpoint}`);
      return null;
    }

    return await res.json();
  } catch (error) {
    console.error(`Failed to fetch ${endpoint}:`, error);
    return null;
  }
}

/** Get published articles with optional filters */
export async function getArticles(filters: { limit?: number, category?: string, tag?: string, ticker?: string } = {}): Promise<Article[]> {
  const params: Record<string, string> = { limit: (filters.limit || 50).toString() };
  if (filters.category) params.category = filters.category;
  if (filters.tag) params.tag = filters.tag;
  if (filters.ticker) params.ticker = filters.ticker;

  const data = await fetchAPI('/public/articles', params);
  return data?.items || [];
}

/** Get a single article by slug */
export async function getArticleBySlug(slug: string): Promise<Article | undefined> {
  const data = await fetchAPI(`/public/articles/${slug}`);
  return data || undefined;
}

/** Get all active categories */
export async function getCategories(): Promise<Category[]> {
  const data = await fetchAPI('/public/categories');
  return data || [];
}

/** Get a category by slug */
export async function getCategoryBySlug(slug: string): Promise<Category | undefined> {
  const data = await fetchAPI(`/public/categories/${slug}`);
  return data || undefined;
}

/** Get all tags */
export async function getTags(): Promise<Tag[]> {
  const data = await fetchAPI('/public/tags');
  return data || [];
}

/** Get a tag by slug */
export async function getTagBySlug(slug: string): Promise<Tag | undefined> {
  const tags = await getTags();
  return tags.find((t) => t.slug === slug);
}

/** Get company/ticker page data */
export async function getCompanyData(ticker: string): Promise<{ company: CompanyTicker, articles: Article[] } | undefined> {
  const data = await fetchAPI(`/public/tickers/${ticker}`);
  if (data) {
    return {
      company: data.company,
      articles: data.articles?.items || []
    };
  }
  return undefined;
}

/** Get related articles */
export async function getRelatedArticles(article: Article, max: number = 3): Promise<Article[]> {
  if (!article.category?.slug) return [];
  const articles = await getArticles({ category: article.category.slug, limit: max + 1 });
  return articles.filter(a => a.id !== article.id).slice(0, max);
}

/** Search articles */
export async function searchArticles(query: string, categorySlug?: string): Promise<Article[]> {
  const params: Record<string, string> = { search: query, limit: '20' };
  if (categorySlug) params.category = categorySlug;
  const data = await fetchAPI('/public/articles', params);
  return data?.items || [];
}
