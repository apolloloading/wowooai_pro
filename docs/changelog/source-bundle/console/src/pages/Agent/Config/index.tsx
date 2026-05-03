import { useState, useMemo, useEffect } from "react";
import { Button, Tabs } from "@agentscope-ai/design";
import { useTranslation } from "react-i18next";
import { useAgentConfig } from "./useAgentConfig.tsx";
import { ToolExecutionLevelCard } from "./components";
import { PageHeader } from "@/components/PageHeader";
import styles from "./index.module.less";

function AgentConfigPage() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState("toolExecutionLevel");
  const {
    loading,
    saving,
    error,
    approvalLevel,
    setApprovalLevel,
    fetchConfig,
    handleSave,
  } = useAgentConfig();

  const dynamicTabs = useMemo(
    () => [
      {
        key: "toolExecutionLevel",
        label: (
          <span className={styles.tabLabel}>
            {t("agentConfig.toolExecutionLevelTitle")}
          </span>
        ),
        children: (
          <div className={styles.tabContent}>
            <ToolExecutionLevelCard
              value={approvalLevel}
              onChange={setApprovalLevel}
              disabled={saving}
            />
          </div>
        ),
      },
    ],
    [t, approvalLevel, setApprovalLevel, saving],
  );

  useEffect(() => {
    const tabKeys = dynamicTabs.map((t) => t.key);
    if (!tabKeys.includes(activeTab)) {
      setActiveTab(tabKeys[0] ?? "toolExecutionLevel");
    }
  }, [dynamicTabs, activeTab]);

  if (loading) {
    return (
      <div className={styles.configPage}>
        <div className={styles.centerState}>
          <span className={styles.stateText}>{t("common.loading")}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.configPage}>
        <div className={styles.centerState}>
          <span className={styles.stateTextError}>{error}</span>
          <Button size="small" onClick={fetchConfig} style={{ marginTop: 12 }}>
            {t("environments.retry")}
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.configPage}>
      <PageHeader parent={t("nav.agent")} current={t("agentConfig.title")} />

      <div className={styles.content}>
        <Tabs
          className={styles.mainTabs}
          activeKey={activeTab}
          onChange={setActiveTab}
          items={dynamicTabs}
          destroyInactiveTabPane={false}
        />
      </div>

      <div className={styles.footerActions}>
        <Button
          onClick={fetchConfig}
          disabled={saving}
          style={{ marginRight: 8 }}
        >
          {t("common.reset")}
        </Button>
        <Button type="primary" onClick={handleSave} loading={saving}>
          {t("common.save")}
        </Button>
      </div>
    </div>
  );
}

export default AgentConfigPage;
