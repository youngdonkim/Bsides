import { defineConfig, fontProviders } from 'astro/config';
import vercel from '@astrojs/vercel';

export default defineConfig({
  output: 'static',
  site: 'https://bsides.kr',
  adapter: vercel({
    webAnalytics: { enabled: true },
    imageService: true,
    imagesConfig: { sizes: [320, 640, 1280] },
  }),
  fonts: [
    {
      name: 'Nanum Pen Script',
      cssVariable: '--b-font-hand-nps',
      provider: fontProviders.google(),
      weights: [400],
      subsets: ['korean', 'latin'],
    },
    {
      name: 'Gaegu',
      cssVariable: '--b-font-hand-gaegu',
      provider: fontProviders.google(),
      weights: [400, 700],
      subsets: ['korean', 'latin'],
    },
  ],
});
