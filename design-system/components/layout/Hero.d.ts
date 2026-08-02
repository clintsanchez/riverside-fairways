import * as React from 'react';

/**
 * Full-bleed page opener: photography under the green overlay, headline,
 * subhead, CTA pair and a trust strip.
 */
export interface HeroProps {
  eyebrow?: string;
  headline?: React.ReactNode;
  subhead?: React.ReactNode;
  /** Background photograph URL. Omitted renders the brand gradient. */
  image?: string;
  /** Button nodes — primary first, reversed/outline second. */
  actions?: React.ReactNode;
  /** Short uppercase proof points shown along the bottom. */
  trust?: string[];
  /** Minimum height in px. */
  height?: number;
  style?: React.CSSProperties;
}

export declare function Hero(props: HeroProps): JSX.Element;
