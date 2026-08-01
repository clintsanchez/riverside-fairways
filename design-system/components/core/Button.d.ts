import * as React from 'react';

/**
 * Primary call-to-action control. Filled green is the default; outline is the
 * quiet partner on light surfaces; reversed sits on photography and green fills.
 */
export interface ButtonProps {
  /** Visual treatment. */
  variant?: 'primary' | 'outline' | 'ghost' | 'reversed';
  /** Control height. `lg` is the hero CTA size. */
  size?: 'sm' | 'md' | 'lg';
  /** Render as an anchor instead of a button. */
  href?: string;
  disabled?: boolean;
  /** Stretch to the container width (mobile CTAs, form submits). */
  fullWidth?: boolean;
  /** Optional leading glyph, usually an <img> from assets/. */
  icon?: React.ReactNode;
  onClick?: (e: React.MouseEvent) => void;
  type?: 'button' | 'submit' | 'reset';
  style?: React.CSSProperties;
  children?: React.ReactNode;
}

export declare function Button(props: ButtonProps): JSX.Element;
