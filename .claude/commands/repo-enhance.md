---
name: repo-enhance
description: Deep repository analysis with competitive research to brainstorm enhancement ideas using DeepWiki, web search, and multi-agent exploration
category: orchestration
complexity: advanced
mcp-servers: [deepwiki, open-websearch, sequential, serena]
personas: [architect, analyzer, deep-research-agent]
argument-hint: "[--focus core|agents|tools|docs] [--compare langchain,langgraph,autogen] [--depth quick|standard|deep]"
---

# /repo-enhance - Repository Enhancement Brainstorming

> **Context Framework Note**: This skill performs comprehensive repository analysis by combining codebase exploration, DeepWiki documentation extraction, and competitive research on popular AI agent frameworks to generate actionable enhancement ideas.

## Triggers
- Repository improvement planning
- Feature gap analysis requests
- Competitive analysis for AI agent frameworks
- Architecture enhancement brainstorming
- "How can we improve this repo" questions

## Context Trigger Pattern
```
/repo-enhance [--focus area] [--compare frameworks] [--depth level]
```

## Parameters
- `--focus`: Target analysis area (core|agents|tools|docs|all) - default: all
- `--compare`: Comma-separated list of frameworks to research (default: claude-agent,codex,langchain,langgraph,autogen,crewai)
- `--depth`: Analysis depth (quick|standard|deep) - default: standard

## Behavioral Flow

### Phase 1: Repository Overview (15% effort)
**Objective**: Understand current codebase structure and capabilities

**Actions**:
1. Use Explore agent to analyze repository structure:
   - Identify core modules and their purposes
   - Map architecture patterns (agents, tools, LLMs, memory)
   - Document existing features and capabilities
   - Note code quality patterns and testing coverage

2. Create structured overview:
   ```yaml
   current_state:
     architecture: [components]
     features: [capabilities]
     patterns: [design patterns used]
     gaps: [identified limitations]
   ```

### Phase 2: DeepWiki Analysis (20% effort)
**Objective**: Extract comprehensive documentation from the repository

**Actions**:
1. Use `mcp__mcp-deepwiki__deepwiki_fetch` with:
   - Current repository URL/path
   - `maxDepth: 1` for comprehensive coverage
   - `mode: aggregate` for unified analysis

2. Extract key insights:
   - API surface and interfaces
   - Usage patterns and examples
   - Documentation gaps
   - Architecture decisions

### Phase 3: Competitive Research (30% effort)
**Objective**: Analyze popular AI agent frameworks for feature inspiration

**Research Targets** (parallel execution):
- **Claude Agent SDK**: Official Anthropic agent patterns
- **OpenAI Codex/Assistants**: OpenAI's agent architecture
- **LangChain**: Popular LLM orchestration framework
- **LangGraph**: Graph-based agent workflows
- **AutoGen**: Microsoft's multi-agent framework
- **CrewAI**: Role-based agent collaboration
- **Semantic Kernel**: Microsoft's AI orchestration

**Actions**:
1. Use `mcp__open-websearch__search` for each framework:
   - Search: "[framework] agent architecture 2024"
   - Search: "[framework] features capabilities"
   - Search: "[framework] vs alternatives comparison"

2. Use `mcp__open-websearch__fetchGithubReadme` for key repos:
   - langchain-ai/langchain
   - langchain-ai/langgraph
   - microsoft/autogen
   - joaomdmoura/crewAI
   - anthropics/anthropic-sdk-python

3. Use `mcp__mcp-deepwiki__deepwiki_fetch` for deep analysis:
   - "langchain" - orchestration patterns
   - "langgraph" - graph-based workflows
   - "autogen" - multi-agent patterns

### Phase 4: Gap Analysis (15% effort)
**Objective**: Identify feature gaps and enhancement opportunities

**Analysis Matrix**:
```yaml
feature_comparison:
  current_repo:
    has: [list of existing features]
    missing: [features others have]
    unique: [differentiating features]

  competitors:
    langchain: [key features]
    langgraph: [key features]
    autogen: [key features]
    crewai: [key features]
```

