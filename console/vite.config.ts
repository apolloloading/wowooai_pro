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
      rollupOptions: {
        output: {
          manualChunks(id) {
            // React core
            if (
              id.includes("node_modules/react/") ||
              id.includes("node_modules/react-dom/") ||
              id.includes("node_modules/react-router-dom/") ||
              id.includes("node_modules/scheduler/")
            ) {
              return "react-vendor";
            }
            // mermaid: only loaded when rendering diagrams
            if (id.includes("node_modules/mermaid/")) {
              return "mermaid-vendor";
            }
            // Code highlighting: only used inside chat code blocks
            if (
              id.includes("node_modules/react-syntax-highlighter/") ||
              id.includes("node_modules/refractor/") ||
              id.includes("node_modules/prismjs/") ||
              id.includes("node_modules/highlight.js/")
            ) {
              return "syntax-highlighter";
            }
            // @ant-design/graphs: large, only used on graph pages
            if (id.includes("node_modules/@ant-design/graphs")) {
              return "antd-graphs";
            }
            // cytoscape: indirectly pulled by @ant-design/graphs
            if (id.includes("node_modules/cytoscape")) {
              return "cytoscape-vendor";
            }
            // @ant-design/x: chat UI kit
            if (id.includes("node_modules/@ant-design/x")) {
              return "antd-x";
            }
            // @agentscope-ai/chat: chat page main component
            if (id.includes("node_modules/@agentscope-ai/chat")) {
              return "agentscope-chat";
            }
            // @agentscope-ai/design + icons shared design system
            if (id.includes("node_modules/@agentscope-ai/")) {
              return "agentscope-design";
            }
            // antd core + antd-style + remaining @ant-design/* (icons etc.)
            if (
              id.includes("node_modules/antd/") ||
              id.includes("node_modules/antd-style/") ||
              id.includes("node_modules/@ant-design/")
            ) {
              return "antd-core";
            }
            // i18n
            if (
              id.includes("node_modules/i18next/") ||
              id.includes("node_modules/react-i18next/")
            ) {
              return "i18n-vendor";
            }
            // Markdown rendering
            if (
              id.includes("node_modules/react-markdown/") ||
              id.includes("node_modules/remark-gfm/") ||
              id.includes("node_modules/rehype") ||
              id.includes("node_modules/remark") ||
              id.includes("node_modules/unified/") ||
              id.includes("node_modules/mdast") ||
              id.includes("node_modules/hast") ||
              id.includes("node_modules/micromark")
            ) {
              return "markdown-vendor";
            }
            // Drag and drop
            if (id.includes("node_modules/@dnd-kit/")) {
              return "dnd-vendor";
            }
            // Utilities (dayjs, zustand, ahooks, etc.)
            if (
              id.includes("node_modules/dayjs/") ||
              id.includes("node_modules/zustand/") ||
              id.includes("node_modules/ahooks/") ||
              id.includes("node_modules/@vvo/tzdb/")
            ) {
              return "utils-vendor";
            }
          },
        },
      },
    },
  };
});
