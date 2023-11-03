import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    "proxy": {
      "/api": {
        // TODO: set target with an env variable
        // target: "http://localhost:5000"
        target: "http://rss-api:80"
      },
    }
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: [
      "./tests/setup.js",
    ],
    include: [
      './src/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}',
      './src/*/test.{jsx,js}',
      './src/*/*/test.{jsx,js}'
    ]
  }
});
