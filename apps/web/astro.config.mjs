import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server',
  adapter: cloudflare({
    imageService: 'compile'
  }),
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
