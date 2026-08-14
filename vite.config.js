import { defineConfig } from 'vite';
import { resolve } from 'path';

// Multi-page static site: every HTML page is a build entry.
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        plansPricing: resolve(__dirname, 'plans-pricing.html'),
        projects: resolve(__dirname, 'projects.html'),
        about: resolve(__dirname, 'about.html'),
        contact: resolve(__dirname, 'contact.html'),
        consultancy: resolve(__dirname, 'consultancy.html'),
      },
    },
  },
});
