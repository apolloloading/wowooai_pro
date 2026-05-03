import { Suspense, useEffect, useState } from "react";
import { Tabs, Spin, Empty, Card } from "antd";
import { useSearchParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { PageHeader } from "../../components/PageHeader";
import { lazyImportWithRetry } from "../../utils/lazyWithRetry";
import TokenUsageEmbed from "./TokenUsageEmbed";
import ToolExecutionSecurity from "./ToolExecutionSecurity";

// Reuse existing pages as inner panels.
// Path is normalised by lazyImportWithRetry — only the segment after
// the first "pages/" is used to look up the glob map, so we keep the
// canonical "<...>/pages/<...>" form here.
const ModelsPage = lazyImportWithRetry("../../pages/Settings/Models");
const MCPPage = lazyImportWithRetry("../../pages/Agent/MCP");
const ToolsPage = lazyImportWithRetry("../../pages/Agent/Tools");

type TopTab = "profile" | "account-security";
type SubTab = "security" | "models" | "mcp" | "tools";

const VALID_TOP: TopTab[] = ["profile", "account-security"];
const VALID_SUB: SubTab[] = ["security", "models", "mcp", "tools"];

function isTopTab(v: string | null): v is TopTab {
  return v !== null && (VALID_TOP as string[]).includes(v);
}
function isSubTab(v: string | null): v is SubTab {
  return v !== null && (VALID_SUB as string[]).includes(v);
}

export default function PersonalCenterPage() {
  const { t } = useTranslation();
  const [params, setParams] = useSearchParams();

  const [topTab, setTopTab] = useState<TopTab>(() => {
    const v = params.get("tab");
    return isTopTab(v) ? v : "profile";
  });

  const [subTab, setSubTab] = useState<SubTab>(() => {
    const v = params.get("sub");
    return isSubTab(v) ? v : "security";
  });

  // Keep URL in sync without reloading
  useEffect(() => {
    const next = new URLSearchParams(params);
    next.set("tab", topTab);
    if (topTab === "account-security") {
      next.set("sub", subTab);
    } else {
      next.delete("sub");
    }
    if (next.toString() !== params.toString()) {
      setParams(next, { replace: true });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topTab, subTab]);

  const accountSecuritySubTabs = [
    {
      key: "security",
      label: t("personalCenter.tabs.security"),
      children: (
        <Suspense
          fallback={<Spin style={{ display: "block", margin: "40px auto" }} />}
        >
          <ToolExecutionSecurity />
        </Suspense>
      ),
    },
    {
      key: "models",
      label: t("personalCenter.tabs.models"),
      children: (
        <Suspense
          fallback={<Spin style={{ display: "block", margin: "40px auto" }} />}
        >
          <ModelsPage />
        </Suspense>
      ),
    },
    {
      key: "mcp",
      label: t("personalCenter.tabs.mcp"),
      children: (
        <Suspense
          fallback={<Spin style={{ display: "block", margin: "40px auto" }} />}
        >
          <MCPPage />
        </Suspense>
      ),
    },
    {
      key: "tools",
      label: t("personalCenter.tabs.tools"),
      children: (
        <Suspense
          fallback={<Spin style={{ display: "block", margin: "40px auto" }} />}
        >
          <ToolsPage />
        </Suspense>
      ),
    },
  ];

  const topTabItems = [
    {
      key: "profile",
      label: t("personalCenter.tabs.profile"),
      children: (
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Card title={t("personalCenter.profile.title")}>
            <Empty description={t("personalCenter.profile.placeholder")} />
          </Card>
          <Card title={t("personalCenter.profile.tokenUsage")}>
            <Suspense
              fallback={
                <Spin style={{ display: "block", margin: "40px auto" }} />
              }
            >
              <TokenUsageEmbed />
            </Suspense>
          </Card>
        </div>
      ),
    },
    {
      key: "account-security",
      label: t("personalCenter.tabs.accountSecurity"),
      children: (
        <Tabs
          activeKey={subTab}
          onChange={(k) => setSubTab(k as SubTab)}
          items={accountSecuritySubTabs}
        />
      ),
    },
  ];

  return (
    <div style={{ padding: "0 0 24px" }}>
      <PageHeader items={[{ title: t("nav.personalCenter") }]} />
      <div style={{ padding: "0 24px" }}>
        <Tabs
          activeKey={topTab}
          onChange={(k) => setTopTab(k as TopTab)}
          items={topTabItems}
          style={{ marginTop: 8 }}
        />
      </div>
    </div>
  );
}
