import { Card } from "@agentscope-ai/design";
import { useTranslation } from "react-i18next";
import React, { useState } from "react";
import { ChannelIcon } from "./ChannelIcon";
import { getChannelLabel, type ChannelKey } from "./constants";
import styles from "../index.module.less";

interface ChannelCardProps {
  channelKey: ChannelKey;
  config: Record<string, unknown>;
  onClick: () => void;
}

export const ChannelCard = React.memo(function ChannelCard({
  channelKey,
  config,
  onClick,
}: ChannelCardProps) {
  const { t } = useTranslation();
  const [isHover, setIsHover] = useState(false);
  const enabled = Boolean(config.enabled);
  const label = getChannelLabel(channelKey, t);

  const getChannelIcon = () => (
    <ChannelIcon channelKey={channelKey} size={32} />
  );

  const getCardClassNames = () => {
    if (isHover) return `${styles.channelCard} ${styles.hover}`;
    if (enabled) return `${styles.channelCard} ${styles.enabled}`;
    return `${styles.channelCard} ${styles.normal}`;
  };

  return (
    <Card
      hoverable
      onClick={onClick}
      onMouseEnter={() => setIsHover(true)}
      onMouseLeave={() => setIsHover(false)}
      className={getCardClassNames()}
      bodyStyle={{ padding: 12 }}
    >
      <div className={styles.cardRow}>
        <div className={styles.channelIcon}>{getChannelIcon()}</div>
        <div className={styles.cardTitle}>{label}</div>
        <div className={styles.statusIndicator}>
          <div
            className={`${styles.statusDot} ${
              enabled ? styles.enabled : styles.disabled
            }`}
          />
          <span
            className={`${styles.statusText} ${
              enabled ? styles.enabled : styles.disabled
            }`}
          >
            {enabled ? t("common.enabled") : t("common.disabled")}
          </span>
        </div>
      </div>
    </Card>
  );
});
