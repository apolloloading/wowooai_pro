import { getChannelIconUrl } from "./channelIcons";

interface ChannelIconProps {
  channelKey: string;
  size?: number;
}

/**
 * Lightweight channel icon used in places like the chat session list.
 *
 * Renders the CDN logo for a known channel key, falling back to the
 * "console" generic icon for unknown keys.  Kept as a separate component
 * so callers don't need to touch DOM `<img>` attributes.
 */
export function ChannelIcon({ channelKey, size = 16 }: ChannelIconProps) {
  return (
    <img
      src={getChannelIconUrl(channelKey)}
      alt={channelKey}
      width={size}
      height={size}
      style={{ display: "inline-block", verticalAlign: "middle" }}
    />
  );
}
