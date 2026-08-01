Use `Hero` once per page, at the very top.

```jsx
<Hero image="assets/hero.jpg" eyebrow="Mobile golf simulator"
      headline="We bring the fairway to you"
      subhead="Anywhere with electricity, in a few hours."
      actions={<><Button size="lg" variant="reversed">Get a quote</Button><Button size="lg" variant="outline" style={{color:'var(--rf-white)',borderColor:'var(--rf-white)'}}>See packages</Button></>}
      trust={['Fully mobile','No golf experience needed','Louisiana & the Gulf Coast']} />
```

- Photography always carries the Primary Green 40% overlay plus the bottom scrim — never place white text on a bare photo.
- The leading hero CTA is always `variant="reversed"` (white fill) — a primary green button disappears against the green overlay and the brand gradient. The secondary is an outline in white.
- Headline is display serif at weight 300 with 2px tracking; keep it under 16 characters per line.
