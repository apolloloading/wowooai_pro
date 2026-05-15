import { Button } from "@agentscope-ai/design";
import { useTranslation } from "react-i18next";
import { useAgentConfig } from "./useAgentConfig.tsx";
import { ToolExecutionLevelCard } from "./components";
import styles from "./index.module.less";

function AgentConfigPage() {
  const { t } = useTranslation();
  const {
    loading,
    saving,
    error,
    approvalLevel,
    setApprovalLevel,
    fetchConfig,
    handleSave,
  } = useAgentConfig();

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
      <div className={styles.content}>
        <div className={styles.tabContent}>
          <ToolExecutionLevelCard
            value={approvalLevel}
            onChange={setApprovalLevel}
            disabled={saving}
          />
        </div>
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
