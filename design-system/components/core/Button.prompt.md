Use `Button` for every call to action — quote requests, package selection, click-to-call.

```jsx
<Button size="lg" href="#quote">Get a quote</Button>
<Button variant="outline">See packages</Button>
<Button variant="reversed" size="lg">Reserve your date</Button>
```

- `variant`: `primary` (filled green) · `outline` (green rule, fills on hover) · `ghost` (nav/tertiary) · `reversed` (white on green or photography).
- `size`: `sm` 38px · `md` 44px (minimum tap target) · `lg` 52px for hero CTAs.
- Hover lightens to `--action-primary-hover`; there is no scale or shadow transform in this brand.
- Copy is sentence case and action-led: "Get a quote", "Reserve your date". Never all caps.
