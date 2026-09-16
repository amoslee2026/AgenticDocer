import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// 开发期：5173 → /api 代理到本机 FastAPI（§5：Vite devserver proxy）。
// 产物：dist/ 由 FastAPI 直接挂载到 /（AB2 单进程交付），无需额外配置。
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8787",
        changeOrigin: false,
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false,
  },
});
