import * as React from 'react';

/**
 * Renders an approved Riverside Fairways logo file. Never re-draw the mark.
 */
export interface LogoProps {
  /** Which approved lockup to render. */
  variant?: 'primary' | 'reversed' | 'ivory' | 'mono' | 'icon' | 'icon-reversed';
  /** Rendered height in px. Full lockup minimum is 120px wide. */
  height?: number;
  /** Path to the copied assets folder, relative to the consuming page. */
  basePath?: string;
  style?: React.CSSProperties;
}

export declare function Logo(props: LogoProps): JSX.Element;
