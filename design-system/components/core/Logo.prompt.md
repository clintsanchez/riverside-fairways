Use `Logo` anywhere the mark appears — header, footer, email header, slide corners. It loads the real PNG from `assets/`; never approximate the script wordmark in type.

```jsx
<Logo height={72} />
<Logo variant="reversed" height={56} />
<Logo variant="icon" height={40} />
```

- `reversed` (white) on Primary or Dark Green; `primary` on white and ivory; `mono` for black-and-white print.
- `icon` is the golf flag alone — avatars, favicons, 120px minimum.
- Clear space equals the flag height on all sides.
