import * as React from 'react';

export interface SiteHeaderNavItem { id: string; label: string }

/**
 * Marketing site header: logo lockup, uppercase nav, click-to-call and a quote CTA.
 */
export interface SiteHeaderProps {
  nav?: SiteHeaderNavItem[];
  /** Id of the current page — underlined in green. */
  active?: string;
  onNavigate?: (id: string) => void;
  /** Click-to-call number, displayed verbatim. */
  phone?: string;
  cta?: { label: string; onClick?: () => void };
  basePath?: string;
  /** Overlay the header on a hero: white logo, hairline rule, reversed CTA. */
  transparent?: boolean;
  style?: React.CSSProperties;
}

export declare function SiteHeader(props: SiteHeaderProps): JSX.Element;
