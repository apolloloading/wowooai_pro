import { type ReactNode } from "react";
import styles from "./index.module.less";

export type PageHeaderBreadcrumbItem = {
  title: ReactNode;
};

export interface PageHeaderProps {
  items?: PageHeaderBreadcrumbItem[];
  parent?: ReactNode;
  current?: ReactNode;
  center?: ReactNode;
  extra?: ReactNode;
  afterBreadcrumb?: ReactNode;
  subRow?: ReactNode;
  className?: string;
}

export function PageHeader({
  center,
  extra,
  afterBreadcrumb,
  subRow,
  className,
}: PageHeaderProps) {
  const hasLeading = afterBreadcrumb != null || subRow != null;
  return (
    <div className={`${styles.pageHeader} ${className ?? ""}`.trim()}>
      {hasLeading ? (
        <div className={styles.leading}>
          {afterBreadcrumb ? (
            <div className={styles.leadingTop}>{afterBreadcrumb}</div>
          ) : null}
          {subRow}
        </div>
      ) : null}
      {center ? <div className={styles.center}>{center}</div> : null}
      {extra ? <div className={styles.extra}>{extra}</div> : null}
    </div>
  );
}
