---
name: diagram-style
version: 0.1.0
description: |
  Apply consistent styling to diagrams. Colors, fonts, themes.
allowed-tools:
  - Read
  - Bash

agents: [design-agent, diagram-agent]

metadata:
  category: "visual-system"
  domain: null
  tier: "optional"
  dependencies:
    mcps: []
    skills: []
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [style, theme, color, font, design, brand]
  discovery:
    related-to: [diagram-generate, design-review, design-html]
  approval-gates: []
  support:
    maintenance-status: "active"
    owner-team: "design-systems"
    last-reviewed: "2026-06-26"
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Diagram Styling

Apply consistent styling: colors, fonts, themes to diagrams.

## Style Profiles

### Enterprise (Default)

- Background: White (#FFFFFF)
- Shapes: Corporate blue (#0066CC)
- Accents: Orange (#FF9900)
- Text: Dark gray (#333333), sans-serif
- Use case: Business, architecture, documentation

### Dark Mode

- Background: Dark gray (#1E1E1E)
- Shapes: Light blue (#66B2FF)
- Accents: Orange (#FF9900)
- Text: White (#FFFFFF), sans-serif
- Use case: Presentations, web apps

### Accessible

- High contrast: Black (#000000), white (#FFFFFF)
- No color-only distinctions
- Larger fonts (12pt minimum)
- Use case: Public documentation, inclusive design

### Brand Custom

- User-specified color palette
- Logo placement option
- Custom fonts (if available)
- Use case: Client deliverables, marketing

## Styling Options

| Option | Example | Effect |
|--------|---------|--------|
| **Colors** | `--primary #0066CC` | Shape fill color |
| **Accents** | `--accent #FF9900` | Highlight, decision nodes |
| **Text** | `--font-family Arial` | Font for all labels |
| **Borders** | `--border-width 2` | Edge thickness |
| **Theme** | `--theme dark` | Preset theme |

## Checklist

1. **Ask for styling preference**
   - Enterprise (default) / Dark / Accessible / Custom?
   - Any brand colors or logos?

2. **Apply style profile**
   - Invoke MCP style tool or manual XML edit
   - Update all shape colors, text colors, fonts

3. **Validate styling**
   - Colors consistent?
   - Text readable (contrast)?
   - No unintended changes?

4. **Save styled diagram**
   - Save as new version or update existing
   - Commit: `style: apply <theme> theme to <diagram>`

## Anti-Patterns

❌ Applying different colors to similar elements
❌ White text on light background (unreadable)
❌ Too many colors (more than 5 in palette)
❌ Overly stylized (prioritize clarity)

✅ Consistent color scheme
✅ High contrast text
✅ Minimal, professional palette
✅ Clarity first, aesthetics second

## See Also

- [`diagram-generate`](../diagram-generate/SKILL.md) — Create diagrams
- [`design-agent`](../agents/design-agent/SKILL.md) — Design specialist

---
