import { appTools, defineConfig } from '@modern-js/app-tools';
import { tailwindcssPlugin } from '@modern-js/plugin-tailwindcss';

// https://modernjs.dev/en/configure/app/usage
export default defineConfig({
  runtime: {
    router: true,
    state: true,
  },
  source: {
    alias: {
      '@': './src',
      src: './src',
    },
  },
  tools: {
    devServer: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
        '/ws': {
          target: 'ws://localhost:8000',
          ws: true,
        },
      },
    },
  },
  output: {
    disableTsChecker: false,
    polyfill: 'usage',
  },
  performance: {
    chunkSplit: {
      strategy: 'split-by-experience',
    },
  },
  server: {
    ssr: false, // Disable SSR for SPA mode
  },
  plugins: [
    appTools({
      bundler: 'rspack', // Set to 'webpack' to enable webpack
    }),
    tailwindcssPlugin(),
  ],
});
