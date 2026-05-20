import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

/** CI（GitHub Pages）通过 env 传入；本地默认 "/" */
const trimmed = process.env.VITE_PAGES_BASE?.trim();
const base = trimmed ? trimmed : "/";

export default defineConfig({
  base,
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: false,
  },
});
