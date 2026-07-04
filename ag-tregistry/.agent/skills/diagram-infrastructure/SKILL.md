---
name: diagram-infrastructure
version: 0.1.0
description: |
  Multi-cloud infrastructure diagrams from Python DSL.
  Generate professional infrastructure diagrams for AWS, GCP, Azure, Kubernetes, hybrid, and multi-cloud architectures.
agents: [diagram-agent]
allowed-tools:
  - Read
  - Bash

metadata:
  category: "visual-system"
  domain: "infrastructure"
  tier: "recommended"
  dependencies:
    mcps:
      - name: infrastructure-diagram-mcp
        min-version: "0.0.4"
    packages:
      - diagrams >= 0.23.0
      - graphviz
    skills:
      - diagram-generate
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [infrastructure, cloud, diagram, AWS, GCP, Azure, Kubernetes, multi-cloud, architecture, Python]
  discovery:
    related-to: [diagram-generate, diagram-export, diagram-iac]
  approval-gates:
    policy-required: []
  support:
    maintenance-status: "active"
    owner-team: "diagram-systems"
    last-reviewed: "2026-06-27"

optional-skills: []
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.

# Diagram Infrastructure

Generate professional infrastructure diagrams using Python diagrams DSL.

## When to Use

- `/diagram-infrastructure` when user says: "Create an AWS architecture diagram", "Draw a Kubernetes cluster", "Visualize our multi-cloud setup"
- User has Python diagrams code or wants to generate from architecture specification
- Need multi-cloud support (AWS, GCP, Azure, Kubernetes)
- Architecture documentation with exportable outputs (.png, .svg, .pdf, .drawio)

## Capabilities

| Capability | Status | Use Case |
|-----------|--------|----------|
| AWS architecture diagrams | ✅ Implemented | EC2, Lambda, RDS, S3, networking, security groups |
| GCP infrastructure diagrams | ✅ Implemented | Compute, Storage, Networking, Cloud Run, GKE |
| Azure architecture diagrams | ✅ Implemented | VMs, App Services, Databases, networking |
| Kubernetes cluster diagrams | ✅ Implemented | Pods, Services, Deployments, networking |
| Hybrid & Multi-cloud | ✅ Implemented | Mixed cloud environments |
| .drawio export | ✅ Implemented | Edit in draw.io, compatible with diagram-export skill |
| .png/.svg export | ✅ Implemented | Raster and vector outputs |

## Tools

### generate_infrastructure_diagram

Generate diagram from Python diagrams DSL code.

```python
await generate_infrastructure_diagram(
    code="from diagrams import Diagram\nfrom diagrams.aws.compute import EC2\nwith Diagram('My Architecture'):\n    EC2('web')",
    diagram_name="my-architecture",
    output_format="png"  # png, svg, drawio, all
)
```

**Parameters:**
- `code` (string, required): Python diagrams DSL code
- `diagram_name` (string, optional): Diagram filename (default: auto-generated)
- `output_format` (string, optional): Output format: png, svg, drawio, all (default: all)

**Returns:** Path to generated diagram(s), preview, and code validation

### list_available_icons

List available icons for diagram generation (AWS, GCP, Azure, Kubernetes, etc.).

```python
await list_available_icons(
    provider="aws",  # aws, gcp, azure, k8s, or all
    category="compute"  # Optional filter
)
```

**Returns:** Icon catalog with categories

### parse_helm_chart

Parse Kubernetes Helm chart and generate diagram.

```python
await parse_helm_chart(
    chart_path="./helm-chart/",
    namespace="default"
)
```

**Returns:** Diagram showing Helm chart resources and relationships

## Routing Logic

```
User Request
    ↓
Is infrastructure diagram request? → Use this skill
    ↓
Has Python diagrams code? 
    ├─ Yes → generate_infrastructure_diagram()
    └─ No → Help user write code or suggest templates
    ↓
Want to export?
    ├─ No → Return PNG/SVG preview
    └─ Yes → generate_infrastructure_diagram(..., output_format="all")
    ↓
Want to edit in draw.io?
    └─ Yes → Use diagram-export skill with .drawio output
```

## Examples

### AWS Architecture

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS

with Diagram("AWS Architecture"):
    elb = ELB("load balancer")
    db = RDS("postgres")
    
    with Cluster("web servers"):
        web_servers = [EC2("web 1"), EC2("web 2")]
    
    elb >> web_servers >> db
```

### Multi-Cloud

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.gcp.compute import GCE
from diagrams.azure.compute import VM

with Diagram("Multi-Cloud Setup"):
    with Cluster("AWS"):
        aws = EC2("instance")
    with Cluster("GCP"):
        gcp = GCE("instance")
    with Cluster("Azure"):
        azure = VM("machine")
```

### Kubernetes

```python
from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, StatefulSet
from diagrams.k8s.network import Service

with Diagram("K8s Cluster"):
    with Cluster("default"):
        svc = Service("api")
        with Cluster("replicas"):
            pods = [Pod("pod-1"), Pod("pod-2")]
        svc >> pods
```

## Testing

```bash
# Generate test diagram
pytest tests/test_diagram_infrastructure.py -v

# Test icon discovery
python -m diagram_infrastructure list_available_icons --provider=aws
```

## MCP Integration

This skill requires the infrastructure-diagram-mcp server:

```json
{
  "mcpServers": {
    "infrastructure-diagram": {
      "command": "python",
      "args": ["-m", "infrastructure_diagram_mcp_server"],
      "env": {
        "GRAPHVIZ_PATH": "/opt/homebrew/bin/dot"
      }
    }
  }
}
```

## Architecture

```
diagram-infrastructure/
├── SKILL.md                    # This file
├── server.py                   # FastMCP server
├── diagrams_tools.py           # Diagram generation (from diagram-mcp-server)
├── models.py                   # Pydantic models
├── parsers/
│   ├── __init__.py
│   ├── helm_parser.py          # Helm chart parsing
│   └── k8s_parser.py           # Kubernetes YAML parsing
├── icons/
│   ├── aws_icons.py            # AWS provider icons
│   ├── gcp_icons.py            # GCP provider icons
│   └── azure_icons.py          # Azure provider icons
├── tests/
│   ├── test_diagram_infrastructure.py
│   └── fixtures/
│       ├── helm-chart/         # Test Helm chart
│       └── k8s.yaml            # Test K8s config
├── pyproject.toml
└── README.md
```

## Dependencies

- **diagrams** >= 0.23.0 (Python diagrams DSL)
- **graphviz** (system package + Python bindings)
- **fastmcp** >= 0.1.0 (MCP framework)
- **pydantic** >= 2.0.0 (validation)

## Known Limitations

- Requires graphviz system package (must be installed separately)
- Diagram complexity limited by GraphViz performance (typically <500 nodes)
- Helm chart parsing requires Helm 3+ installed for full template support
- Custom providers require importing additional libraries

## Future Enhancements

- Direct YAML→diagram conversion (YAML DSL)
- Terraform diagram generation
- CloudFormation template visualization
- Real-time diagram editing
- Diagram comparison/diff tool

## See Also

- [andrewmoshu/diagram-mcp-server](https://github.com/andrewmoshu/diagram-mcp-server) - Source implementation
- [diagram-as-code MCP](./diagram-iac.md) - AWS IaC diagram generation
- [diagram-cloudformation](./diagram-cloudformation.md) - CloudFormation visualization
- [Python diagrams docs](https://diagrams.mingrammer.com/) - DSL reference
