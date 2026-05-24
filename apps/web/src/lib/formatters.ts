/**
 * Format a date string into a human-readable long form.
 * Example: "May 24, 2026"
 */
export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

/**
 * Format a date string into a compact short form.
 * Example: "May 24"
 */
export function formatDateShort(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Format a date string as a human-readable relative timestamp.
 * Examples: "just now", "2 hours ago", "3 days ago"
 */
export function formatRelativeTime(dateStr: string): string {
  const now = Date.now();
  const then = new Date(dateStr).getTime();
  const diffMs = now - then;

  if (diffMs < 0) return 'just now';

  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const weeks = Math.floor(days / 7);
  const months = Math.floor(days / 30);

  if (seconds < 60) return 'just now';
  if (minutes === 1) return '1 minute ago';
  if (minutes < 60) return `${minutes} minutes ago`;
  if (hours === 1) return '1 hour ago';
  if (hours < 24) return `${hours} hours ago`;
  if (days === 1) return 'yesterday';
  if (days < 7) return `${days} days ago`;
  if (weeks === 1) return '1 week ago';
  if (weeks < 5) return `${weeks} weeks ago`;
  if (months === 1) return '1 month ago';
  if (months < 12) return `${months} months ago`;

  return formatDate(dateStr);
}

/**
 * Format reading time in minutes.
 * Example: "5 min read"
 */
export function formatReadingTime(minutes: number): string {
  if (minutes <= 1) return '1 min read';
  return `${minutes} min read`;
}

/**
 * Convert an article_type enum value to a human-readable label.
 */
export function getArticleTypeLabel(
  type: string,
): string {
  const labels: Record<string, string> = {
    news: 'News',
    analysis: 'Analysis',
    explainer: 'Explainer',
    earnings: 'Earnings',
    market_update: 'Market Update',
    alert: 'Alert',
    opinion: 'Opinion',
  };
  return labels[type] ?? type;
}

/**
 * Convert a source_type enum value to a human-readable label.
 */
export function getSourceTypeLabel(
  type: string,
): string {
  const labels: Record<string, string> = {
    company_filing: 'Company Filing',
    exchange_disclosure: 'Exchange Disclosure',
    press_release: 'Press Release',
    news_article: 'News Article',
    official_statement: 'Official Statement',
    market_data: 'Market Data',
    social_media: 'Social Media',
    other: 'Other',
  };
  return labels[type] ?? type;
}

/**
 * Truncate text to a maximum length, appending an ellipsis if trimmed.
 */
export function truncate(text: string, maxLen: number): string {
  if (text.length <= maxLen) return text;
  const trimmed = text.slice(0, maxLen);
  // Cut at the last space so we don't break mid-word
  const lastSpace = trimmed.lastIndexOf(' ');
  return (lastSpace > 0 ? trimmed.slice(0, lastSpace) : trimmed) + '…';
}
