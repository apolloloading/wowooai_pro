import { useState, useEffect, useCallback } from "react";
import api from "../../../api";
import type { ProviderInfo, ActiveModelsInfo } from "../../../api/types";
import { useAgentStore } from "../../../stores/agentStore";

/**
 * Provider IDs hidden from the UI per product spec 02-前端界面重构.
 * Backend still ships these providers; we only hide their entry from
 * the model list so future product decisions can re-enable them
 * without touching the backend.
 */
const HIDDEN_PROVIDER_IDS: ReadonlySet<string> = new Set([
  "ollama",
  "lmstudio",
  "modelscope",
  "azure-openai",
  "openrouter",
  "opencode",
  "siliconflow-cn",
  "siliconflow-intl",
  "zhipu-cn",
  "zhipu-cn-codingplan",
  "zhipu-intl",
  "zhipu-intl-codingplan",
]);

/**
 * Whether local-model providers (is_local=true) are hidden in the UI.
 * Per product spec the wowooai release does not expose local providers.
 */
const HIDE_LOCAL_PROVIDERS = true;

function isProviderVisible(p: ProviderInfo): boolean {
  if (HIDDEN_PROVIDER_IDS.has(p.id)) return false;
  if (HIDE_LOCAL_PROVIDERS && p.is_local) return false;
  return true;
}

export function useProviders() {
  const [providers, setProviders] = useState<ProviderInfo[]>([]);
  const [activeModels, setActiveModels] = useState<ActiveModelsInfo | null>(
    null,
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { selectedAgent } = useAgentStore();

  const fetchAll = useCallback(async (showLoading = true) => {
    if (showLoading) {
      setLoading(true);
    }
    setError(null);
    try {
      const [provData, activeData] = await Promise.all([
        api.listProviders(),
        api.getActiveModels({ scope: "global" }),
      ]);
      if (!Array.isArray(provData)) {
        throw new Error(
          "Unexpected API response. Is VITE_API_BASE_URL configured correctly?",
        );
      }
      setProviders(provData.filter(isProviderVisible));
      if (activeData) setActiveModels(activeData);
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Failed to load provider data";
      console.error("Failed to load providers:", err);
      setError(msg);
    } finally {
      if (showLoading) {
        setLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    fetchAll();
  }, [fetchAll, selectedAgent]);

  return {
    providers,
    activeModels,
    loading,
    error,
    fetchAll,
  };
}
