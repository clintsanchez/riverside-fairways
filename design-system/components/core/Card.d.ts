import * as React from 'react';

/**
 * Media + body container used for packages, event types and testimonials.
 */
export interface CardProps {
  /** Surface treatment. `inverse` sits on dark green sections. */
  variant?: 'default' | 'surface' | 'elevated' | 'inverse';
  /** Image or video node rendered in a 16:10 media well. */
  media?: React.ReactNode;
  /** Small uppercase label above the title. */
  eyebrow?: string;
  title?: React.ReactNode;
  /** Actions pinned to the bottom of the card. */
  footer?: React.ReactNode;
  /** Adds a 2px green border — use for the recommended package only. */
  featured?: boolean;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}

export declare function Card(props: CardProps): JSX.Element;
