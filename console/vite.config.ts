import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  // Empty = same-origin; frontend and backend served together, no hardcoded host.
  // Use a dedicated Vite-prefixed key so unrelated shell BASE_URL values don't leak into the build.
  const apiBaseUrl = env.VITE_API_BASE_URL ?? "";

  return {
    define: {
      VITE_API_BASE_URL: JSON.stringify(apiBaseUrl),
      TOKEN: JSON.stringify(env.TOKEN || ""),
      MOBILE: false,
    },
    plugins: [react()],
    css: {
      modules: {
        localsConvention: "camelCase",
        generateScopedName: "[name]__[local]__[hash:base64:5]",
      },
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
        },
      },
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      host: "0.0.0.0",
      port: 5173,
      // Proxy API requests to the local wowooai backend so the Vite dev
      // page is same-origin with the API and works without .env.local.
      // Override target with WOWOOAI_DEV_BACKEND env var if needed.
      proxy: (() => {
        const target = env.WOWOOAI_DEV_BACKEND || "http://127.0.0.1:8088";
        return {
          "/api": { target, changeOrigin: true },
          "/console": { target, changeOrigin: true },
        };
      })(),
    },
    build: {
      // Output to WowooAI's console directory,
      // so we don't need to copy files manually after build.
      // outDir: path.resolve(__dirname, "../src/wowooai/console"),
      // emptyOutDir: true,
      cssCodeSplit: true,
      sourcemap: mode !== "production",
      chunkSizeWarningLimit: 1000,
    },
  };
});
