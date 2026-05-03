import { Suspense } from "react";
import { Layout, Spin } from "antd";
import { Routes, Route, useLocation, Navigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import Sidebar from "../Sidebar";
import Header from "../Header";
import ConsolePollService from "../../components/ConsolePollService";
import { ChunkErrorBoundary } from "../../components/ChunkErrorBoundary";
import { lazyImportWithRetry } from "../../utils/lazyWithRetry";
import { usePlugins } from "../../plugins/PluginContext";
import styles from "../index.module.less";

import Chat from "../../pages/Chat";

const ChannelsPage = lazyImportWithRetry("../../pages/Control/Channels");
const CronJobsPage = lazyImportWithRetry("../../pages/Control/CronJobs");
const AgentConfigPage = lazyImportWithRetry("../../pages/Agent/Config");
const SkillsPage = lazyImportWithRetry("../../pages/Agent/Skills");
const WorkspacePage = lazyImportWithRetry("../../pages/Agent/Workspace");
const MCPPage = lazyImportWithRetry("../../pages/Agent/MCP");
const ModelsPage = lazyImportWithRetry("../../pages/Settings/Models");
const TokenUsagePage = lazyImportWithRetry("../../pages/Settings/TokenUsage");

const { Content } = Layout;

const pathToKey: Record<string, string> = {
  "/chat": "chat",
  "/channels": "channels",
  "/cron-jobs": "cron-jobs",
  "/skills": "skills",
  "/mcp": "mcp",
  "/workspace": "workspace",
  "/models": "models",
  "/agent-config": "agent-config",
  "/token-usage": "token-usage",
};

export default function MainLayout() {
  const { t } = useTranslation();
  const location = useLocation();
  const currentPath = location.pathname;
  const { pluginRoutes } = usePlugins();

  let selectedKey = pathToKey[currentPath] || "";
  if (!selectedKey) {
    const matchedPlugin = pluginRoutes.find(
      (route) => currentPath === route.path,
    );
    selectedKey = matchedPlugin
      ? matchedPlugin.path.replace(/^\//, "")
      : "chat";
  }

  return (
    <Layout className={styles.mainLayout}>
      <Header />
      <Layout>
        <Sidebar selectedKey={selectedKey} />
        <Content className="page-container">
          <ConsolePollService />
          <div className="page-content">
            <ChunkErrorBoundary resetKey={currentPath}>
              <Suspense
                fallback={
                  <Spin
                    tip={t("common.loading")}
                    style={{ display: "block", margin: "20vh auto" }}
                  />
                }
              >
                <Routes>
                  <Route path="/" element={<Navigate to="/chat" replace />} />
                  <Route path="/chat/*" element={<Chat />} />
                  <Route path="/channels" element={<ChannelsPage />} />
                  <Route path="/cron-jobs" element={<CronJobsPage />} />
                  <Route path="/skills" element={<SkillsPage />} />
                  <Route path="/mcp" element={<MCPPage />} />
                  <Route path="/workspace" element={<WorkspacePage />} />
                  <Route path="/models" element={<ModelsPage />} />
                  <Route path="/agent-config" element={<AgentConfigPage />} />
                  <Route path="/token-usage" element={<TokenUsagePage />} />

                  {pluginRoutes.map((route) => (
                    <Route
                      key={route.path}
                      path={route.path}
                      element={<route.component />}
                    />
                  ))}
                </Routes>
              </Suspense>
            </ChunkErrorBoundary>
          </div>
        </Content>
      </Layout>
    </Layout>
  );
}
