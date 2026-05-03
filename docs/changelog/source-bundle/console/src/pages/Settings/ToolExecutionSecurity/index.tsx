import { useCallback, useEffect, useRef, useState } from "react";
import { Button, Spin, Alert, Space } from "antd";
import { useTranslation } from "react-i18next";
import { agentsApi } from "../../../api/modules/agents";
import { useAgentStore } from "../../../stores/agentStore";
import { useAppMessage } from "../../../hooks/useAppMessage";
import type { AgentProfileConfig } from "../../../api/types/agents";
import {
  ToolExecutionLevelCard,
  type ToolExecutionLevel,
} from "../../Agent/Config/components/ToolExecutionLevelCard";

export default function ToolExecutionSecurityPage() {
  const { t } = useTranslation();
  const { message } = useAppMessage();
  const { selectedAgent } = useAgentStore();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [level, setLevel] = useState<ToolExecutionLevel>("AUTO");
  const initialLevelRef = useRef<ToolExecutionLevel>("AUTO");
  const profileRef = useRef<AgentProfileConfig | null>(null);

  const fetchConfig = useCallback(async () => {
    if (!selectedAgent) return;
    setLoading(true);
    setError(null);
    try {
      const profile = await agentsApi.getAgent(selectedAgent);
      profileRef.current = profile;
      const loaded = (
        profile?.approval_level || "AUTO"
      ).toUpperCase() as ToolExecutionLevel;
      setLevel(loaded);
      initialLevelRef.current = loaded;
    } catch (err) {
      setError(
        err instanceof Error ? err.message : t("agentConfig.loadFailed"),
      );
    } finally {
      setLoading(false);
    }
  }, [selectedAgent, t]);

  useEffect(() => {
    fetchConfig();
  }, [fetchConfig]);

  const handleSave = useCallback(async () => {
    if (!profileRef.current || !selectedAgent) return;
    setSaving(true);
    try {
      const next = { ...profileRef.current, approval_level: level };
      await agentsApi.updateAgent(selectedAgent, next);
      profileRef.current = next;
      initialLevelRef.current = level;
      message.success(t("agentConfig.saveLevelSuccess"));
    } catch (err) {
      message.error(
        err instanceof Error ? err.message : t("agentConfig.saveLevelFailed"),
      );
    } finally {
      setSaving(false);
    }
  }, [level, selectedAgent, message, t]);

  if (loading) {
    return (
      <div style={{ padding: 40, textAlign: "center" }}>
        <Spin />
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: 24 }}>
        <Alert
          type="error"
          message={error}
          action={
            <Button size="small" onClick={fetchConfig}>
              {t("environments.retry")}
            </Button>
          }
        />
      </div>
    );
  }

  const dirty = level !== initialLevelRef.current;

  return (
    <div style={{ padding: 24 }}>
      <ToolExecutionLevelCard
        value={level}
        onChange={setLevel}
        disabled={saving}
      />
      <div style={{ marginTop: 16, textAlign: "right" }}>
        <Space>
          <Button
            onClick={() => setLevel(initialLevelRef.current)}
            disabled={!dirty || saving}
          >
            {t("common.reset")}
          </Button>
          <Button
            type="primary"
            onClick={handleSave}
            loading={saving}
            disabled={!dirty}
          >
            {t("common.save")}
          </Button>
        </Space>
      </div>
    </div>
  );
}
