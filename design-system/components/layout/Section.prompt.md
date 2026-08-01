Use `Section` for every band of a page — it owns the vertical rhythm (96px) and the 1200px container.

```jsx
<Section variant="surface" eyebrow="Packages" heading="Pick your tier" align="center"
         lead="Every package includes delivery, setup and breakdown.">
  <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'var(--space-3)'}}>…</div>
</Section>
```

- Alternate `default` (white) and `surface` (ivory); use `inverse` once per page at most.
- Headings are Cormorant Garamond semibold with 1px tracking; eyebrows are uppercase 12px with .18em tracking.
