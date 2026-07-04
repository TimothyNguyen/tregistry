---
name: diagram-iac
version: 0.1.0
description: |
  AWS architecture diagrams from YAML code (infrastructure-as-code).
  Generate architecture diagrams using diagram-as-code YAML format.
agents: [diagram-agent]
allowed-tools:
  - Read
  - Bash

metadata:
  category: "visual-system"
  domain: "infrastructure"
  tier: "recommended"
  dependencies:
    external:
      - awsdac (diagram-as-code CLI)
    skills:
      - diagram-generate
      - diagram-export
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [aws, architecture, iac, yaml, diagram, code]
  discovery:
    related-to: [diagram-infrastructure, diagram-cloudformation, diagram-generate]
  approval-gates:
    policy-required: []
  support:
    maintenance-status: "active"
    owner-team: "diagram-systems"
    last-reviewed: "2026-06-27"
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.

# Diagram IaC

Generate AWS architecture diagrams from YAML (Infrastructure-as-Code).

## When to Use

- `/diagram-iac` when user says: "Create AWS architecture from YAML", "Draw from infrastructure template", "Visualize my CloudFormation"
- User has YAML diagram definitions or infrastructure specifications
- Need to generate diagrams that follow AWS architecture guidelines
- Want YAML-based, version-controlled diagram definitions

## Capabilities

| Capability | Status | Use Case |
|-----------|--------|----------|
| YAML → diagram generation | ✅ Implemented | IaC-based architecture diagrams |
| AWS compliance | ✅ Implemented | Architecture guidelines adherence |
| PNG output | ✅ Implemented | Documentation, presentations |
| DRAWIO export | ✅ Implemented | Edit in draw.io |
| Reusable templates | ✅ Implemented | Share diagram patterns |
| CloudFormation preview | ⚠️ Planned | CF template → YAML conversion |

## Tools

### generate_iac_diagram

Generate diagram from YAML infrastructure definition.

```python
await generate_iac_diagram(
    yaml_content="""
    DiagramName: "My AWS Architecture"
    Resources:
      - Type: EC2
        Label: "Web Server"
      - Type: RDS
        Label: "Database"
    Connections:
      - Source: 0
        Target: 1
    """,
    output_format="png"
)
```

**Parameters:**
- `yaml_content` (string, required): YAML infrastructure definition
- `output_format` (string, optional): png, svg, drawio, all (default: all)
- `output_path` (string, optional): Custom output directory

**Returns:** Path to generated diagram, PNG preview

### list_aws_resources

List available AWS resources for diagram generation.

```python
await list_aws_resources(
    category="compute"  # Optional: compute, network, database, storage
)
```

**Returns:** Resource catalog by category

## YAML Format

```yaml
DiagramName: "AWS Architecture Example"
Description: "Sample 3-tier web application"
Groups:
  - Name: "Web Tier"
    Resources:
      - Type: ELB
        Label: "Load Balancer"
      - Type: EC2
        Label: "Web Server 1"
      - Type: EC2
        Label: "Web Server 2"
  
  - Name: "Application Tier"
    Resources:
      - Type: Lambda
        Label: "API Handler"
  
  - Name: "Data Tier"
    Resources:
      - Type: RDS
        Label: "PostgreSQL"
      - Type: ElastiCache
        Label: "Redis"

Connections:
  - Source: ["Load Balancer"]
    Target: ["Web Server 1", "Web Server 2"]
  - Source: ["Web Server 1", "Web Server 2"]
    Target: ["API Handler"]
  - Source: ["API Handler"]
    Target: ["PostgreSQL", "Redis"]
```

## Supported AWS Resources

**Compute:**
- EC2, ECS, Lambda, Elastic Beanstalk, AppRunner

**Storage:**
- S3, EBS, EFS, Glacier, Backup

**Database:**
- RDS, DynamoDB, ElastiCache, DocumentDB, Neptune

**Networking:**
- VPC, Subnet, SecurityGroup, NatGateway, InternetGateway, ELB, ALB, NLB, VPNGateway

**Security:**
- IAM, KMS, Secrets Manager, Certificate Manager

**Monitoring:**
- CloudWatch, CloudTrail, X-Ray

... and 100+ more AWS services

## Examples

### Simple 3-Tier App

