import { useState, useEffect, useCallback, useRef } from "react";
import { useTranslation } from "react-i18next";
import { agentsApi } from "../../../api/modules/agents";
import type { AgentProfileConfig } from "../../../api/types/agents";
import { useAppMessage } from "../../../hooks/useAppMessage";
import { useAgentStore } from "../../../stores/agentStore";
import type { ToolExecutionLevel } from "./components/ToolExecutionLevelCard";

export function useAgentConfig() {
  const { t } = useTranslation();
  const { message } = useAppMessage();
  const { selectedAgent } = useAgentStore();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [approvalLevel, setApprovalLevel] =
    useState<ToolExecutionLevel>("AUTO");
  const initialApprovalLevelRef = useRef<ToolExecutionLevel>("AUTO");
  const agentProfileRef = useRef<AgentProfileConfig | null>(null);

  const fetchConfig = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const agentProfile = await agentsApi.getAgent(selectedAgent);
      agentProfileRef.current = agentProfile;
      const loadedLevel = (
        agentProfile.approval_level || "AUTO"
      ).toUpperCase() as ToolExecutionLevel;
      setApprovalLevel(loadedLevel);
      initialApprovalLevelRef.current = loadedLevel;
    } catch (err) {
      const errMsg =
        err instanceof Error ? err.message : t("agentConfig.loadFailed");
      setError(errMsg);
    } finally {
      setLoading(false);
    }
  }, [t, selectedAgent]);

  useEffect(() => {
    fetchConfig();
  }, [fetchConfig]);

  const handleSave = useCallback(async () => {
    if (!agentProfileRef.current) return;
    setSaving(true);
    try {
      const updatedProfile: AgentProfileConfig = {
        ...agentProfileRef.current,
        approval_level: approvalLevel,
      };
      await agentsApi.updateAgent(selectedAgent, updatedProfile);
      agentProfileRef.current = updatedProfile;
      initialApprovalLevelRef.current = approvalLevel;
      message.success(t("agentConfig.saveSuccess"));
    } catch (err) {
      const errMsg =
        err instanceof Error ? err.message : t("agentConfig.saveFailed");
      message.error(errMsg);
    } finally {
      setSaving(false);
    }
  }, [t, selectedAgent, approvalLevel, message]);

  return {
    loading,
    saving,
    error,
    approvalLevel,
    setApprovalLevel,
    fetchConfig,
    handleSave,
  };
}
