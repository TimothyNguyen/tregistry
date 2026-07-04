---
name: diagram-validate
version: 0.1.0
description: |
  Validate diagram completeness and design patterns.
  Checks: all labels present, connections complete, swimlanes correct.
allowed-tools:
  - Read
  - Bash
  - Grep

agents: [diagram-agent, qa-agent, design-agent, spec-agent]

metadata:
  category: "visual-system"
  domain: null
  tier: "essential"
  dependencies:
    mcps: []
    skills: []
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [validate, check, quality, completeness, diagram]
  discovery:
    related-to: [diagram-generate, diagram-export]
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

# Diagram Validation

Validate diagrams before export. Checks completeness, design patterns, and quality.

## Validation Checklist

Before exporting .drawio file, run through:

- [ ] **All nodes labeled** — No unnamed boxes
- [ ] **All connections have endpoints** — No dangling edges
- [ ] **Swimlanes defined** — If present: clear actor/responsibility labels
- [ ] **No self-loops** — Node shouldn't point to itself (unless intentional state machine)
- [ ] **No unreachable nodes** — All nodes connected to main flow
- [ ] **Consistent styling** — Colors, fonts, sizing consistent
- [ ] **Text readable** — No overlapping labels, minimum font size 10pt
- [ ] **Grid alignment** — Shapes aligned to grid (for cleaner layout)
- [ ] **Connection points** — Edges connect at shape corners/centers, not arbitrary points

## Diagram-Specific Checks

### Flowchart

- [ ] Start node exists (typically circle or "Start" oval)
- [ ] End node exists (typically circle or "End" oval)
- [ ] All decisions have two+ paths (Yes/No, True/False, etc.)
- [ ] No loops back to start (unless infinite loop intended)
- [ ] Process boxes clearly describe action (verb + noun)

### Architecture

- [ ] All components labeled with name + type
- [ ] Data flow arrows labeled (request, response, event, etc.)
- [ ] External systems distinguished from internal
- [ ] Database/cache layers clearly separated
- [ ] No duplicate components

### ER (Entity-Relationship)

- [ ] All tables have primary key labeled
- [ ] Relationships labeled with cardinality (1:1, 1:N, M:N)
- [ ] Foreign keys marked
- [ ] No orphaned tables (all connected)
- [ ] Column types specified in diagram or legend

### Sequence Diagram

- [ ] All actors/participants labeled
- [ ] Lifelines properly terminated
- [ ] Message sequences numbered or ordered
- [ ] Return arrows distinct from request arrows
- [ ] No messages crossing without intersection

### State Machine

- [ ] Initial state marked
- [ ] Final/accepting states marked
- [ ] Transitions labeled with trigger condition
- [ ] All states reachable from initial
- [ ] No unreachable states

## Common Issues & Fixes

| Issue | Check | Fix |
|-------|-------|-----|
| Unnamed boxes | All nodes labeled? | Add labels: "Process Name" |
| Dangling edges | All arrows connected? | Remove or connect edges |
| Overlapping text | Text readable? | Expand boxes, reduce font, reposition |
| Misaligned shapes | Grid aligned? | Enable grid snap, align to grid |
| Unclear flow | Decision labels clear? | Add Yes/No or True/False labels |
| Too complex | Scope < 20 components? | Split into multiple focused diagrams |
| Inconsistent colors | Color scheme consistent? | Apply diagram-style skill |
| Unclear relationships | ER labels present? | Add 1:1, 1:N, M:N labels |

## Anti-Patterns

❌ Exporting without validation
❌ Ignoring warnings ("It looks fine to me")
❌ Unlabeled nodes or edges
❌ Too many components (20+)
❌ Mixing multiple diagram types in one canvas

✅ Always validate before export
✅ Fix all issues from checklist
✅ Keep diagrams focused and simple
✅ Label everything
✅ One diagram = one concept

## Output Rules

After validation, output:
1. ✅ Validation PASSED (all checks green) or
2. ⚠️ Validation WARNING (issues found, list them) or
3. ❌ Validation FAILED (blockers, must fix)

If issues found, ask: "Fix these and revalidate?"

## See Also

- [`diagram-generate`](../diagram-generate/SKILL.md) — Create diagrams
- [`diagram-export`](../diagram-export/SKILL.md) — Export after validation

---
