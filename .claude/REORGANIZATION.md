# Claude Project Folder Reorganization — 2026-08-01

## Summary
Riverside Fairways Claude project items have been successfully reorganized into a dedicated `.claude/` folder within the project root.

## What was moved
- `CLAUDE.md` → `.claude/CLAUDE.md`
- `HANDOFF.md` → `.claude/HANDOFF.md`

## Folder structure created
```
Riverside Fairways/
├── .claude/
│   ├── CLAUDE.md          (project instructions)
│   ├── HANDOFF.md         (work-in-progress handoff)
│   ├── memory/            (project-specific memory)
│   └── settings/          (project-specific settings)
├── .agents/
├── .env.example
├── .gitignore
├── .mcp.json
├── 00-Client-Brief.md
├── 06-Reports/
├── DESIGN.md
├── README.md
├── aib/
├── brand-style-guide.md
├── brand/
└── website/
```

## Updates made to documents

### CLAUDE.md
Updated all relative paths to account for `.claude/` location:
- `.agents/product-marketing.md` → `../.agents/product-marketing.md`
- `00-Client-Brief.md` → `../00-Client-Brief.md`
- `brand/` → `../brand/`
- `DESIGN.md` → `../DESIGN.md`
- `website/css-tokens.css` → `../website/css-tokens.css`
- `brand-style-guide.md` → `../brand-style-guide.md`
- `06-Reports/records-check.md` → `../06-Reports/records-check.md`
- `.env` → `../.env`
- `.env.example` → `../.env.example`
- `.mcp.json` → `../.mcp.json`
- `CREDENTIALS.local.md` → `../CREDENTIALS.local.md`

### HANDOFF.md
Updated all relative paths:
- `CREDENTIALS.local.md` → `../CREDENTIALS.local.md`
- `06-Reports/records-check.md` → `../06-Reports/records-check.md`
- `brand/` → `../brand/`
- `DESIGN.md` → `../DESIGN.md`
- `website/css-tokens.css` → `../website/css-tokens.css`
- `brand-style-guide.md` → `../brand-style-guide.md`

## Memory system
Project-specific memory is available at `.claude/memory/` and synced with:
- Global memory: `/Users/clintsanchez/.claude/projects/-Users-clintsanchez-pCloud-Drive-Documents-BlakSheep-Creative-Clients-Riverside-Fairways-Riverside-Fairways/memory/`

## Next steps
- Any new Claude-related configuration should go in `.claude/settings/`
- Project memories should be saved to `.claude/memory/`
- Keep this folder checked into git for portability
