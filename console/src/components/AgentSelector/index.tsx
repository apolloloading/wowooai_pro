import { Select, Tag, Tooltip } from "antd";
import { useEffect, useState } from "react";
import { CheckCircle, EyeOff, ChevronRight } from "lucide-react";
import { SparkDownLine, SparkUpLine } from "@agentscope-ai/icons";
import { useAgentStore } from "../../stores/agentStore";
import { agentsApi } from "../../api/modules/agents";
import { useTranslation } from "react-i18next";
import { getAgentDisplayName } from "../../utils/agentDisplayName";
import { useNavigate } from "react-router-dom";
import { useAppMessage } from "../../hooks/useAppMessage";
import styles from "./index.module.less";

interface AgentSelectorProps {
  collapsed?: boolean;
}

function AgentBadge({ size = 18 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="agentBadgeGrad" x1="0" y1="0" x2="24" y2="24" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#3b82f6" />
          <stop offset="100%" stopColor="#1d4ed8" />
        </linearGradient>
      </defs>
      <rect x="1.5" y="1.5" width="21" height="21" rx="6" fill="url(#agentBadgeGrad)" />
      <circle cx="12" cy="9.5" r="2.6" fill="#ffffff" />
      <path
        d="M6.4 17.8c1-2.4 3.1-3.6 5.6-3.6s4.6 1.2 5.6 3.6"
        stroke="#ffffff"
        strokeWidth="1.8"
        strokeLinecap="round"
        fill="none"
      />
      <circle cx="18.4" cy="6.2" r="1.6" fill="#ffffff" opacity="0.95" />
      <circle cx="18.4" cy="6.2" r="0.7" fill="#1d4ed8" />
    </svg>
  );
}

export default function AgentSelector({
  collapsed = false,
}: AgentSelectorProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { selectedAgent, agents, setSelectedAgent, setAgents } =
    useAgentStore();
  const { message } = useAppMessage();
  const [loading, setLoading] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      setLoading(true);
      const data = await agentsApi.listAgents();
      const sortedAgents = [...data.agents].sort((a, b) => {
        if (a.enabled === b.enabled) return 0;
        return a.enabled ? -1 : 1;
      });
      setAgents(sortedAgents);
    } catch (error) {
      console.error("Failed to load agents:", error);
      message.error(t("agent.loadFailed"));
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (value: string) => {
    const targetAgent = agents?.find((a) => a.id === value);

    if (targetAgent && !targetAgent.enabled) {
      message.warning(t("agent.cannotSwitchToDisabled"));
      return;
    }

    setSelectedAgent(value);
    message.success(t("agent.switchSuccess"));
  };

  useEffect(() => {
    if (!agents?.length || selectedAgent === "default") return;

    const currentAgent = agents.find((a) => a.id === selectedAgent);

    if (!currentAgent) {
      setSelectedAgent("default");
      message.warning(t("agent.currentAgentDeleted"));
    } else if (!currentAgent.enabled) {
      setSelectedAgent("default");
      message.warning(t("agent.currentAgentDisabled"));
    }
  }, [agents, selectedAgent, setSelectedAgent, t]);

  const currentAgentInfo = agents?.find((a) => a.id === selectedAgent);

  if (collapsed) {
    return (
      <Tooltip
        title={
          currentAgentInfo
            ? getAgentDisplayName(currentAgentInfo, t)
            : selectedAgent
        }
        placement="right"
        overlayInnerStyle={{ background: "rgba(0,0,0,0.75)", color: "#fff" }}
      >
        <div className={styles.agentSelectorCollapsed}>
          <AgentBadge size={20} />
        </div>
      </Tooltip>
    );
  }

  return (
    <div className={styles.agentSelectorWrapper}>
      <Select
        value={selectedAgent}
        onChange={handleChange}
        loading={loading}
        className={styles.agentSelector}
        placeholder={t("agent.selectAgent")}
        optionLabelProp="label"
        popupClassName={styles.agentSelectorDropdown}
        onDropdownVisibleChange={setDropdownOpen}
        suffixIcon={
          dropdownOpen ? <SparkUpLine size={20} /> : <SparkDownLine size={20} />
        }
        dropdownRender={(menu) => (
          <>
            {menu}
            <div className={styles.dropdownFooter}>
              <button
                className={styles.managementLink}
                onClick={() => {
                  setDropdownOpen(false);
                  navigate("/agents");
                }}
              >
                {t("agent.management")}
                <ChevronRight size={12} strokeWidth={2.5} />
              </button>
            </div>
          </>
        )}
      >
        {agents?.map((agent) => (
          <Select.Option
            key={agent.id}
            value={agent.id}
            disabled={!agent.enabled}
            label={
              <div className={styles.selectedAgentLabel}>
                <AgentBadge size={20} />
                <span>{getAgentDisplayName(agent, t)}</span>
                {!agent.enabled && <EyeOff size={12} strokeWidth={2} />}
              </div>
            }
          >
            <div
              className={styles.agentOption}
              style={{ opacity: agent.enabled ? 1 : 0.5 }}
            >
              <span className={styles.agentOptionNameText}>
                {getAgentDisplayName(agent, t)}
              </span>
              {agent.id === selectedAgent && (
                <CheckCircle
                  size={14}
                  strokeWidth={2}
                  className={styles.activeIndicator}
                />
              )}
              {!agent.enabled && (
                <Tag style={{ margin: 0 }}>{t("agent.disabled")}</Tag>
              )}
            </div>
          </Select.Option>
        ))}
      </Select>
    </div>
  );
}
