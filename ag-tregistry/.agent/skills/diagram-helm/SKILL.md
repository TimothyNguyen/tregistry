---
name: diagram-helm
version: 0.1.0
description: |
  Kubernetes Helm chart visualization.
  Generate architecture diagrams from Helm charts automatically.
agents: [diagram-agent]
allowed-tools:
  - Read
  - Bash

metadata:
  category: "visual-system"
  domain: "infrastructure"
  tier: "recommended"
  dependencies:
    skills:
      - diagram-infrastructure
      - diagram-generate
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [kubernetes, helm, k8s, diagram, containerization]
  discovery:
    related-to: [diagram-infrastructure]
  support:
    maintenance-status: "active"
    owner-team: "diagram-systems"
    last-reviewed: "2026-06-27"
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.

# Diagram Helm

Generate Kubernetes architecture diagrams from Helm charts automatically.

## When to Use

- `/diagram-helm` when user says: "Draw my Helm chart", "Visualize Kubernetes deployment", "Diagram this Helm release"
- User has Helm chart directory or values
- Need to understand Kubernetes architecture visually
- Want to document Helm deployments

## Capabilities

| Capability | Status | Use Case |
|-----------|--------|----------|
| Helm chart parsing | ✅ Implemented | Parse Helm chart structure |
| Pod/Deployment extraction | ✅ Implemented | Extract k8s resources |
| Service mapping | ✅ Implemented | Show service relationships |
| Multi-container analysis | ✅ Implemented | Visualize sidecar patterns |
| Replica/DaemonSet handling | ✅ Implemented | Show deployment scaling |

## Tools

### visualize_helm_chart

Convert Helm chart to architecture diagram.

```python
await visualize_helm_chart(
    chart_path="./my-app-chart/",
    namespace="default",
    values_override={"replicaCount": 3}
)
```

**Parameters:**
- `chart_path` (string, required): Path to Helm chart directory
- `namespace` (string, optional): Kubernetes namespace (default: default)
- `values_override` (object, optional): Override values.yaml settings

**Returns:** Diagram path, PNG preview

### parse_helm_values

Extract resource definitions from Helm chart values.

**Returns:** Pod specs, services, ingresses, configmaps, etc.

## Example

**Helm Chart Structure:**
```
my-app-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
```

**Generated Diagram:** Shows:
- Ingress → Service → Pods
- Multiple pod replicas
- Sidecar containers
- ConfigMaps/Secrets referenced

## Key Features

### Multi-Tier Visualization

Shows relationships between:
- Ingress → Load Balancer
- Service → Pod Endpoints
- StatefulSets → Persistent Volumes
- DaemonSets → All Nodes

### Container Analysis

For each Pod:
- Main container(s)
- Init containers
- Sidecar containers
- Volume mounts
- Port exposures

### Network Policies

Visualizes:
- Service selectors
- Network policies
- Ingress rules
- DNS names

## Limitations

- Requires Helm 3+ installed
- Template variables must be evaluable
- CRDs (custom resources) shown as generic boxes
- Complex Helm hooks simplified

## Prerequisites

**REQUIRED: Install system dependencies FIRST**

### Graphviz (Required for diagram rendering)

Graphviz is needed to render Helm chart diagrams.

```bash
# macOS (Homebrew)
brew install graphviz

# Ubuntu/Debian (apt)
sudo apt-get install graphviz graphviz-dev

# RHEL/CentOS (yum)
sudo yum install graphviz graphviz-devel

# Windows (Chocolatey - requires admin)
choco install graphviz

# Windows (Direct download)
# Download from https://graphviz.org/download/ and add to PATH
```

Verify installation:
```bash
dot -V  # Should print Graphviz version
```

### Helm (Required for parsing Helm charts)

Helm is required to parse and render Helm chart templates.

```bash
# macOS (Homebrew)
brew install helm

# Ubuntu/Debian (apt)
sudo apt-get install helm

# RHEL/CentOS (yum)
sudo yum install helm

# Windows (Chocolatey)
choco install kubernetes-helm

# Windows (Direct download)
# Download from https://github.com/helm/helm/releases and add to PATH
```

Verify installation:
```bash
helm version  # Should print version information
```

## Installation

### Python Package

```bash
# 1. Ensure graphviz and helm are installed (see Prerequisites above)

# 2. Install Python package
pip install -e .

# 3. Verify imports work
python -c "from diagram_helm.server import mcp; print('OK')"
```

## MCP Configuration

Add to Claude Desktop or other MCP client:

```json
{
  "mcpServers": {
    "diagram-helm": {
      "command": "python",
      "args": ["-m", "diagram_helm.server"],
      "env": {"LOG_LEVEL": "INFO"}
    }
  }
}
```

## Workflow

```
User provides Helm chart path
    ↓
Parse chart metadata (Chart.yaml)
    ↓
Load and render values
    ↓
Extract Kubernetes resources
    ↓
Map relationships (Services→Pods, etc.)
    ↓
Generate diagram-infrastructure YAML
    ↓
Call diagram-infrastructure MCP
    ↓
Return architecture visualization
```

## Related Skills

- **diagram-infrastructure** - Underlying diagram generator
- **diagram-export** - Export formats
- **diagram-generate** - High-level requests

## Installation

```bash
# Requires Helm 3+
brew install helm        # macOS
sudo apt-get install helm  # Linux

# Optional: Helm plugins for advanced parsing
helm plugin install https://github.com/chartmuseum/helm-push
```

## See Also

- [Helm Documentation](https://helm.sh/)
- [Kubernetes Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [diagram-infrastructure](../diagram-infrastructure) - Underlying diagram tool
