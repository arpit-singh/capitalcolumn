import { getArticles } from '../lib/data';
import { siteConfig } from '../lib/config';

export async function GET() {
  const articles = getArticles().slice(0, 50);

  const items = articles.map((article) => `
    <item>
      <title><![CDATA[${article.title}]]></title>
      <link>${siteConfig.url}/news/${article.slug}</link>
      <description><![CDATA[${article.dek}]]></description>
      <pubDate>${new Date(article.published_at).toUTCString()}</pubDate>
      <guid isPermaLink="true">${siteConfig.url}/news/${article.slug}</guid>
      <category>${article.category.name}</category>
    </item>`).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${siteConfig.name}</title>
    <link>${siteConfig.url}</link>
    <description>${siteConfig.description}</description>
    <language>en</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <atom:link href="${siteConfig.url}/rss.xml" rel="self" type="application/rss+xml" />
    ${items}
  </channel>
</rss>`;

  return new Response(xml.trim(), {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
