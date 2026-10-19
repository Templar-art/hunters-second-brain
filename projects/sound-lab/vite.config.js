import react from '@vitejs/plugin-react';
import safeParser from 'postcss-safe-parser';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [react()],
  resolve: { dedupe: ['react', 'react-dom'] },
  css: { postcss: { parser: safeParser } }
});
