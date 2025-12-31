---
name: web-researcher
description: Research topics on the web and synthesize findings
version: "1.0.0"
author: OxyGent Team

allowed-tools:
  - Read
  - HttpTool

model: claude-3-opus
timeout: 180
---

# Web Researcher Skill

## Overview

This skill conducts web research on specified topics, synthesizes findings from multiple sources, and provides comprehensive, well-structured reports.

## Instructions

When this skill is activated, follow these steps to conduct thorough web research:

### Step 1: Understand the Research Request

1. Parse the user's query to identify the core topic
2. Determine the scope (broad overview vs. specific details)
3. Identify key aspects to research
4. Determine the depth of research needed

### Step 2: Plan the Research Strategy

Break down the research into logical sub-topics:

**For broad topics:**
- Definitions and basic concepts
- Current state of the field
- Key developments and trends
- Expert opinions and consensus
- Controversies or debates

**For specific questions:**
- Direct answer if available
- Supporting evidence
- Alternative viewpoints
- Recent updates

### Step 3: Conduct Research

Use the HttpTool to fetch information from web sources:

**Search Strategy:**
1. Start with authoritative sources (official documentation, research papers)
2. Check recent articles and news (last 1-2 years)
3. Look for expert consensus and peer-reviewed sources
4. Cross-reference information across multiple sources
5. Note any contradictions or evolving information

**Source Quality Assessment:**
- Prioritize: official docs, academic sources, established publications
- Use cautiously: blogs, forums, social media
- Verify: check multiple sources for claims
- Note the date of information (outdated info may be misleading)

### Step 4: Synthesize Findings

Organize the information into a coherent report:

```markdown
# Research Report: [Topic]

## Executive Summary
[2-3 sentence overview of key findings]

## Key Findings

### 1. [First major finding]
- Detail: [explanation]
- Source: [attribution]
- Significance: [why it matters]

### 2. [Second major finding]
[Continue as needed...]

## Detailed Information

### Background & Context
[Historical context, definitions, foundational concepts]

### Current State
[Present situation, recent developments, status as of [date]]

### Different Perspectives
[If applicable, present varying viewpoints]

## Notable Sources
1. [Source name] - [URL] - [Key information]
2. [Continue as needed...]

## Limitations & Caveats
[What couldn't be determined, what to verify, date sensitivity]

## Recommendations for Further Research
[What to explore next based on gaps found]
```

### Step 5: Quality Check

Before delivering the report, verify:
- [ ] Information is current (note dates)
- [ ] Multiple sources agree on key facts
- [ ] Contradictions are noted
- [ ] Claims are attributed to sources
- [ ] The report directly answers the original query

## Research Guidelines

### Handling Different Types of Queries

**Factual Questions (e.g., "What is the population of Japan?")**
- Find current, authoritative data
- Note the year of the data
- Provide source links

**Conceptual Questions (e.g., "How does machine learning work?")**
- Start with clear definition
- Explain in accessible terms
- Provide examples
- Reference reputable explanations

**Comparison Questions (e.g., "PostgreSQL vs MySQL")**
- Use structured comparison format
- Cover key dimensions (performance, features, cost)
- Note use cases where each excels
- Avoid bias; present strengths of each

**Current Events (e.g., "Latest AI developments")**
- Prioritize recent sources (last 3-6 months)
- Note that information may change
- Distinguish between facts and speculation

**Technical/Scientific Topics**
- Prioritize peer-reviewed sources
- Note scientific consensus vs. emerging research
- Explain technical concepts clearly

### Source Credibility Guidelines

**High Credibility:**
- Official documentation (API docs, standards bodies)
- Peer-reviewed academic papers
- Reputable news organizations with editorial standards
- Government sources (for official data)
- Industry-recognized experts

**Medium Credibility:**
- Technical blogs by known experts
- Industry publications
- Well-maintained wikis (with verification)

**Low Credibility (verify with other sources):**
- Personal blogs
- Forum posts
- Social media
- Anonymous sources

### Avoiding Common Pitfalls

**Don't:**
- Present speculation as fact
- Rely on a single source
- Ignore information that contradicts your assumptions
- Overstate certainty on evolving topics
- Plagiarize; synthesize and attribute

**Do:**
- Distinguish between established facts and developing information
- Note when sources disagree
- Admit limitations in the available information
- Provide source attribution
- Update information with dates

## Examples

### Example 1: Technology Research

**User Request:** "Research Rust programming language"

**Research Plan:**
1. Official Rust documentation (what is Rust, key features)
2. Recent articles on Rust adoption (current state)
3. Comparison with C++ (context)
4. Use cases and industry adoption

### Example 2: Current Event Research

**User Request:** "What's happening with AI regulation?"

**Research Plan:**
1. Recent regulatory developments (EU AI Act, US executive orders)
2. Industry response and positions
3. Expert opinions on implications
4. Timeline of upcoming changes

### Example 3: Practical Decision Support

**User Request:** "Which JavaScript framework should I learn in 2024?"

**Research Plan:**
1. Current popularity and adoption stats
2. Use cases for each major framework
3. Industry demand and job market
4. Learning curve opinions
5. Community and ecosystem health

## Output Format Guidelines

- Use clear headings and structure
- Prioritize most important information first
- Use bullet points for readability
- Include source links when relevant
- Note the date of information
- Acknowledge uncertainty or evolving situations
