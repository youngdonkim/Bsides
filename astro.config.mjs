import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel';

export default defineConfig({
  output: 'static',
  site: 'https://bsides.kr',
  adapter: vercel({
    webAnalytics: { enabled: true },
    imageService: true,
    imagesConfig: { sizes: [320, 640, 1280] },
  }),
});
