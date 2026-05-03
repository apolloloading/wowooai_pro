import { Table, Button, Space, Popconfirm, Tag } from "antd";
import type { ColumnsType } from "antd/es/table";
import { useTranslation } from "react-i18next";
import { EditOutlined, DeleteOutlined, RobotOutlined } from "@ant-design/icons";
import { EyeOff, Eye } from "lucide-react";
import type { AgentSummary } from "../../../../api/types/agents";
import { useTheme } from "../../../../contexts/ThemeContext";
import { getAgentDisplayName } from "../../../../utils/agentDisplayName";
import styles from "../index.module.less";

interface AgentTableProps {
  agents: AgentSummary[];
  loading: boolean;
  onEdit: (agent: AgentSummary) => void;
  onDelete: (agentId: string) => void;
  onToggle: (agentId: string, currentEnabled: boolean) => void;
}

export function AgentTable({
  agents,
  loading,
  onEdit,
  onDelete,
  onToggle,
}: AgentTableProps) {
  const { t } = useTranslation();
  const { isDark } = useTheme();

  const disabledStyle: React.CSSProperties = isDark
    ? { color: "rgba(255,255,255,0.35)", opacity: 1 }
    : {};

  const iconStyle: React.CSSProperties = isDark
    ? { color: "rgba(255,255,255,0.85)" }
    : {};

  const columns: ColumnsType<AgentSummary> = [
    {
      title: t("agent.name"),
      dataIndex: "name",
      key: "name",
      width: 240,
      render: (_text: string, record: AgentSummary) => (
        <Space>
          <RobotOutlined
            style={{
              fontSize: 16,
              opacity: record.enabled ? 1 : 0.5,
            }}
          />
          <span style={{ opacity: record.enabled ? 1 : 0.5 }}>
            {getAgentDisplayName(record, t)}
          </span>
          {!record.enabled && <Tag color="error">{t("agent.disabled")}</Tag>}
        </Space>
      ),
    },
    {
      title: t("agent.description"),
      dataIndex: "description",
      key: "description",
      ellipsis: true,
    },
    {
      title: t("common.actions"),
      key: "actions",
      render: (_: any, record: AgentSummary) => (
        <Space>
          <Button
            type="text"
            size="middle"
            icon={<EditOutlined />}
            onClick={() => onEdit(record)}
            disabled={record.id === "wowooai"}
            style={record.id === "wowooai" ? disabledStyle : iconStyle}
            title={
              record.id === "wowooai"
                ? t("agent.defaultNotEditable")
                : undefined
            }
          />
          <Popconfirm
            title={
              record.enabled
                ? t("agent.disableConfirm")
                : t("agent.enableConfirm")
            }
            description={
              record.enabled
                ? t("agent.disableConfirmDesc")
                : t("agent.enableConfirmDesc")
            }
            onConfirm={() => onToggle(record.id, record.enabled)}
            disabled={record.id === "wowooai"}
            okText={t("common.confirm")}
            cancelText={t("common.cancel")}
          >
            <Button
              type="text"
              size="middle"
              icon={record.enabled ? <EyeOff size={14} /> : <Eye size={14} />}
              disabled={record.id === "wowooai"}
              style={record.id === "wowooai" ? disabledStyle : iconStyle}
              title={
                record.id === "wowooai"
                  ? t("agent.defaultNotDisablable")
                  : undefined
              }
            />
          </Popconfirm>
          <Popconfirm
            title={t("agent.deleteConfirm")}
            description={t("agent.deleteConfirmDesc")}
            onConfirm={() => onDelete(record.id)}
            disabled={record.id === "wowooai"}
            okText={t("common.confirm")}
            cancelText={t("common.cancel")}
          >
            <Button
              type="link"
              size="middle"
              danger
              icon={<DeleteOutlined />}
              disabled={record.id === "wowooai"}
              style={record.id === "wowooai" ? disabledStyle : undefined}
              title={
                record.id === "wowooai"
                  ? t("agent.defaultNotDeletable")
                  : undefined
              }
            />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className={styles.tableCard}>
      <Table
        dataSource={agents}
        columns={columns}
        loading={loading}
        rowKey="id"
        pagination={false}
      />
    </div>
  );
}
