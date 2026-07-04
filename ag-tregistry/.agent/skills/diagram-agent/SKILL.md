---
name: diagram-agent
version: 0.1.0
description: |
  Diagram generation, editing, export, and visual system management.
  Specializes in Draw.io diagrams: architecture, flowchart, ER, sequence, class, state, mind-map.
agents: [_infrastructure]
allowed-tools:
  - Read
  - Bash
  - Grep

metadata:
  category: "visual-system"
  domain: null
  tier: "recommended"
  dependencies:
    mcps:
      - name: drawio-mcp
        min-version: "1.0.0"
    skills:
      - diagram-generate
      - diagram-export
      - diagram-validate
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [diagram, architecture, flowchart, visual, draw.io, sketch]
  discovery:
    related-to: [design-agent, design-html, design-review]
  approval-gates:
    policy-required: [mcp-egress]
  support:
    maintenance-status: "active"
    owner-team: "design-systems"
    last-reviewed: "2026-06-26"

optional-skills:
  - diagram-search
  - diagram-style
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Diagram Agent

Specialist agent for diagram generation, editing, export, and visual system management.

## When to Use

- `/diagram-agent` when user says: "Draw the architecture", "Create a flowchart", "Design a data model"
- User wants diagrams as primary deliverable (not secondary visuals)
- Diagram needs editing, styling, or multi-format export
- Architecture/flow documentation is critical to spec

## Skills

This agent coordinates across:

| Skill | Use | Invoked When |
|-------|-----|--------------|
| `diagram-generate` | Create diagrams from text | "Draw X", "Create a flowchart", "Visualize the flow" |
| `diagram-export` | Export to PNG/SVG/PDF | "Export to PNG", "I need this as PDF" |
| `diagram-search` | Find shapes, icons, templates | "Find an AWS Lambda shape", "Search AWS icons" |
| `diagram-validate` | Check completeness | Before exporting: all labels? connections complete? |
| `diagram-style` (optional) | Apply design system colors | "Use our brand colors", "Apply dark theme" |

## Routing Logic

```
User Request
    ↓
Is diagram request? → /diagram-agent
    ↓
Need specific type? (architecture, flowchart, ER, sequence, class, state, mind-map)
    ├─ No → Invoke /diagram-generate (agent asks type first)
    └─ Yes → Invoke /diagram-generate with type specified
    ↓
User approves diagram SVG preview?
    ├─ No → /diagram-generate (revise)
    └─ Yes → Continue
    ↓
Need styling? → /diagram-style (optional)
    ↓
Need export? (PNG, SVG, PDF)
    ├─ No → Save .drawio file, done
    └─ Yes → /diagram-export
    ↓
Validate completeness
    ├─ Issues found → /diagram-validate (checklist)
    └─ Complete → Done
```

## Agent Workflows

### Workflow 1: Generate + Preview (Minimal)

```
1. /diagram-generate
   ├─ Ask: diagram type?
   ├─ Ask: scope (components, entities, actors)?
   └─ Generate SVG preview inline

2. User approves or requests revisions
   ├─ Approve → Save .drawio
   └─ Revise → /diagram-generate again
```

**Time:** 5-10 minutes

**Output:** `.drawio` file + SVG in docs/diagrams/

### Workflow 2: Generate + Export (Production)

```
1. /diagram-generate
   ├─ Create diagram from spec
   ├─ Show SVG preview
   └─ Get approval

2. /diagram-export
   ├─ Export PNG (for docs)
   ├─ Export PDF (for print)
   └─ Export SVG (for embedding)

3. /diagram-validate
   ├─ Check: all labels present?
   ├─ Check: swimlanes correct?
   ├─ Check: connections complete?
   └─ Output: validation report

4. Save all files, commit
```

**Time:** 15-30 minutes

**Output:** diagram.drawio, diagram.png, diagram.pdf, diagram.svg

### Workflow 3: Edit Existing Diagram

