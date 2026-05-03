import { useState, useEffect, useCallback } from "react";
import { Input, Switch, Spin, Empty, Tabs } from "antd";
import {
  BookOutlined,
  SearchOutlined,
  AppstoreOutlined,
  UnorderedListOutlined,
} from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import { PageHeader } from "@/components/PageHeader";
import { useAgentStore } from "@/stores/agentStore";
import { request } from "@/api";
import { invalidateSkillCache } from "@/api/modules/skill";
import type { SkillSpec } from "@/api/types";
import { useAppMessage } from "@/hooks/useAppMessage";
import styles from "./index.module.less";

function useKnowledgeSkills() {
  const [skills, setSkills] = useState<SkillSpec[]>([]);
  const [loading, setLoading] = useState(false);
  const { message } = useAppMessage();
  // Follow the currently selected agent — each agent owns its own knowledge base
  const { selectedAgent } = useAgentStore();

  const fetchSkills = useCallback(async () => {
    if (!selectedAgent) return;
    setLoading(true);
    try {
      const opts: RequestInit = {
        headers: new Headers({ "X-Agent-Id": selectedAgent }),
      };
      const data = await request<SkillSpec[]>("/skills", opts);
      // Only keep skills tagged as knowledge
      const knowledgeSkills = (data || []).filter(
        (s) => s.metadata_type === "knowledge",
      );
      setSkills(knowledgeSkills);
    } catch (err) {
      console.error("Failed to load knowledge skills", err);
      message.error("加载知识库失败");
    } finally {
      setLoading(false);
    }
  }, [selectedAgent]);

  useEffect(() => {
    fetchSkills();
  }, [fetchSkills]);

  const toggleEnabled = useCallback(
    async (skillName: string, enabled: boolean) => {
      if (!selectedAgent) return;
      try {
        const opts: RequestInit = {
          method: "POST",
          headers: new Headers({ "X-Agent-Id": selectedAgent }),
        };
        const action = enabled ? "enable" : "disable";
        await request<void>(
          `/skills/${encodeURIComponent(skillName)}/${action}`,
          opts,
        );
        invalidateSkillCache({ agentId: selectedAgent });
        setSkills((prev) =>
          prev.map((s) => (s.name === skillName ? { ...s, enabled } : s)),
        );
      } catch (err) {
        console.error("Failed to toggle knowledge skill", err);
        message.error("操作失败");
      }
    },
    [selectedAgent],
  );

  return { skills, loading, toggleEnabled };
}

interface KnowledgeCardProps {
  skill: SkillSpec;
  viewMode: "card" | "list";
  onToggle: (name: string, enabled: boolean) => void;
}

