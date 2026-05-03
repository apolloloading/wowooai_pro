import { Modal, Form, Input } from "antd";
import { useTranslation } from "react-i18next";
import type { AgentSummary } from "@/api/types/agents";
import { getAgentDisplayName } from "@/utils/agentDisplayName";

interface AgentModalProps {
  open: boolean;
  editingAgent: AgentSummary | null;
  form: ReturnType<typeof Form.useForm>[0];
  selectedSkills: string[];
  onSelectedSkillsChange: (skills: string[]) => void;
  onInstalledSkillsLoaded: (skills: string[]) => void;
  onSave: () => Promise<void>;
  onCancel: () => void;
}

export function AgentModal({
  open,
  editingAgent,
  form,
  onSave,
  onCancel,
}: AgentModalProps) {
  const { t } = useTranslation();

  return (
    <Modal
      title={
        editingAgent
          ? t("agent.editTitle", {
              name: getAgentDisplayName(editingAgent, t),
            })
          : t("agent.createTitle")
      }
      open={open}
      onOk={onSave}
      onCancel={onCancel}
      width={520}
      okText={t("common.save")}
      cancelText={t("common.cancel")}
    >
      <Form form={form} layout="vertical" autoComplete="off">
        {editingAgent && (
          <Form.Item name="id" label={t("agent.id")}>
            <Input disabled />
          </Form.Item>
        )}
        <Form.Item
          name="name"
          label={t("agent.name")}
          rules={[{ required: true, message: t("agent.nameRequired") }]}
        >
          <Input placeholder={t("agent.namePlaceholder")} />
        </Form.Item>
        <Form.Item name="description" label={t("agent.description")}>
          <Input.TextArea
            placeholder={t("agent.descriptionPlaceholder")}
            rows={3}
          />
        </Form.Item>
        <Form.Item
          name="workspace_dir"
          label={t("agent.workspace")}
          help={!editingAgent ? t("agent.workspaceHelp") : undefined}
        >
          <Input
            placeholder="~/.wowooai/workspaces/my-agent"
            disabled={!!editingAgent}
          />
        </Form.Item>
      </Form>
    </Modal>
  );
}
