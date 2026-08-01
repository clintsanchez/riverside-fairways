import * as React from 'react';

export interface SiteFooterColumn { title: string; links: { label: string; href?: string }[] }

/**
 * Dark green site footer: ivory logo, tagline, link columns and contact row.
 */
export interface SiteFooterProps {
  columns?: SiteFooterColumn[];
  phone?: string;
  email?: string;
  /** One-line service-area sentence. */
  serviceArea?: string;
  social?: { label: string; href: string }[];
  tagline?: string;
  basePath?: string;
  style?: React.CSSProperties;
}

export declare function SiteFooter(props: SiteFooterProps): JSX.Element;
