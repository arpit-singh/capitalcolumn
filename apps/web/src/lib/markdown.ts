import { marked } from 'marked';

// Configure marked for safe financial content rendering
marked.setOptions({
  gfm: true,
  breaks: false,
});

export function renderMarkdown(markdown: string): string {
  return marked.parse(markdown) as string;
}
