import type { SiteConfig } from './types';

export const siteConfig: SiteConfig = {
  name: 'CapitalColumn',
  tagline: 'AI-Powered Financial Intelligence',
  description:
    'CapitalColumn delivers AI-assisted financial news, market analysis, and earnings coverage with full source transparency and editorial oversight.',
  url: import.meta.env.PUBLIC_SITE_URL || 'https://capitalcolumn.in',
  apiUrl: import.meta.env.PUBLIC_API_BASE_URL || 'https://api.capitalcolumn.in',
  mediaUrl:
    import.meta.env.PUBLIC_MEDIA_BASE_URL || 'https://media.capitalcolumn.in',
  defaultAuthor: 'CapitalColumn Editorial Desk',
  defaultOgImage: '/og-default.png',
};