```yaml
DiagramName: "3-Tier Web Application"

Groups:
  - Name: "Presentation Layer"
    Resources:
      - Type: CloudFront
        Label: "CDN"
      - Type: ALB
        Label: "Load Balancer"
  
  - Name: "Application Layer"
    Resources:
      - Type: ECS
        Label: "Web Containers"
      - Type: Lambda
        Label: "API"
  
  - Name: "Data Layer"
    Resources:
      - Type: RDS
        Label: "Database"
      - Type: ElastiCache
        Label: "Cache"

Connections:
  - Source: ["CDN"]
    Target: ["Load Balancer"]
  - Source: ["Load Balancer"]
    Target: ["Web Containers", "API"]
  - Source: ["Web Containers", "API"]
    Target: ["Database", "Cache"]
```

### Microservices

```yaml
DiagramName: "Microservices Architecture"

Groups:
  - Name: "API Gateway"
    Resources:
      - Type: APIGateway
        Label: "REST API"
  
  - Name: "Services"
    Resources:
      - Type: Lambda
        Label: "User Service"
      - Type: Lambda
        Label: "Order Service"
      - Type: Lambda
        Label: "Payment Service"
  
  - Name: "Data"
    Resources:
      - Type: DynamoDB
        Label: "Users"
      - Type: DynamoDB
        Label: "Orders"
  
  - Name: "Messaging"
    Resources:
      - Type: SQS
        Label: "Task Queue"

Connections:
  - Source: ["REST API"]
    Target: ["User Service", "Order Service"]
  - Source: ["Order Service"]
    Target: ["Payment Service", "Task Queue"]
```

## Routing Logic

```
User provides YAML
    ↓
Validate YAML syntax
    ↓
Check resource types (AWS compliance)
    ↓
generate_iac_diagram()
    ↓
Return PNG + preview
    ↓
User approves?
    ├─ No → Revise YAML
    └─ Yes → Export (diagram-export skill)
```

## Prerequisites

**REQUIRED: Install system dependencies FIRST**

### Graphviz (Required for diagram rendering)

Graphviz is needed to render diagrams.

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

### AWS Diagram-as-Code CLI (awsdac) - Required for diagram generation

awsdac is the CLI tool that parses YAML and generates diagrams.

```bash
# macOS (Homebrew)
brew install awsdac

# Linux/macOS (go install)
go install github.com/awslabs/diagram-as-code/cmd/awsdac@latest

# Windows - Install from GitHub releases
# https://github.com/awslabs/diagram-as-code/releases
# Download .exe and add to PATH
```

Verify installation:
```bash
awsdac --version  # Should print version number
```

## Installation

### Python Package

```bash
# 1. Ensure graphviz and awsdac are installed (see Prerequisites above)

# 2. Install Python package
pip install -e .

# 3. Verify imports work
python -c "from diagram_iac.server import mcp; print('OK')"
```

## MCP Configuration

Add to Claude Desktop or other MCP client:

```json
{
  "mcpServers": {
    "diagram-iac": {
      "command": "python",
      "args": ["-m", "diagram_iac.server"],
      "env": {"AWSDAC_PATH": "awsdac"}
    }
  }
}
```

## Testing

```bash
# Validate YAML
awsdac my-architecture.yaml --validate

# Generate diagram
awsdac my-architecture.yaml -o architecture.png

# List available resources
awsdac --list-resources
```

## Architecture

```
diagram-iac/
├── SKILL.md              # This file
├── server.py             # FastMCP server wrapper
├── models.py             # Pydantic models
├── aws_resources.py      # AWS resource catalog
├── tests/
│   └── test_diagram_iac.py
└── examples/
    ├── simple-app.yaml
    ├── microservices.yaml
    └── vpc-network.yaml
```

## Known Limitations

- Requires awsdac (diagram-as-code) CLI installed
- AWS resources only (not multi-cloud)
- YAML format specific to awsdac syntax
- No real-time editing (generate from YAML only)

## Integration

**Works with:**
- diagram-generate (high-level requests)
- diagram-export (format conversion)
- diagram-cloudformation (CF template integration)

**Skill family:** diagram-*

## See Also

- [awslabs/diagram-as-code](https://github.com/awslabs/diagram-as-code) - Source
- [diagram-iac documentation](https://github.com/awslabs/diagram-as-code/blob/main/doc/introduction.md)
- [AWS architecture guidelines](https://aws.amazon.com/architecture/icons/)
- [diagram-cloudformation](./diagram-cloudformation.md) - CloudFormation → YAML
