import { useState, useRef, useCallback } from "react";
import { Card, Button, Form } from "antd";
import { useAppMessage } from "../../../hooks/useAppMessage";
import { PlusOutlined, RobotOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { agentsApi } from "../../../api/modules/agents";
import { invalidateSkillCache } from "../../../api/modules/skill";
import type { AgentSummary } from "../../../api/types/agents";
import { useAgentStore } from "../../../stores/agentStore";
import { useAgents } from "./useAgents";
import { AgentTable, AgentModal } from "./components";
import { PageHeader } from "@/components/PageHeader";
import styles from "./index.module.less";

export default function AgentsPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { agents, loading, deleteAgent, toggleAgent, loadAgents } =
    useAgents();
  const { selectedAgent, setSelectedAgent } = useAgentStore();
  const [modalVisible, setModalVisible] = useState(false);
  const [editingAgent, setEditingAgent] = useState<AgentSummary | null>(null);
  const [form] = Form.useForm();
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const installedSkillsRef = useRef<string[]>([]);
  const { message } = useAppMessage();

  const handleCreate = () => {
    setEditingAgent(null);
    form.resetFields();
    form.setFieldsValue({
      workspace_dir: "",
    });
    setSelectedSkills([]);
    installedSkillsRef.current = [];
    setModalVisible(true);
  };

  const handleAICreate = () => {
    navigate("/chat");
    setTimeout(() => {
      const event = new CustomEvent("wowooai:chat-input", {
        detail: { text: "[使用技能：AI创建数字员工]，帮我创建一个数字员工" },
      });
      window.dispatchEvent(event);
    }, 800);
  };

  const handleEdit = async (agent: AgentSummary) => {
    try {
      setSelectedSkills([]);
      installedSkillsRef.current = [];
      invalidateSkillCache({ agentId: agent.id });
      const config = await agentsApi.getAgent(agent.id);
      setEditingAgent(agent);
      form.setFieldsValue(config);
      setModalVisible(true);
    } catch (error) {
      console.error("Failed to load agent config:", error);
      message.error(t("agent.loadConfigFailed"));
    }
  };

  const handleDelete = async (agentId: string) => {
    try {
      await deleteAgent(agentId);

      if (selectedAgent === agentId) {
        setSelectedAgent("wowooai");
        message.info(t("agent.switchedToDefault"));
      }
    } catch {
      message.error(t("agent.deleteFailed"));
    }
  };

  const handleToggle = async (agentId: string, currentEnabled: boolean) => {
    const newEnabled = !currentEnabled;
    try {
      await toggleAgent(agentId, newEnabled);

      if (!newEnabled && selectedAgent === agentId) {
        setSelectedAgent("wowooai");
        message.info(t("agent.switchedToDefault"));
      }
    } catch {
      // Error already handled in hook
    }
  };

  const handleInstalledSkillsLoaded = useCallback((skills: string[]) => {
    installedSkillsRef.current = skills;
  }, []);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const workspaceRaw = values.workspace_dir;
      const workspace_dir =
        typeof workspaceRaw === "string"
          ? workspaceRaw.trim() || undefined
          : workspaceRaw;
      const payload = { ...values, workspace_dir };

      if (editingAgent) {
        await agentsApi.updateAgent(editingAgent.id, payload);
        invalidateSkillCache({ agentId: editingAgent.id });
        message.success(t("agent.updateSuccess"));
      } else {
        const result = await agentsApi.createAgent({ ...payload });
        message.success(`${t("agent.createSuccess")} (ID: ${result.id})`);
      }

      setModalVisible(false);
      await loadAgents();
    } catch (error: any) {
      console.error("Failed to save agent:", error);
      if (editingAgent) {
        invalidateSkillCache({ agentId: editingAgent.id });
      }
      message.error(error.message || t("agent.saveFailed"));
    }
  };

  return (
    <div className={styles.agentsPage}>
      <PageHeader
        items={[{ title: t("agent.agents") }]}
        extra={
          <div className={styles.headerRight}>
            <Button
              icon={<RobotOutlined />}
              onClick={handleAICreate}
            >
              AI 创建数字员工
            </Button>
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={handleCreate}
            >
              {t("agent.create")}
            </Button>
          </div>
        }
      />

      <Card className={styles.tableCard}>
        <AgentTable
          agents={agents}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onToggle={handleToggle}
        />
      </Card>

      <AgentModal
        open={modalVisible}
        editingAgent={editingAgent}
        form={form}
        selectedSkills={selectedSkills}
        onSelectedSkillsChange={setSelectedSkills}
        onInstalledSkillsLoaded={handleInstalledSkillsLoaded}
        onSave={handleSubmit}
        onCancel={() => setModalVisible(false)}
      />
    </div>
  );
}
