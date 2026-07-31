import path from "node:path"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// Builds to a single IIFE bundle (not ES modules) dropped straight into
// the static site's assets/ folder, so it works over plain file:// the
// same way the rest of the site does — no module-script CORS issues,
// no separate Node server required at runtime.
export default defineConfig({
  plugins: [react(), tailwindcss()],
  publicDir: false,
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "./src"),
    },
  },
  build: {
    outDir: path.resolve(import.meta.dirname, "../assets/tdx-widgets"),
    emptyOutDir: true,
    cssCodeSplit: false,
    rollupOptions: {
      input: path.resolve(import.meta.dirname, "./src/main.tsx"),
      output: {
        format: "iife",
        entryFileNames: "tdx-widgets.js",
        assetFileNames: (info) =>
          info.name?.endsWith(".css") ? "tdx-widgets.css" : "[name][extname]",
      },
    },
  },
})
