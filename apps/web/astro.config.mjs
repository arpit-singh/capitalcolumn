import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  output: 'static',
  site: 'https://capitalcolumn.in',
  integrations: [sitemap()],
  vite: {
    resolve: {
      alias: {
        '@': '/src',
      },
    },
  },
});
