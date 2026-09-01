# WPCodeBox snippets

Reference copies of the two snippets that run on the live site. **The site reads
from the WPCodeBox database table, not from these files** — they are here so the
code is version-controlled and reviewable.

| File | WPCodeBox snippet | What it does |
| --- | --- | --- |
| `../rf-stylesheet.css` | id 2 (CSS) | Tokenised stylesheet, 17 sections |
| `rf-related-loops.php` | id 3 (PHP) | Relationship-filtered loops, FAQ accordion behaviour, FAQPage schema, service gallery shortcode, explicit 301s |

## If you edit these files

Nothing happens automatically. Paste the change into WPCodeBox, or ask Claude to
push it. After any change to `_elementor_data` or these snippets, purge WP Engine
before verifying — a correct write still renders stale otherwise.

## Notes worth keeping

- The stylesheet's token layer is declared on `:root, body` deliberately.
  Elementor scopes its globals to `.elementor-kit-1368` on `<body>`, so a
  `:root`-only declaration never resolves them.
- Do not use `#FFFFFF` in the CSS. The WPCodeBox minifier mangles repeating-character
  hex values. Use the `white` keyword or an off-by-one value.
- Elementor's base CSS sets `.e-con::before { opacity: .5 }`. Any scrim applied
  through that pseudo-element renders at half strength unless you set
  `opacity: 1` — this cost three attempts on the 404 page.