function KnowledgeCard({ skill, viewMode, onToggle }: KnowledgeCardProps) {
  const isEnterprise = skill.knowledge_type === "enterprise";
  const isMock = skill.source === "mock"; // 假数据不显示开关 / 状态徽标
  const displayName = skill.label || skill.name;

  if (viewMode === "list") {
    return (
      <div className={styles.knowledgeListItem}>
        <div className={styles.listItemLeft}>
          <div className={styles.listIcon}>
            <BookOutlined />
          </div>
          <div className={styles.listItemInfo}>
            <div className={styles.listItemHeader}>
              <span className={styles.listItemTitle}>{displayName}</span>
              {isEnterprise && (
                <span
                  className={`${styles.typeBadge} ${styles.enterpriseBadge}`}
                >
                  企业
                </span>
              )}
            </div>
            <p className={styles.listItemDesc}>{skill.description}</p>
          </div>
        </div>
        {!isMock && (
          <div className={styles.listItemRight}>
            <Switch
              size="small"
              checked={skill.enabled}
              onChange={(checked) => onToggle(skill.name, checked)}
            />
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={styles.knowledgeCard}>
      <div className={styles.cardTopRow}>
        <div className={styles.cardIcon}>
          <BookOutlined />
        </div>
        {!isMock && (
          <div className={styles.cardTopRight}>
            <span
              className={`${styles.statusBadge} ${
                skill.enabled ? styles.status_enabled : styles.status_disabled
              }`}
            >
              <span className={styles.statusDot} />
              {skill.enabled ? "已启用" : "已停用"}
            </span>
          </div>
        )}
      </div>

      <div className={styles.cardTitle}>{displayName}</div>
      <p className={styles.cardDesc}>{skill.description}</p>

      <div className={styles.cardMeta}>
        {isEnterprise && (
          <span className={`${styles.typeBadge} ${styles.enterpriseBadge}`}>
            企业知识库
          </span>
        )}
        {!isEnterprise && (
          <span className={styles.typeBadge}>个人知识库</span>
        )}
      </div>

      {!isMock && (
        <div className={styles.cardFooter}>
          <span style={{ fontSize: 12, color: "rgba(20,20,19,0.45)" }}>
            {skill.name}
          </span>
          <Switch
            size="small"
            checked={skill.enabled}
            onChange={(checked) => onToggle(skill.name, checked)}
          />
        </div>
      )}
    </div>
  );
}

interface SkillListProps {
  skills: SkillSpec[];
  loading: boolean;
  viewMode: "card" | "list";
  searchQuery: string;
  onToggle: (name: string, enabled: boolean) => void;
  emptyTitle?: string;
  emptyHint?: string;
}

function KnowledgeList({
  skills,
  loading,
  viewMode,
  searchQuery,
  onToggle,
  emptyTitle,
  emptyHint,
}: SkillListProps) {
  const filtered = searchQuery
    ? skills.filter(
        (s) =>
          s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          (s.label ?? "").toLowerCase().includes(searchQuery.toLowerCase()) ||
          (s.description ?? "")
            .toLowerCase()
            .includes(searchQuery.toLowerCase()),
      )
    : skills;

  if (loading) {
    return (
      <div className={styles.emptyState}>
        <Spin size="large" />
      </div>
    );
  }

  if (filtered.length === 0) {
    return (
      <div className={styles.emptyState}>
        <Empty
          description={
            searchQuery ? (
              <span className={styles.emptyStateText}>
                未找到匹配的知识库
              </span>
            ) : (
              <div>
                <p className={styles.emptyStateTitle}>
                  {emptyTitle ?? "暂无知识库"}
                </p>
                <p className={styles.emptyStateText}>
                  {emptyHint ?? "知识库将在数字员工启动时自动加载"}
                </p>
              </div>
            )
          }
        />
      </div>
    );
  }

  if (viewMode === "card") {
    return (
      <div className={styles.knowledgeGrid}>
        {filtered.map((skill) => (
          <KnowledgeCard
            key={skill.name}
            skill={skill}
            viewMode="card"
            onToggle={onToggle}
          />
        ))}
      </div>
    );
  }

  return (
    <div className={styles.knowledgeList}>
      {filtered.map((skill) => (
        <KnowledgeCard
          key={skill.name}
          skill={skill}
          viewMode="list"
          onToggle={onToggle}
        />
      ))}
    </div>
  );
}

// （已移除占位 mock 数据：现在「我的知识库」由后端真实加载，例如内置的
// `onboarding-guide` 入职指引。如果后续需要新的默认知识库，建议在
// `src/wowooai/agents/skills/<name>-zh|-en/` 下添加 SKILL.md，并在
// `src/wowooai/app/migration.py:_DEFAULT_KNOWLEDGE_SKILL_NAMES` 中登记。）

export default function KnowledgePage() {
  const { t } = useTranslation();
  const { skills, loading, toggleEnabled } = useKnowledgeSkills();
  const { selectedAgent } = useAgentStore();
  const [activeTab, setActiveTab] = useState("personal");
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState<"card" | "list">("card");

  // Reset tab to personal whenever the selected agent changes
  useEffect(() => {
    setActiveTab("personal");
    setSearchQuery("");
  }, [selectedAgent]);

  // 我的知识库：仅展示真实数据（由后端按 metadata_type === "knowledge" 返回）
  const personalSkills = skills.filter(
    (s) => s.knowledge_type !== "enterprise",
  );
  // 企业知识库：仅展示真实数据（暂未上线，目前为筹备中占位）
  const enterpriseSkills = skills.filter(
    (s) => s.knowledge_type === "enterprise",
  );

  return (
    <div className={styles.knowledgePage}>
      <PageHeader items={[{ title: t("nav.knowledge") }]} />

      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        style={{ padding: "0 16px" }}
        items={[
          {
            key: "personal",
            label: `我的知识库${
              personalSkills.length > 0 ? ` (${personalSkills.length})` : ""
            }`,
          },
          {
            key: "enterprise",
            label: `企业知识库${
              enterpriseSkills.length > 0
                ? ` (${enterpriseSkills.length})`
                : ""
            }`,
          },
        ]}
      />

      <div className={styles.toolbar}>
        <Input
          prefix={<SearchOutlined style={{ color: "rgba(0,0,0,0.25)" }} />}
          placeholder="搜索知识库..."
          className={styles.searchInput}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          allowClear
        />
        <div className={styles.toolbarRight}>
          <div className={styles.viewToggle}>
            <button
              className={`${styles.viewToggleBtn} ${
                viewMode === "card" ? styles.viewToggleBtnActive : ""
              }`}
              onClick={() => setViewMode("card")}
              title="卡片视图"
            >
              <AppstoreOutlined />
            </button>
            <button
              className={`${styles.viewToggleBtn} ${
                viewMode === "list" ? styles.viewToggleBtnActive : ""
              }`}
              onClick={() => setViewMode("list")}
              title="列表视图"
            >
              <UnorderedListOutlined />
            </button>
          </div>
        </div>
      </div>

      <div className={styles.tabContent}>
        {activeTab === "personal" && (
          <KnowledgeList
            skills={personalSkills}
            loading={loading}
            viewMode={viewMode}
            searchQuery={searchQuery}
            onToggle={toggleEnabled}
          />
        )}
        {activeTab === "enterprise" && (
          <KnowledgeList
            skills={enterpriseSkills}
            loading={loading}
            viewMode={viewMode}
            searchQuery={searchQuery}
            onToggle={toggleEnabled}
            emptyTitle="敬请期待"
            emptyHint="企业知识库正在筹备中，将在后续版本推出"
          />
        )}
      </div>
    </div>
  );
}
