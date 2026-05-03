/**
 * Personal Center → 安全（工具守卫精简版）。
 * 只展示工具守卫核心：开关 + 受保护工具 / 禁止工具 + 规则表格。
 */
import { useState, useCallback } from "react";
import { Form, Switch, Button, Card, Select } from "@agentscope-ai/design";
import { PlusCircleOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import api from "../../api";
import { useAppMessage } from "../../hooks/useAppMessage";
import {
  useToolGuard,
  type MergedRule,
} from "../Settings/Security/useToolGuard";
import {
  RuleTable,
  RuleModal,
  PreviewModal,
} from "../Settings/Security/components";
import styles from "../Settings/Security/index.module.less";

const BUILTIN_TOOLS = [
  "execute_shell_command",
  "execute_python_code",
  "browser_use",
  "desktop_screenshot",
  "view_image",
  "read_file",
  "write_file",
  "edit_file",
  "append_file",
  "view_text_file",
  "write_text_file",
  "send_file_to_user",
];

export default function ToolGuardOnly() {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const [editForm] = Form.useForm();
  const [saving, setSaving] = useState(false);
  const {
    config,
    customRules,
    builtinRules,
    enabled,
    setEnabled,
    mergedRules,
    loading,
    error,
    fetchAll,
    toggleRule,
    deleteCustomRule,
    addCustomRule,
    updateCustomRule,
    buildSaveBody,
  } = useToolGuard();

  const [editModal, setEditModal] = useState(false);
  const [editingRule, setEditingRule] = useState<MergedRule | null>(null);
  const [previewRule, setPreviewRule] = useState<MergedRule | null>(null);
  const { message } = useAppMessage();

  const handleSave = useCallback(async () => {
    try {
      setSaving(true);
      const values = await form.validateFields();
      const guardedTools: string[] = values.guarded_tools ?? [];
      const body = {
        enabled: values.enabled,
        guarded_tools: guardedTools.length > 0 ? guardedTools : null,
        denied_tools: values.denied_tools ?? [],
        custom_rules: customRules,
        disabled_rules: Array.from(buildSaveBody().disabled_rules),
        shell_evasion_checks: config?.shell_evasion_checks ?? {},
      };
      await api.updateToolGuard(body);
      setEnabled(body.enabled);
      message.success(t("security.saveSuccess"));
    } catch (err) {
      if (err instanceof Error && "errorFields" in err) return;
      message.error(
        err instanceof Error ? err.message : t("security.saveFailed"),
      );
    } finally {
      setSaving(false);
    }
  }, [customRules, buildSaveBody, form, t, message, setEnabled]);

  const openAddRule = useCallback(() => {
    setEditingRule(null);
    editForm.resetFields();
    editForm.setFieldsValue({
      severity: "HIGH",
      category: "command_injection",
      tools: [],
      params: [],
      patterns: "",
      exclude_patterns: "",
    });
    setEditModal(true);
  }, [editForm]);

  const openEditRule = useCallback(
    (rule: MergedRule) => {
      setEditingRule(rule);
      editForm.setFieldsValue({
        ...rule,
        patterns: rule.patterns.join("\n"),
        exclude_patterns: rule.exclude_patterns.join("\n"),
      });
      setEditModal(true);
    },
    [editForm],
  );

  const handleEditSave = useCallback(async () => {
    try {
      const values = await editForm.validateFields();
      const patterns = (values.patterns as string)
        .split("\n")
        .map((s: string) => s.trim())
        .filter(Boolean);
      const excludePatterns = ((values.exclude_patterns as string) || "")
        .split("\n")
        .map((s: string) => s.trim())
        .filter(Boolean);
      const rule = {
        id: values.id,
        tools: values.tools ?? [],
        params: values.params ?? [],
        category: values.category,
        severity: values.severity,
        patterns,
        exclude_patterns: excludePatterns,
        description: values.description || "",
        remediation: values.remediation || "",
      };
      if (editingRule) {
        updateCustomRule(editingRule.id, rule);
      } else {
        const allIds = [
          ...builtinRules.map((r) => r.id),
          ...customRules.map((r) => r.id),
        ];
        if (allIds.includes(rule.id)) {
          message.error(t("security.rules.duplicateId"));
          return;
        }
        addCustomRule(rule);
      }
      setEditModal(false);
    } catch {
      /* validation */
    }
  }, [
    editingRule,
    builtinRules,
    customRules,
    updateCustomRule,
    addCustomRule,
    editForm,
    t,
    message,
  ]);

  const toolOptions = BUILTIN_TOOLS.map((name) => ({
    label: name,
    value: name,
  }));

  if (loading) {
    return (
      <div style={{ padding: 24 }}>
        <span>{t("common.loading")}</span>
      </div>
    );
  }
  if (error) {
    return (
      <div style={{ padding: 24 }}>
        <span style={{ color: "red" }}>{error}</span>
        <Button
          size="small"
          onClick={fetchAll}
          style={{ marginLeft: 12 }}
        >
          {t("environments.retry")}
        </Button>
      </div>
    );
  }

  return (
    <div className={styles.securityPage} style={{ padding: 0 }}>
      <p className={styles.tabDescription} style={{ marginBottom: 16 }}>
        {t("security.toolGuardDescription")}
      </p>

      <Card className={styles.formCard}>
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            enabled: config?.enabled ?? true,
            guarded_tools: config?.guarded_tools ?? [],
            denied_tools: config?.denied_tools ?? [],
          }}
        >
          <Form.Item
            label={t("security.enabled")}
            name="enabled"
            valuePropName="checked"
            tooltip={t("security.enabledTooltip")}
          >
            <Switch onChange={(val) => setEnabled(val)} />
          </Form.Item>
          <div className={styles.toolGuardRow}>
            <Form.Item
              label={t("security.guardedTools")}
              name="guarded_tools"
              tooltip={t("security.guardedToolsTooltip")}
              style={{ marginBottom: 0 }}
            >
              <Select
                mode="tags"
                options={toolOptions}
                placeholder={t("security.guardedToolsPlaceholder")}
                disabled={!enabled}
                allowClear
                style={{ width: "100%" }}
              />
            </Form.Item>
            <Form.Item
              label={t("security.deniedTools")}
              name="denied_tools"
              tooltip={t("security.deniedToolsTooltip")}
              style={{ marginBottom: 0 }}
            >
              <Select
                mode="tags"
                options={toolOptions}
                placeholder={t("security.deniedToolsPlaceholder")}
                disabled={!enabled}
                allowClear
                style={{ width: "100%" }}
              />
            </Form.Item>
          </div>
        </Form>
      </Card>

      <div className={styles.sectionContainer} style={{ marginTop: 16 }}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>{t("security.rules.title")}</h2>
          <Button
            type="primary"
            icon={<PlusCircleOutlined />}
            onClick={openAddRule}
            disabled={!enabled}
            size="middle"
          >
            {t("security.rules.add")}
          </Button>
        </div>
        <Card className={styles.tableCard}>
          <RuleTable
            rules={mergedRules}
            enabled={enabled}
            onToggleRule={toggleRule}
            onPreviewRule={setPreviewRule}
            onEditRule={openEditRule}
            onDeleteRule={deleteCustomRule}
          />
        </Card>
      </div>

      <div
        className={styles.footerButtons}
        style={{ position: "static", marginTop: 16 }}
      >
        <Button
          onClick={() => {
            form.resetFields();
            fetchAll();
          }}
          disabled={saving}
          style={{ marginRight: 8 }}
        >
          {t("common.reset")}
        </Button>
        <Button type="primary" onClick={handleSave} loading={saving}>
          {t("common.save")}
        </Button>
      </div>

      <RuleModal
        open={editModal}
        editingRule={editingRule}
        existingRuleIds={[
          ...builtinRules.map((r) => r.id),
          ...customRules.map((r) => r.id),
        ]}
        onOk={handleEditSave}
        onCancel={() => setEditModal(false)}
        form={editForm}
      />
      <PreviewModal rule={previewRule} onClose={() => setPreviewRule(null)} />
    </div>
  );
}