```
1. Load .drawio file from repo
2. Ask: what should change?
3. /diagram-generate (load + modify mode)
4. Preview changes
5. Export updated versions
6. Commit changes
```

**Time:** 5-15 minutes

## Diagram Types Reference

| Type | Best For | Example |
|------|----------|---------|
| **Flowchart** | Process flows, decision trees | Login flow, deployment pipeline |
| **Architecture** | System components + connections | Microservices architecture, cloud setup |
| **ER (Entity-Relationship)** | Data models, schema | Database design, entity relationships |
| **Sequence** | Actor interactions, workflows | User journey, API call sequence |
| **Class** | Object-oriented design | Class hierarchy, inheritance |
| **State** | State machines, lifecycle | Order status flow, app states |
| **Mind-Map** | Brainstorming, concepts | Feature breakdown, organization |
| **Swimlane** | Parallel processes, actors | Cross-functional flow, responsibilities |

**Decision logic:**

- Complex process? → Flowchart
- Infrastructure/components? → Architecture
- Data model? → ER
- Actor interactions? → Sequence
- OOP design? → Class
- State changes? → State machine
- Exploration? → Mind-map
- Multi-actor responsibility? → Swimlane

## Anti-Patterns

❌ **Avoid:**
- Generating without asking type first
- Creating overly detailed diagrams (15+ components = too complex)
- Using XML when Mermaid is simpler
- Exporting before user approves
- Mixing multiple diagram purposes in one canvas
- Forgetting to validate before exporting

✅ **Do:**
- Ask clarifying questions first
- Keep diagrams focused and simple
- Show SVG preview before saving
- Validate completeness
- Use consistent styling
- Save both .drawio (editable) and exports

## Policy Requirements

**MCP Egress:** diagram-generate requires explicit approval to invoke `drawio-mcp` server.

Set in skill metadata:
```yaml
approval-gates:
  policy-required: [mcp-egress]
```

User must approve: "This will connect to drawio-mcp to generate diagrams. OK?"

## Diagram Placement & Grid

Diagrams follow rigid grid to simplify layout:

```
Column position: col * 180 + 40
Row position:    row * 120 + 40

Example: Cell (2, 3) is at (2*180+40, 3*120+40) = (400, 400)
```

This eliminates overlap checking and simplifies generation.

## Integration Points

**With `/design-agent`:**
- Design-agent handles UI component design
- Diagram-agent handles architecture/flow visualization
- Collaborate on system architecture diagrams

**With `/spec-agent`:**
- Spec writes requirements
- Diagram-agent visualizes spec (swimlanes, flows, actors)
- Diagrams added to spec document

**With `/orchestrate`:**
- Orchestrate coordinates multi-agent work
- Diagram-agent contributes visual specs
- Other agents implement based on diagram + spec

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Too many components" | Break into multiple focused diagrams |
| "Layout messy" | Use swimlanes to organize, apply grid |
| "Colors look wrong" | Invoke `/diagram-style` for design system colors |
| "Shapes missing" | Invoke `/diagram-search` to find specific shapes |
| "File won't open" | Validate XML syntax: `/diagram-validate` |
| "Export quality poor" | Try PNG with higher DPI or use PDF instead |

## Related Skills

- [`diagram-generate`](../diagram-generate/SKILL.md) — Core diagram creation
- [`diagram-export`](../diagram-export/SKILL.md) — Export to PNG/SVG/PDF
- [`diagram-search`](../diagram-search/SKILL.md) — Find shapes & templates
- [`diagram-validate`](../diagram-validate/SKILL.md) — Validate completeness
- [`diagram-style`](../diagram-style/SKILL.md) — Apply design system styling
- [`design-agent`](../agents/design-agent/SKILL.md) — UI/design specialist
- [`design-html`](../design-html/SKILL.md) — HTML component design

## See Also

- [drawio-mcp Analysis](../../docs/DRAWIO-MCP-ANALYSIS.md)
- [Diagram Examples](../../references/diagram-examples.md)
- [Shape Library Reference](../../references/shape-library.md)

