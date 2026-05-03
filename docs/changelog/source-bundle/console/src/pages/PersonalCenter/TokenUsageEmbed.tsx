import { lazy } from "react";

// Lazy-load Token Usage page so we don't bring in its bundle
// when the user only views Profile.
const TokenUsagePage = lazy(() => import("../Settings/TokenUsage"));

export default function TokenUsageEmbed() {
  return <TokenUsagePage />;
}
