Use `Card` for package tiers, event-type tiles and testimonials — 12px radius, hairline border, whisper-soft shadow.

```jsx
<Card eyebrow="Package" title="The Clubhouse" featured
      footer={<Button fullWidth>Get a quote</Button>}>
  Full simulator setup, on-site attendant, and four hours of play.
</Card>
```

- `variant="surface"` on white sections; `variant="default"` on ivory sections — cards and their background never match.
- `featured` marks exactly one package per grid.
- Media wells are 16:10 and always contain people-forward photography.
