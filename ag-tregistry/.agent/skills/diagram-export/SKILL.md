---
name: diagram-export
version: 0.1.0
description: |
  Export Draw.io diagrams to PNG, SVG, PDF with styling options.
allowed-tools:
  - Read
  - Bash

agents: [design-agent, diagram-agent, spec-agent, pm]

metadata:
  category: "visual-system"
  domain: null
  tier: "essential"
  dependencies:
    mcps:
      - name: drawio-mcp
        min-version: "1.0.0"
    skills: []
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [export, png, pdf, svg, diagram, visualization]
  discovery:
    related-to: [diagram-generate, design-html]
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

# Diagram Export

Export .drawio files to PNG, SVG, or PDF with configurable styling and DPI.

## Checklist

1. **Validate input**
   - [ ] Input file is valid .drawio XML
   - [ ] Export format specified (png, svg, pdf)
   - [ ] Output path specified or default to `docs/diagrams/<name>.<format>`

2. **Configure export**
   - [ ] PNG: Ask DPI preference (default 96, high-res 300)
   - [ ] SVG: Ask embed-fonts preference (yes/no)
   - [ ] PDF: Ask page size (A4, letter, auto)

3. **Export**
   - [ ] Invoke MCP export tool
   - [ ] Verify output file created
   - [ ] Check file size is reasonable (PNG <5MB, PDF <10MB)

4. **Validate output**
   - [ ] Output file opens in viewer
   - [ ] Formatting preserved (colors, shapes)
   - [ ] No rendering artifacts

5. **Save & commit**
   - [ ] Save alongside .drawio: `docs/diagrams/name.png`, `name.pdf`, `name.svg`
   - [ ] Commit: `feat: export <name> diagram to <formats>`

## Export Formats

| Format | Best For | Use Case |
|--------|----------|----------|
| **PNG** | Web, docs, presentations | Screenshots, embedding in markdown |
| **SVG** | Web, scaling | Interactive docs, responsive designs |
| **PDF** | Print, sharing, archives | Formal documentation, distribution |

### PNG Export

DPI options:
- 96 DPI (screen resolution, smaller file)
- 150 DPI (high-quality screen display)
- 300 DPI (print quality, larger file)

Default: 96 DPI unless print intended.

### SVG Export

Embedded fonts: Yes (self-contained) or No (smaller file, requires fonts)

Default: Yes (self-contained).

### PDF Export

Page size options:
- A4 (210×297mm, standard)
- Letter (8.5×11in, US standard)
- Auto (fit content, minimal margins)

Default: Auto.

## Anti-Patterns

❌ Exporting multiple formats without specifying output paths
❌ PNG at 300 DPI for web (wasteful file size)
❌ PDF without page size preference
❌ Exporting before diagram is validated

✅ Always ask user: "Which formats? PNG for web, PDF for print?"
✅ Default to sensible DPI for use case
✅ Validate diagram before exporting

## See Also

- [`diagram-generate`](../diagram-generate/SKILL.md) — Create diagrams
- [`diagram-validate`](../diagram-validate/SKILL.md) — Validate before export

---
