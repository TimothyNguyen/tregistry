---
name: diagram-cloudformation
version: 0.1.0
description: |
  AWS CloudFormation template visualization.
  Convert CloudFormation templates to architecture diagrams automatically.
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
      - diagram-iac
      - diagram-generate
    min-agent-arch-version: "0.1.4"
  training:
    keywords: [cloudformation, cf, template, aws, diagram, iac]
  discovery:
    related-to: [diagram-iac, diagram-infrastructure]
  support:
    maintenance-status: "active"
    owner-team: "diagram-systems"
    last-reviewed: "2026-06-27"
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.

# Diagram CloudFormation

Convert CloudFormation templates to architecture diagrams automatically.

## When to Use

- `/diagram-cloudformation` when user says: "Draw my CloudFormation stack", "Visualize this CF template", "Diagram my AWS infrastructure"
- User has CloudFormation JSON or YAML template
- Need to understand stack architecture visually
- Want to document infrastructure

## Capabilities

| Capability | Status | Use Case |
|-----------|--------|----------|
| CF JSON → diagram | ✅ Implemented | Parse CloudFormation JSON |
| CF YAML → diagram | ✅ Implemented | Parse CloudFormation YAML |
| Resource extraction | ✅ Implemented | Parse Resources section |
| Connection mapping | ✅ Implemented | Map logical relationships |
| Quick preview | ✅ Implemented | Fast diagram generation |

## Tools

### visualize_cloudformation_template

Convert CloudFormation template to architecture diagram.

```python
await visualize_cloudformation_template(
    template_content="""
    AWSTemplateFormatVersion: '2010-09-09'
    Resources:
      WebServer:
        Type: AWS::EC2::Instance
      Database:
        Type: AWS::RDS::DBInstance
    """,
    output_format="png"
)
```

**Parameters:**
- `template_content` (string, required): CloudFormation template (JSON or YAML)
- `output_format` (string, optional): png, svg, drawio, all

**Returns:** Diagram path, PNG preview

### extract_cf_resources

Extract resources from CloudFormation template.

**Returns:** Resource list with types and properties

## How It Works

1. Parse CloudFormation template (JSON/YAML)
2. Extract Resources section
3. Identify AWS resource types (EC2, RDS, Lambda, etc.)
4. Map logical connections (SecurityGroups, VPCs, etc.)
5. Convert to diagram-iac YAML format
6. Generate diagram via diagram-iac

## Example

**Input CloudFormation:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Simple web application'

Resources:
  WebSecurityGroup:
    Type: AWS::EC2::SecurityGroup
  
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      SecurityGroupIds:
        - !Ref WebSecurityGroup
  
  Database:
    Type: AWS::RDS::DBInstance

Outputs:
  InstanceId:
    Value: !Ref WebServer
```

**Output Diagram:** Visual architecture showing web server, security group, and database with connections.

## Prerequisites

**REQUIRED: Install Graphviz system package FIRST**

Graphviz is needed to render CloudFormation diagrams.

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

## Installation

### Python Package

```bash
# 1. Ensure graphviz is installed (see Prerequisites above)

# 2. Install Python package
pip install -e .

# 3. Verify imports work
python -c "from diagram_cloudformation.server import mcp; print('OK')"
```

## MCP Configuration

Add to Claude Desktop or other MCP client:

```json
{
  "mcpServers": {
    "diagram-cloudformation": {
      "command": "python",
      "args": ["-m", "diagram_cloudformation.server"],
      "env": {"LOG_LEVEL": "INFO"}
    }
  }
}
```

## Limitations

- Requires valid CloudFormation syntax
- Requires graphviz system package for rendering
- Complex templates with many resources may generate large diagrams
- Custom resources (non-AWS) shown as generic boxes
- Does not execute template (no actual resource creation)

## Related Skills

- **diagram-iac** - Manual YAML diagram definition
- **diagram-infrastructure** - Python diagrams DSL
- **diagram-export** - Export formats

## Architecture

Wraps diagram-iac by:
1. Parsing CF template
2. Extracting resource definitions
3. Converting to diagram-iac YAML format
4. Calling generate_iac_diagram()

## See Also

- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/)
- [diagram-iac](../diagram-iac) - Underlying YAML diagram generator
- [AWS Resources in diagrams](../diagram-iac/SKILL.md#supported-aws-resources)
