---
name: diagram-search
version: 0.1.0
description: |
  Search Draw.io shape library for icons, shapes, and templates.
  Supports 10,000+ shapes: AWS, Azure, Cisco, P&ID, flowchart elements, etc.
allowed-tools:
  - Bash
  - Grep

agents: [design-agent, diagram-agent, spec-agent, orchestrate]

metadata:
  category: "visual-system"
  domain: null
  tier: "recommended"
  dependencies:
    mcps:
      - name: drawio-mcp
        min-version: "1.0.0"
    skills: []
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [search, shapes, icons, aws, azure, templates, library]
  discovery:
    related-to: [diagram-generate, design-agent]
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

# Shape Search

Search 10,000+ Draw.io shapes across all libraries.

## Supported Libraries

| Library | Examples | Count |
|---------|----------|-------|
| AWS | Lambda, S3, RDS, VPC, API Gateway | 500+ |
| Azure | App Service, SQL Database, Blob Storage | 400+ |
| Cisco | Routers, Firewalls, Switches | 300+ |
| Kubernetes | Pods, Services, Deployments | 200+ |
| GCP | Compute, Cloud SQL, Cloud Storage | 300+ |
| Flowchart | Decision, Process, Terminator, Data | 50+ |
| P&ID (Process & Instrumentation) | Valves, pumps, sensors, reactors | 400+ |
| UML | Class, sequence, state machine elements | 150+ |
| UI/UX | Forms, buttons, icons, wireframes | 200+ |
| Database | Tables, relationships, normalization | 100+ |
| Standard Shapes | Rectangle, circle, diamond, polygon | 50 |

## Search Patterns

**By name:** `lambda`, `rds`, `s3`, `api gateway`
**By category:** `aws compute`, `azure storage`, `kubernetes`
**By domain:** `database`, `messaging`, `storage`, `compute`
**Fuzzy:** `lambda-like`, `similar to ec2`

## Checklist

1. **Ask for search criteria**
   - What shape/icon do you need?
   - Which cloud provider (AWS, Azure, GCP)?
   - Approximate category?

2. **Search**
   - Invoke MCP search_shapes tool
   - Return top 5-10 matching shapes with previews

3. **Present options**
   - Show shape name, description, library
   - Let user pick which shape to use

4. **Export shape definition**
   - Save shape definition for use in diagram-generate
   - Or: auto-add to current diagram

## Common Searches

| Need | Search |
|------|--------|
| AWS Lambda | `aws lambda` or `aws compute` |
| Database | `database` or `rds` or `dynamodb` |
| Message queue | `sqs` or `kafka` or `messaging` |
| Load balancer | `elb` or `alb` or `load balancer` |
| Cache | `elasticache` or `redis` or `cache` |
| Kubernetes pod | `k8s pod` or `kubernetes pod` |
| API | `api gateway` or `rest api` |
| Storage | `s3` or `storage` or `blob` |

## Anti-Patterns

❌ Using generic rectangles when domain-specific shapes exist
❌ Searching without specifying cloud provider
❌ Mixing multiple cloud provider shapes (AWS + Azure) in same diagram
❌ Using outdated shape names (old AWS icons)

✅ Search first if domain-specific shapes available
✅ Specify cloud provider to narrow results
✅ Keep shapes consistent within diagram
✅ Use modern shape libraries

## See Also

- [`diagram-generate`](../diagram-generate/SKILL.md) — Use shapes in diagrams
- [Draw.io Shape Library](https://www.draw.io/)

---
