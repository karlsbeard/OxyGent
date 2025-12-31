---
name: technical-writer
description: Write technical documentation, guides, and API references
version: "1.0.0"
author: OxyGent Team

allowed-tools:
  - Read
  - Glob
  - Grep

model: claude-3-opus
timeout: 180
---

# Technical Writer Skill

## Overview

This skill creates high-quality technical documentation including API references, user guides, tutorials, and architectural documentation.

## Instructions

When this skill is activated, follow these steps to create effective technical documentation:

### Step 1: Understand the Documentation Request

1. Identify the type of documentation needed
2. Determine the target audience (developers, end-users, executives)
3. Understand the subject matter (use Read/Glob/Grep to explore code)
4. Clarify the scope and depth required

### Step 2: Explore the Subject Matter

Use available tools to understand the topic:
- **Read:** Examine source code, existing docs, config files
- **Glob:** Find related files and understand structure
- **Grep:** Search for specific patterns, functions, or configurations

### Step 3: Create the Documentation

Use the appropriate format based on the documentation type:

## Documentation Templates

### API Reference Template

```markdown
# [API/Module] Reference

## Overview
[Brief description of what this API/module does and when to use it]

## Base URL
```
[Base URL for all endpoints]
```

## Authentication
[Description of authentication method]

### Bearer Token
```bash
Authorization: Bearer YOUR_TOKEN
```

## Endpoints

### [Endpoint Name]

**Method:** `GET|POST|PUT|DELETE`
**Path:** `/path/to/endpoint`
**Description:** [What this endpoint does]

#### Request

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param` | string | Yes | [Description] |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filter` | string | No | [Description] |

**Request Body:**
\`\`\`json
{
  "field": "value",
  "nested": {
    "field": "value"
  }
}
\`\`\`

#### Response

**Success Response (200):**
\`\`\`json
{
  "status": "success",
  "data": {}
}
\`\`\`

**Error Response (4xx/5xx):**
\`\`\`json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
\`\`\`

#### Example

\`\`\`bash
curl -X POST https://api.example.com/endpoint \\
  -H "Authorization: Bearer TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"field": "value"}'
\`\`\`

---

## Data Models

### [Model Name]
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `name` | string | Display name |

## Error Codes
| Code | Description |
|------|-------------|
| `INVALID_INPUT` | Input validation failed |
| `NOT_FOUND` | Resource not found |
```

### User Guide Template

```markdown
# [Feature/Product] User Guide

## Introduction
[What this feature does and value proposition]

## Prerequisites
- [Requirement 1]
- [Requirement 2]

## Getting Started

### Installation/Setup
\`\`\`bash
# Installation commands
\`\`\`

### Basic Usage
\`\`\`
# Code example
\`\`\`

## Features

### [Feature 1]: [Description]
[How to use this feature with examples]

### [Feature 2]: [Description]
[How to use this feature with examples]

## Common Use Cases

### Use Case 1: [Title]
**Scenario:** [Description]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:** [What happens]

### Use Case 2: [Title]
[Continue pattern...]

## Troubleshooting

### Problem: [Issue description]
**Solution:** [Steps to resolve]

### Problem: [Issue description]
**Solution:** [Steps to resolve]

## FAQ

**Q: [Common question]**
A: [Answer]

**Q: [Common question]**
A: [Answer]

## Resources
- [Related documentation link]
- [Tutorial link]
- [Video tutorial link]
```

### Tutorial Template

```markdown
# Tutorial: [Title]

## Overview
[What you'll build and learn]

## Prerequisites
- [Skill/knowledge required 1]
- [Skill/knowledge required 2]
- [Tool/software required]

## Time Estimate
[How long this tutorial takes]

## Step 1: [First Step]

### Objective
[What we're accomplishing]

### Instructions
[Detailed steps with code examples]

\`\`\`python
# Code example with explanation
def example():
    return "result"
\`\`\`

### Expected Output
[What the user should see]

---

## Step 2: [Second Step]
[Continue pattern...]

## Conclusion
[Summary of what was accomplished]

## Next Steps
[Where to go from here]

## Additional Resources
- [Links to related content]
```

### README Template

```markdown
# [Project Name]

[Short description of what this project does]

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Contributing](#contributing)
- [License](#license)

## Description
[Detailed description of the project]

## Installation

\`\`\`bash
# Installation commands
\`\`\`

## Usage

### Basic Usage
\`\`\`python
# Example code
\`\`\`

### Advanced Configuration
[Configuration options]

## API Reference
[Link to detailed API docs or brief reference]

## Development

### Setup
\`\`\`bash
# Development setup commands
\`\`\`

### Running Tests
\`\`\`bash
# Test commands
\`\`\`

## Contributing
[Guidelines for contributors]

## License
[License information]

## Acknowledgments
[Credits and attributions]
```

### Architecture Documentation Template

```markdown
# [System] Architecture

## Overview
[High-level description of the system]

## Architecture Diagram
[Mermaid diagram or ASCII art showing structure]

## Components

### [Component Name]
**Purpose:** [What this component does]
**Technology:** [Technology stack]
**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]

**Key Classes/Modules:**
- `ClassName`: [Purpose]
- `ModuleName`: [Purpose]

---

## Data Flow

\`\`\`
[Diagram showing data flow between components]
\`\`\`

## Design Decisions

### [Decision 1]: [Choice Made]
**Rationale:** [Why this decision was made]
**Trade-offs:** [What was traded for this choice]
**Alternatives Considered:** [Other options evaluated]

---

## Scalability Considerations
[How the system scales]

## Security Considerations
[Security measures and considerations]

## Deployment Architecture
[Production deployment structure]
```

## Writing Guidelines

### General Principles

**Clarity:**
- Use simple, direct language
- Avoid jargon unless necessary (then define it)
- One concept per paragraph
- Use active voice

**Structure:**
- Start with overview/summary
- Group related information
- Use consistent formatting
- Include table of contents for long docs

**Accuracy:**
- Verify technical details
- Test code examples
- Update regularly
- Version your documentation

### Code Examples

**DO:**
- Include imports in examples
- Show complete, runnable snippets
- Add comments explaining key lines
- Show expected output
- Handle errors appropriately

**DON'T:**
- Use placeholder code without explanation
- Omit critical setup steps
- Assume environment configuration

### Formatting Best Practices

**Headings:**
- Use `#` for title
- Use `##` for major sections
- Use `###` for subsections
- Keep headings descriptive and concise

**Lists:**
- Use bullet lists for options/items
- Use numbered lists for steps
- Nest lists appropriately (max 3 levels)

**Code Blocks:**
- Specify language for syntax highlighting
- Keep examples under 50 lines if possible
- Break long examples into multiple blocks

**Tables:**
- Use for structured data
- Include header row
- Keep width manageable (max 6 columns)

**Emphasis:**
- Use **bold** for key terms
- Use `code` for inline code
- Use > for block quotes sparingly
- Avoid ALL CAPS

## Examples

### Example 1: Writing API Docs

**Request:** "Document the user authentication API"

**Approach:**
1. Read the auth module code
2. Identify all endpoints
3. Test each endpoint to verify behavior
4. Write documentation with examples
5. Include error scenarios

### Example 2: Writing a Tutorial

**Request:** "Create a 'Getting Started' tutorial for the SDK"

**Approach:**
1. Identify minimum viable use case
2. Break into sequential steps
3. Write and test each step
4. Add troubleshooting section
5. Include links to advanced topics

### Example 3: Updating README

**Request:** "Improve the project README"

**Approach:**
1. Review current README
2. Identify missing sections
3. Add quick start guide
4. Include example usage
5. Add contribution guidelines
