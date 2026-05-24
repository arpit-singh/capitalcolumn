export interface Article {
  id: string;
  external_id: string | null;
  slug: string;
  title: string;
  dek: string;
  summary: string;
  body_markdown: string;
  body_html?: string;
  status: 'draft' | 'in_review' | 'scheduled' | 'published' | 'archived' | 'rejected';
  language: string;
  article_type: 'news' | 'analysis' | 'explainer' | 'earnings' | 'market_update' | 'alert' | 'opinion';
  category: Category;
  tags: Tag[];
  tickers: CompanyTicker[];
  sources: Source[];
  author: Author;
  published_at: string;
  scheduled_at: string | null;
  created_at: string;
  updated_at: string;
  reading_time_minutes: number;
  featured_image: MediaAsset | null;
  seo_title: string;
  seo_description: string;
  canonical_url: string | null;
  noindex: boolean;
  is_ai_generated: boolean;
  is_editor_reviewed: boolean;
  ai_pipeline_name: string | null;
  ai_model_name: string | null;
  confidence_score: number | null;
  fact_check_status: 'unchecked' | 'ai_checked' | 'human_checked' | 'source_verified';
  correction_note: string | null;
  last_corrected_at: string | null;
  key_takeaways?: string[];
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  parent_id: string | null;
  sort_order: number;
  is_active: boolean;
}

export interface Tag {
  id: string;
  name: string;
  slug: string;
}

export interface CompanyTicker {
  id: string;
  name: string;
  ticker: string;
  exchange: string;
  country: string;
  sector: string;
  industry: string;
  logo_url: string | null;
  company_page_slug: string;
}

export interface Source {
  id: string;
  source_name: string;
  source_url: string;
  source_type: 'company_filing' | 'exchange_disclosure' | 'press_release' | 'news_article' | 'official_statement' | 'market_data' | 'social_media' | 'other';
  publisher: string;
  published_at: string | null;
  accessed_at: string;
  relevance_note: string;
  quote_used: string | null;
  is_primary_source: boolean;
}

export interface Author {
  id: string;
  name: string;
  slug: string;
  bio: string;
  avatar_url: string | null;
  author_type: 'human' | 'ai_assisted' | 'editorial_team';
}

export interface MediaAsset {
  id: string;
  public_url: string;
  alt_text: string;
  caption: string;
  credit: string;
  width: number;
  height: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface SiteConfig {
  name: string;
  tagline: string;
  description: string;
  url: string;
  apiUrl: string;
  mediaUrl: string;
  defaultAuthor: string;
  defaultOgImage: string;
}
