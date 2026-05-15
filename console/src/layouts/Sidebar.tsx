import { Layout, Button, Modal, Input, Form, Tooltip, Dropdown } from "antd";
import { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAppMessage } from "../hooks/useAppMessage";
import {
  SparkChatTabFill,
  SparkDateLine,
  SparkMagicWandLine,
  SparkLocalFileLine,
  SparkModePlazaLine,
  SparkModifyLine,
  SparkMcpMcpLine,
  SparkWifiLine,
  SparkDataLine,
  SparkExitFullscreenLine,
  SparkSearchUserLine,
  SparkMenuExpandLine,
  SparkMenuFoldLine,
  SparkAccountManagementLine,
} from "@agentscope-ai/icons";
import { ChevronDown } from "lucide-react";
import { clearAuthToken } from "../api/config";
import { authApi } from "../api/modules/auth";
import AgentSelector from "../components/AgentSelector";
import styles from "./index.module.less";
import { useTheme } from "../contexts/ThemeContext";

const { Sider } = Layout;

interface SidebarProps {
  selectedKey: string;
}

export default function Sidebar({ selectedKey }: SidebarProps) {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { message } = useAppMessage();
  const { isDark } = useTheme();
  const [authEnabled, setAuthEnabled] = useState(false);
  const [accountModalOpen, setAccountModalOpen] = useState(false);
  const [accountLoading, setAccountLoading] = useState(false);
  const [accountForm] = Form.useForm();
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    authApi
      .getStatus()
      .then((res) => setAuthEnabled(res.enabled))
      .catch(() => {});
  }, []);

  const handleUpdateProfile = async (values: {
    currentPassword: string;
    newUsername?: string;
    newPassword?: string;
  }) => {
    const trimmedUsername = values.newUsername?.trim() || undefined;
    const trimmedPassword = values.newPassword?.trim() || undefined;

    if (values.newPassword && !trimmedPassword) {
      message.error(t("account.passwordEmpty"));
      return;
    }

    if (values.newUsername && !trimmedUsername) {
      message.error(t("account.usernameEmpty"));
      return;
    }

    if (!trimmedUsername && !trimmedPassword) {
      message.warning(t("account.nothingToUpdate"));
      return;
    }

    setAccountLoading(true);
    try {
      await authApi.updateProfile(
        values.currentPassword,
        trimmedUsername,
        trimmedPassword,
      );
      message.success(t("account.updateSuccess"));
      setAccountModalOpen(false);
      accountForm.resetFields();
      clearAuthToken();
      window.location.href = "/login";
    } catch (err: unknown) {
      const raw = err instanceof Error ? err.message : "";
      let msg = t("account.updateFailed");
      if (raw.includes("password is incorrect")) {
        msg = t("account.wrongPassword");
      } else if (raw.includes("Nothing to update")) {
        msg = t("account.nothingToUpdate");
      } else if (raw.includes("cannot be empty")) {
        msg = t("account.nothingToUpdate");
      } else if (raw) {
        msg = raw;
      }
      message.error(msg);
    } finally {
      setAccountLoading(false);
    }
  };

  const navItems = [
    {
      key: "chat",
      icon: <SparkChatTabFill size={18} />,
      path: "/chat",
      label: t("nav.chat"),
    },
    {
      key: "cron-jobs",
      icon: <SparkDateLine size={18} />,
      path: "/cron-jobs",
      label: t("nav.cronJobs"),
    },
    {
      key: "skills",
      icon: <SparkMagicWandLine size={18} />,
      path: "/skills",
      label: t("nav.skills"),
    },
    {
      key: "mcp",
      icon: <SparkMcpMcpLine size={18} />,
      path: "/mcp",
      label: t("nav.mcp"),
    },
    {
      key: "channels",
      icon: <SparkWifiLine size={18} />,
      path: "/channels",
      label: t("nav.channels"),
    },
    {
      key: "workspace",
      icon: <SparkLocalFileLine size={18} />,
      path: "/workspace",
      label: t("nav.workspace"),
    },
  ];

  const personalCenterItems = [
    {
      key: "models",
      icon: <SparkModePlazaLine size={18} />,
      path: "/models",
      label: t("nav.models"),
    },
    {
      key: "agent-config",
      icon: <SparkModifyLine size={18} />,
      path: "/agent-config",
      label: t("nav.agentConfig"),
    },
    {
      key: "token-usage",
      icon: <SparkDataLine size={18} />,
      path: "/token-usage",
      label: t("nav.tokenUsage"),
    },
  ];

  const personalCenterActive = useMemo(
    () => personalCenterItems.some((it) => it.key === selectedKey),
    [personalCenterItems, selectedKey],
  );

  const [personalCenterOpen, setPersonalCenterOpen] = useState(
    personalCenterActive,
  );

  useEffect(() => {
    if (personalCenterActive) setPersonalCenterOpen(true);
  }, [personalCenterActive]);

  const renderNav = () => (
    <nav className={collapsed ? styles.collapsedNav : styles.sidebarNav}>
      {navItems.map((item) => {
        const isActive = selectedKey === item.key;
        const button = (
          <button
            key={item.key}
            className={
              collapsed
                ? `${styles.collapsedNavItem} ${
                    isActive ? styles.collapsedNavItemActive : ""
                  }`
                : `${styles.sidebarNavItem} ${
                    isActive ? styles.sidebarNavItemActive : ""
                  }`
            }
            onClick={() => navigate(item.path)}
          >
            <span className={styles.sidebarNavIcon}>{item.icon}</span>
            {!collapsed && <span>{item.label}</span>}
          </button>
        );

        return collapsed ? (
          <Tooltip
            key={item.key}
            title={item.label}
            placement="right"
            overlayInnerStyle={{
              background: "rgba(0,0,0,0.75)",
              color: "#fff",
            }}
          >
            {button}
          </Tooltip>
        ) : (
          button
        );
      })}
    </nav>
  );

  return (
    <Sider
      width={collapsed ? 72 : 240}
      className={`${styles.sider}${
        collapsed ? ` ${styles.siderCollapsed}` : ""
      }${isDark ? ` ${styles.siderDark}` : ""}`}
    >
      <div className={styles.sidebarScrollArea}>
        <AgentSelector collapsed={collapsed} />
        {renderNav()}
      </div>

      {authEnabled && !collapsed && (
        <div className={styles.authActions}>
          <Button
            type="text"
            icon={<SparkSearchUserLine size={16} />}
            onClick={() => {
              accountForm.resetFields();
              setAccountModalOpen(true);
            }}
            block
            className={`${styles.authBtn} ${
              collapsed ? styles.authBtnCollapsed : ""
            }`}
          >
            {!collapsed && t("account.title")}
          </Button>
          <Button
            type="text"
            icon={<SparkExitFullscreenLine size={16} />}
            onClick={() => {
              clearAuthToken();
              window.location.href = "/login";
            }}
            block
            className={`${styles.authBtn} ${
              collapsed ? styles.authBtnCollapsed : ""
            }`}
          >
            {!collapsed && t("login.logout")}
          </Button>
        </div>
      )}

      <div className={styles.collapseToggleContainer}>
        <Button
          type="text"
          icon={
            collapsed ? (
              <SparkMenuExpandLine size={20} />
            ) : (
              <SparkMenuFoldLine size={20} />
            )
          }
          onClick={() => setCollapsed(!collapsed)}
          className={styles.collapseToggle}
        />
      </div>

      {/* Personal Center — pinned to the absolute bottom of the sidebar */}
      {collapsed ? (
        <div className={styles.personalCenter}>
          <Dropdown
            placement="topRight"
            trigger={["click"]}
            menu={{
              items: personalCenterItems.map((it) => ({
                key: it.key,
                icon: it.icon,
                label: it.label,
                onClick: () => navigate(it.path),
              })),
              selectedKeys: personalCenterActive ? [selectedKey] : [],
            }}
          >
            <Tooltip
              title={t("nav.personalCenter")}
              placement="right"
              overlayInnerStyle={{
                background: "rgba(0,0,0,0.75)",
                color: "#fff",
              }}
            >
              <button
                className={`${styles.collapsedNavItem} ${
                  personalCenterActive ? styles.collapsedNavItemActive : ""
                }`}
              >
                <span className={styles.sidebarNavIcon}>
                  <SparkAccountManagementLine size={18} />
                </span>
              </button>
            </Tooltip>
          </Dropdown>
        </div>
      ) : (
        <div className={styles.personalCenter}>
          <button
            className={`${styles.sidebarNavItem} ${styles.personalCenterTrigger} ${
              personalCenterActive ? styles.sidebarNavItemActive : ""
            }`}
            onClick={() => setPersonalCenterOpen((v) => !v)}
            aria-expanded={personalCenterOpen}
          >
            <span className={styles.sidebarNavIcon}>
              <SparkAccountManagementLine size={18} />
            </span>
            <span style={{ flex: 1 }}>{t("nav.personalCenter")}</span>
            <ChevronDown
              size={14}
              className={`${styles.personalCenterChevron} ${
                personalCenterOpen ? styles.personalCenterChevronOpen : ""
              }`}
            />
          </button>
          {personalCenterOpen && (
            <div className={styles.personalCenterSubmenu}>
              {personalCenterItems.map((item) => {
                const isActive = selectedKey === item.key;
                return (
                  <button
                    key={item.key}
                    className={`${styles.sidebarNavItem} ${styles.personalCenterSubItem} ${
                      isActive ? styles.sidebarNavItemActive : ""
                    }`}
                    onClick={() => navigate(item.path)}
                  >
                    <span className={styles.sidebarNavIcon}>{item.icon}</span>
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      )}

      <Modal
        open={accountModalOpen}
        onCancel={() => setAccountModalOpen(false)}
        title={t("account.title")}
        footer={null}
        destroyOnHidden
        centered
      >
        <Form form={accountForm} layout="vertical" onFinish={handleUpdateProfile}>
          <Form.Item
            name="currentPassword"
            label={t("account.currentPassword")}
            rules={[
              { required: true, message: t("account.currentPasswordRequired") },
            ]}
          >
            <Input.Password />
          </Form.Item>
          <Form.Item name="newUsername" label={t("account.newUsername")}>
            <Input placeholder={t("account.newUsernamePlaceholder")} />
          </Form.Item>
          <Form.Item name="newPassword" label={t("account.newPassword")}>
            <Input.Password placeholder={t("account.newPasswordPlaceholder")} />
          </Form.Item>
          <Form.Item
            name="confirmPassword"
            label={t("account.confirmPassword")}
            dependencies={["newPassword"]}
            rules={[
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value && !getFieldValue("newPassword")) {
                    return Promise.resolve();
                  }
                  if (value === getFieldValue("newPassword")) {
                    return Promise.resolve();
                  }
                  return Promise.reject(
                    new Error(t("account.passwordMismatch")),
                  );
                },
              }),
            ]}
          >
            <Input.Password placeholder={t("account.confirmPasswordPlaceholder")} />
          </Form.Item>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={accountLoading}
              block
            >
              {t("account.save")}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </Sider>
  );
}
