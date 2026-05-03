import { Button, Tooltip, Dropdown } from "@agentscope-ai/design";
import type { ColumnsType } from "antd/es/table";
import type { MenuProps } from "antd";
import type { CronJobSpecOutput } from "../../../../api/types";
import { MoreOutlined } from "@ant-design/icons";
import { TFunction } from "i18next";
import { parseCron } from "./parseCron";
import styles from "../index.module.less";

type CronJob = CronJobSpecOutput;

interface ColumnHandlers {
  onToggleEnabled: (job: CronJob) => void;
  onExecuteNow: (job: CronJob) => void;
  onEdit: (job: CronJob) => void;
  onDelete: (jobId: string) => void;
  t: TFunction;
}

export const createColumns = (
  handlers: ColumnHandlers,
): ColumnsType<CronJob> => {
  return [
    {
      title: handlers.t("cronJobs.name"),
      dataIndex: "name",
      key: "name",
      width: 200,
      fixed: "left",
    },
    {
      title: handlers.t("cronJobs.enabled"),
      dataIndex: "enabled",
      key: "enabled",
      width: 100,
      render: (enabled: boolean) => (
        <span className={styles.statusIndicator}>
          <span
            className={`${styles.statusDot} ${
              enabled ? styles.enabled : styles.disabled
            }`}
          />
          {enabled
            ? handlers.t("common.enabled")
            : handlers.t("common.disabled")}
        </span>
      ),
    },
    {
      title: handlers.t("cronJobs.scheduleCron"),
      dataIndex: ["schedule", "cron"],
      key: "cron",
      width: 200,
      render: (cron: string) => {
        const cronParts = parseCron(cron || "0 9 * * *");
        let displayText = "";
        switch (cronParts.type) {
          case "hourly":
            displayText = handlers.t("cronJobs.cronTypeHourly");
            break;
          case "daily":
            displayText = `${handlers.t("cronJobs.cronTypeDaily")} ${String(cronParts.hour).padStart(2, "0")}:${String(cronParts.minute).padStart(2, "0")}`;
            break;
          case "weekly": {
            const dayNames = (cronParts.daysOfWeek || []).map((d) => {
              const dayMap: Record<string, string> = {
                mon: handlers.t("cronJobs.cronDayMon"),
                tue: handlers.t("cronJobs.cronDayTue"),
                wed: handlers.t("cronJobs.cronDayWed"),
                thu: handlers.t("cronJobs.cronDayThu"),
                fri: handlers.t("cronJobs.cronDayFri"),
                sat: handlers.t("cronJobs.cronDaySat"),
                sun: handlers.t("cronJobs.cronDaySun"),
              };
              return dayMap[d] || d;
            }).join(",");
            displayText = `${handlers.t("cronJobs.cronTypeWeekly")} ${dayNames} ${String(cronParts.hour).padStart(2, "0")}:${String(cronParts.minute).padStart(2, "0")}`;
            break;
          }
          case "custom":
            displayText = cron;
            break;
        }
        return (
          <Tooltip title={<div><div>Cron: {cron}</div></div>}>
            <span className={styles.cronText}>{displayText}</span>
          </Tooltip>
        );
      },
    },
    {
      title: handlers.t("cronJobs.scheduleTimezone"),
      dataIndex: ["schedule", "timezone"],
      key: "timezone",
      width: 160,
    },
    {
      title: handlers.t("cronJobs.taskContent", "任务内容"),
      key: "task_content",
      width: 260,
      ellipsis: true,
      render: (_: unknown, record: CronJob) => {
        // 合并 text + request.input 展示
        const textPart = (record as any).text || "";
        const inputPart = (record as any).request?.input
          ? JSON.stringify((record as any).request.input)
          : "";
        const display = textPart || inputPart || "-";
        return (
          <Tooltip title={display}>
            <span className={styles.tableText}>{display}</span>
          </Tooltip>
        );
      },
    },
    {
      title: handlers.t("cronJobs.action"),
      key: "action",
      width: 200,
      fixed: "right",
      render: (_: unknown, record: CronJob) => {
        const menuItems: MenuProps["items"] = [
          {
            key: "edit",
            label: handlers.t("cronJobs.edit"),
            disabled: record.enabled,
            onClick: () => handlers.onEdit(record),
          },
          {
            key: "delete",
            label: handlers.t("cronJobs.delete"),
            disabled: record.enabled,
            danger: true,
            onClick: () => handlers.onDelete(record.id),
          },
        ];
        return (
          <div className={styles.actionColumn}>
            <Button type="link" size="small" onClick={() => handlers.onToggleEnabled(record)}>
              {record.enabled ? handlers.t("cronJobs.disable") : handlers.t("common.enable")}
            </Button>
            <Button type="link" size="small" onClick={() => handlers.onExecuteNow(record)}>
              {handlers.t("cronJobs.executeNow")}
            </Button>
            <Dropdown menu={{ items: menuItems }} placement="bottomRight">
              <Button type="text" size="small" icon={<MoreOutlined />} />
            </Dropdown>
          </div>
        );
      },
    },
  ];
};
