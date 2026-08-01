import * as React from 'react';

/**
 * Page section wrapper: background skin, 1200px container, and the standard
 * eyebrow / heading / lead header block.
 */
export interface SectionProps {
  /** Background skin. Alternate `default` and `surface` down a page. */
  variant?: 'default' | 'surface' | 'subtle' | 'inverse' | 'brand';
  /** Small uppercase kicker above the heading. */
  eyebrow?: string;
  heading?: React.ReactNode;
  /** Intro paragraph, capped at the reading measure. */
  lead?: React.ReactNode;
  align?: 'left' | 'center';
  /** Use the tighter 64px vertical rhythm. */
  tight?: boolean;
  /** Container max-width override, e.g. `var(--container-narrow)`. */
  width?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}

export declare function Section(props: SectionProps): JSX.Element;
