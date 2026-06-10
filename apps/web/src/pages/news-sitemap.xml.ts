import { getArticles } from '../lib/data';
import { siteConfig } from '../lib/config';

export async function GET() {
  const now = Date.now();
  const fortyEightHoursAgo = now - 48 * 60 * 60 * 1000;

  const allArticles = await getArticles();
  const recentArticles = allArticles.filter(
    (a) => new Date(a.published_at).getTime() >= fortyEightHoursAgo
  );

  const items = recentArticles.map((article) => `
  <url>
    <loc>${siteConfig.url}/news/${article.slug}</loc>
    <news:news>
      <news:publication>
        <news:name>${siteConfig.name}</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>${new Date(article.published_at).toISOString()}</news:publication_date>
      <news:title><![CDATA[${article.title}]]></news:title>
      <news:keywords>${article.tags.map((t) => t.name).join(', ')}</news:keywords>
    </news:news>
  </url>`).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  ${items}
</urlset>`;

  return new Response(xml.trim(), {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=1800',
    },
  });
}
