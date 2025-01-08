import { formatDistance } from "date-fns";
import {
  AntAvatar as Avatar,
  AntFlex as Flex,
  AntList as List,
  AntListItemProps as ListItemProps,
  AntSkeleton as Skeleton,
  AntTooltip as Tooltip,
  AntTypography as Typography,
  Icons,
} from "fidesui";
import NextLink from "next/link";

import { ACTION_CENTER_ROUTE } from "~/features/common/nav/v2/routes";
import { formatDate, getWebsiteIconUrl } from "~/features/common/utils";

import { MonitorSummary } from "./types";

const { Text } = Typography;

interface MonitorResultProps extends ListItemProps {
  monitorSummary: MonitorSummary;
  showSkeleton?: boolean;
}

export const MonitorResult = ({
  monitorSummary,
  showSkeleton,
  ...props
}: MonitorResultProps) => {
  if (!monitorSummary) {
    return null;
  }

  const {
    name,
    property,
    total_updates: totalUpdates,
    updates,
    last_monitored: lastMonitored,
    warning,
    key,
  } = monitorSummary;

  const assetCountString = Object.entries(updates)
    .map((update) => {
      return `${update[1]} ${update[0]}s`;
    })
    .join(", ");

  const lastMonitoredDistance = lastMonitored
    ? formatDistance(new Date(lastMonitored), new Date(), {
        addSuffix: true,
      })
    : undefined;

  const iconUrl = property ? getWebsiteIconUrl(property) : undefined;

  return (
    <List.Item data-testid={`monitor-result-${key}`} {...props}>
      <Skeleton avatar title={false} loading={showSkeleton} active>
        <List.Item.Meta
          avatar={!!iconUrl && <Avatar src={iconUrl} size="small" />}
          title={
            <NextLink
              href={`${ACTION_CENTER_ROUTE}/${key}`}
              className="whitespace-nowrap"
            >
              {`${totalUpdates} assets detected${property ? `on ${property}` : ""}`}
              {!!warning && (
                <Tooltip
                  title={typeof warning === "string" ? warning : undefined}
                >
                  <Icons.WarningAltFilled
                    className="ml-1 inline-block align-middle"
                    style={{ color: "var(--fidesui-error)" }}
                  />
                </Tooltip>
              )}
            </NextLink>
          }
          description={`${assetCountString} detected.`}
        />
        <Flex className="gap-12">
          <Text style={{ maxWidth: 300 }} ellipsis={{ tooltip: name }}>
            {name}
          </Text>
          {!!lastMonitoredDistance && (
            <Tooltip title={formatDate(lastMonitored)}>
              <Text data-testid="monitor-date">{lastMonitoredDistance}</Text>
            </Tooltip>
          )}
        </Flex>
      </Skeleton>
    </List.Item>
  );
};
