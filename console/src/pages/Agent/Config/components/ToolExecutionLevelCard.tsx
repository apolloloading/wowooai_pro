import { Radio, Space, Typography } from "antd";
import { Shield, CheckCircle, AlertTriangle, Ban } from "lucide-react";
import { useTranslation } from "react-i18next";
import styles from "../index.module.less";

const { Text, Paragraph } = Typography;

export type ToolExecutionLevel = "STRICT" | "SMART" | "AUTO" | "OFF";

interface LevelOption {
  value: ToolExecutionLevel;
  label: string;
  icon: React.ReactNode;
  description: string;
  color: string;
}

interface ToolExecutionLevelCardProps {
  value: ToolExecutionLevel;
  onChange: (level: ToolExecutionLevel) => void;
  disabled?: boolean;
}

export function ToolExecutionLevelCard({
  value: level,
  onChange,
  disabled = false,
}: ToolExecutionLevelCardProps) {
  const { t } = useTranslation();

  const levelOptions: LevelOption[] = [
    {
      value: "STRICT",
      label: t("agentConfig.toolExecutionLevel.strict"),
      icon: <Ban size={18} />,
      description: t("agentConfig.toolExecutionLevel.strictDesc"),
      color: "#ff4d4f",
    },
    {
      value: "SMART",
      label: t("agentConfig.toolExecutionLevel.smart"),
      icon: <AlertTriangle size={18} />,
      description: t("agentConfig.toolExecutionLevel.smartDesc"),
      color: "#faad14",
    },
    {
      value: "AUTO",
      label: t("agentConfig.toolExecutionLevel.auto"),
      icon: <Shield size={18} />,
      description: t("agentConfig.toolExecutionLevel.autoDesc"),
      color: "#1890ff",
    },
    {
      value: "OFF",
      label: t("agentConfig.toolExecutionLevel.off"),
      icon: <CheckCircle size={18} />,
      description: t("agentConfig.toolExecutionLevel.offDesc"),
      color: "#52c41a",
    },
  ];

  return (
    <div className={styles.formCard}>
      <Radio.Group
        value={level}
        onChange={(e) => onChange(e.target.value as ToolExecutionLevel)}
        disabled={disabled}
        style={{ width: "100%" }}
      >
        <Space direction="vertical" size={16} style={{ width: "100%" }}>
          {levelOptions.map((option) => (
            <div
              key={option.value}
              className={styles.levelOptionCard}
              style={{
                borderColor: level === option.value ? option.color : "#e8e8e8",
                borderWidth: level === option.value ? 2 : 1,
                borderStyle: "solid",
                borderRadius: 8,
                padding: 16,
                cursor: "pointer",
                transition: "all 0.3s",
                background: "#fff",
              }}
              onClick={() => !disabled && onChange(option.value)}
            >
              <Radio value={option.value} style={{ width: "100%" }}>
                <div style={{ marginLeft: 12 }}>
                  <Space align="start" size={12}>
                    <div style={{ color: option.color, marginTop: 2 }}>
                      {option.icon}
                    </div>
                    <div style={{ flex: 1 }}>
                      <Text strong style={{ fontSize: 15 }}>
                        {option.label}
                      </Text>
                      <Paragraph
                        type="secondary"
                        style={{ margin: "4px 0 0 0", fontSize: 13 }}
                      >
                        {option.description}
                      </Paragraph>
                    </div>
                  </Space>
                </div>
              </Radio>
            </div>
          ))}
        </Space>
      </Radio.Group>
    </div>
  );
}
