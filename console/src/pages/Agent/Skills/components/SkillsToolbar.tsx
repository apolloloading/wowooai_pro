import { Input } from "@agentscope-ai/design";
import { UnorderedListOutlined, AppstoreOutlined } from "@ant-design/icons";
import { useTranslation } from "react-i18next";
import styles from "../index.module.less";

interface SkillsToolbarProps {
  searchQuery: string;
  onSearchChange: (value: string) => void;
  viewMode: "card" | "list";
  onViewModeChange: (mode: "card" | "list") => void;
}

export function SkillsToolbar({
  searchQuery,
  onSearchChange,
  viewMode,
  onViewModeChange,
}: SkillsToolbarProps) {
  const { t } = useTranslation();

  return (
    <div className={styles.toolbar}>
      <div className={styles.searchContainer}>
        <Input
          className={styles.searchInput}
          placeholder={t("skills.searchPlaceholder")}
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>
      <div className={styles.toolbarRight}>
        <div className={styles.viewToggle}>
          <button
            className={`${styles.viewToggleBtn} ${
              viewMode === "list" ? styles.viewToggleBtnActive : ""
            }`}
            onClick={() => onViewModeChange("list")}
            title={t("skills.listView")}
          >
            <UnorderedListOutlined />
          </button>
          <button
            className={`${styles.viewToggleBtn} ${
              viewMode === "card" ? styles.viewToggleBtnActive : ""
            }`}
            onClick={() => onViewModeChange("card")}
            title={t("skills.gridView")}
          >
            <AppstoreOutlined />
          </button>
        </div>
      </div>
    </div>
  );
}