### Phase 5: Enhancement Brainstorming (20% effort)
**Objective**: Generate prioritized enhancement ideas

**Categories**:
1. **Core Architecture Enhancements**
   - Agent orchestration patterns
   - Memory and state management
   - Tool integration improvements

2. **New Feature Ideas**
   - Graph-based workflows (inspired by LangGraph)
   - Role-based agents (inspired by CrewAI)
   - Streaming and real-time capabilities
   - Multi-modal support

3. **Developer Experience**
   - API simplification
   - Documentation improvements
   - Example and template additions
   - CLI enhancements

4. **Performance & Reliability**
   - Caching strategies
   - Error handling patterns
   - Observability and tracing
   - Testing infrastructure

## MCP Integration

### DeepWiki MCP
- **Primary Use**: Repository documentation extraction
- **Pattern**: `deepwiki_fetch(url, maxDepth=1, mode="aggregate")`
- **Output**: Comprehensive markdown documentation

### Open-WebSearch MCP
- **Primary Use**: Competitive research and trend analysis
- **Tools**:
  - `search`: Web search for framework comparisons
  - `fetchGithubReadme`: Direct GitHub README extraction
- **Pattern**: Parallel searches for efficiency

### Sequential MCP
- **Primary Use**: Complex reasoning for gap analysis and prioritization
- **Pattern**: Multi-step analysis with hypothesis testing

### Serena MCP
- **Primary Use**: Session persistence for cross-session research
- **Pattern**: Store findings for incremental updates

## Tool Coordination

### Parallel Execution Opportunities
```yaml
parallel_phase_3:
  - search: "Claude Agent SDK features 2024"
  - search: "LangChain vs LangGraph comparison"
  - search: "AutoGen multi-agent patterns"
  - search: "CrewAI role-based agents"

parallel_deepwiki:
  - deepwiki_fetch: "langchain"
  - deepwiki_fetch: "langgraph"
  - deepwiki_fetch: "autogen"
```

### Sequential Dependencies
```yaml
sequential_flow:
  1. Repository overview → identifies focus areas
  2. DeepWiki current repo → baseline documentation
  3. Competitive research → feature landscape
  4. Gap analysis → opportunities identified
  5. Brainstorming → prioritized enhancements
```

## Output Standards

### Report Generation
Save comprehensive report to: `claudedocs/repo_enhance_[timestamp].md`

### Report Structure
```markdown
# Repository Enhancement Analysis

## Executive Summary
[Key findings and top 5 recommendations]

## Current State Analysis
### Architecture Overview
### Feature Inventory
### Identified Strengths
### Current Limitations

## Competitive Landscape
### Framework Comparison Matrix
### Feature Gap Analysis
### Industry Trends

## Enhancement Recommendations

### Priority 1: Critical Improvements
[High-impact, feasible enhancements]

### Priority 2: Feature Additions
[New capabilities to consider]

### Priority 3: Long-term Vision
[Strategic architectural improvements]

## Implementation Roadmap
[Suggested sequencing and dependencies]

## Sources and References
[All researched sources with links]
```

## Examples

### Quick Analysis
```
/repo-enhance --depth quick
# Fast overview with top 3 enhancement ideas
# ~5 minutes, minimal research
```

### Standard Analysis
```
/repo-enhance
# Full analysis with competitive research
# ~15 minutes, comprehensive report
```

### Deep Competitive Analysis
```
/repo-enhance --compare langchain,langgraph,autogen,crewai --depth deep
# Extensive research on specific frameworks
# ~30 minutes, detailed comparison matrix
```

### Focused Analysis
```
/repo-enhance --focus agents --compare autogen,crewai
# Target agent orchestration patterns
# Compare with multi-agent frameworks only
```

## Boundaries

**Will:**
- Analyze current repository structure and capabilities
- Research popular AI agent frameworks for inspiration
- Generate actionable enhancement recommendations
- Provide prioritized implementation suggestions
- Create comprehensive documentation of findings

**Will Not:**
- Make changes to the codebase directly
- Implement enhancements without user approval
- Access private/proprietary framework documentation
- Make subjective quality judgments without evidence
- Recommend changes that break existing functionality
