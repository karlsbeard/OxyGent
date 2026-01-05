---
name: summarizer
description: Summarize long documents, articles, and texts
version: "1.0.0"
author: OxyGent Team

allowed-tools:
  - Read
  - Glob
---

# Summarizer Skill

## Overview

This skill creates concise, accurate summaries of long documents, articles, and texts while preserving key information and context.

## Instructions

When this skill is activated, follow these steps to create effective summaries:

### Step 1: Understand the Summarization Request

1. Identify the document(s) to summarize
2. Determine the desired summary length (short, medium, detailed)
3. Identify the focus (general overview, specific points, action items)
4. Check the document type (article, report, meeting notes, code, etc.)

### Step 2: Read and Analyze the Document

Use the Read tool to examine the content:

**For Articles/Blog Posts:**
- Identify the main thesis or argument
- Note key supporting points
- Extract conclusions and call-to-action

**For Reports/White Papers:**
- Find the executive summary
- Identify methodology and key findings
- Note recommendations

**For Meeting Notes/Transcripts:**
- Identify attendees and their roles
- Extract decisions made
- Note action items with owners
- Highlight unresolved issues

**For Technical Documentation:**
- Identify purpose and scope
- Extract key concepts and definitions
- Note important procedures or commands

### Step 3: Create the Summary

Use the appropriate format based on document type and user needs:

**General Summary Format:**
```markdown
# Summary: [Document Title]

## Overview
[1-2 sentence capturing the main point]

## Key Points
1. [First key point with brief detail]
2. [Second key point]
3. [Continue as needed...]

## Conclusion
[Main conclusion or outcome]

## Tags/Keywords
[Relevant tags for categorization]
```

**Article Summary Format:**
```markdown
# Article Summary: [Title]

**Source:** [Author/Publication]
**Date:** [Publication date]
**Length:** [Original word count]

## Main Idea
[The core argument or thesis]

## Key Points
- [Point 1]
- [Point 2]
- [Continue...]

## Notable Quotes
> "[Important quote that captures essence]"

## Conclusion
[Author's conclusion or main takeaway]
```

**Meeting Notes Summary Format:**
```markdown
# Meeting Summary: [Meeting Title]

**Date:** [Date]
**Attendees:** [List]

## Decisions Made
1. [Decision 1] - [Brief context]
2. [Decision 2]

## Action Items
| Task | Owner | Due Date |
|------|-------|----------|
| [Task 1] | [Name] | [Date] |
| [Task 2] | [Name] | [Date] |

## Discussion Points
- [Topic 1]: [Brief summary]
- [Topic 2]: [Brief summary]

## Next Steps
[What happens next]
```

**Technical Document Summary:**
```markdown
# Document Summary: [Title]

**Type:** [API Guide/Tutorial/Reference]
**Audience:** [Target audience level]

## Purpose
[What this document explains]

## Key Concepts
1. **[Concept 1]:** [Definition]
2. **[Concept 2]:** [Definition]

## Important Commands/Procedures
```[language]
[Key code snippets or commands]
```

## Quick Reference
[Essential information in condensed form]
```

### Step 4: Quality Check

Before delivering the summary, verify:
- [ ] Summary is objective (no personal opinions)
- [ ] Key information is preserved
- [ ] Summary is significantly shorter than original
- [ ] Important names, dates, and numbers are accurate
- [ ] Tone matches the original document
- [ ] No critical information was omitted

## Summary Length Guidelines

**Short Summary (1-2 paragraphs):**
- Use for quick overview
- Include main idea only
- ~100-150 words

**Medium Summary (bullet points):**
- Use for balanced detail
- Include 3-5 key points
- ~200-300 words

**Detailed Summary (structured):**
- Use for comprehensive understanding
- Include all major sections
- ~400-600 words

## Best Practices

**DO:**
- Start with the most important information
- Use the same tone as the original
- Preserve critical data points, names, dates
- Use bullet points for readability
- Quote key phrases when they add value
- Attribute opinions to their sources
- Maintain factual accuracy

**DON'T:**
- Introduce information not in the original
- Mix personal opinions with the summary
- Change the meaning of statements
- Omit critical findings or conclusions
- Make claims without source attribution
- Over-simplify complex topics
- Ignore the document's structure

## Examples

### Example 1: Article Summary

**Original:** A 2000-word article about remote work trends

**Summary:**
```markdown
# Article Summary: The Future of Remote Work

**Source:** Harvard Business Review
**Date:** March 2024

## Main Idea
Remote work is shifting from a pandemic necessity to a permanent feature
of modern work, with companies adopting hybrid models as the long-term standard.

## Key Points
- **Hybrid Dominance:** 73% of companies plan permanent hybrid arrangements
- **Productivity Paradox:** Individual productivity up 15%, but collaboration challenges persist
- **Geographic Dispersion:** Companies hiring talent across 3+ time zones on average
- **Office Reinvention:** Offices becoming collaboration hubs, not primary workspaces

## Conclusion
The future is hybrid, and success requires intentional design of both
in-office and remote work experiences.
```

### Example 2: Technical Document Summary

**Original:** API documentation (50 pages)

**Summary:**
```markdown
# API Summary: Payment Processing Service

## Purpose
RESTful API for processing payments, handling refunds, and managing
customer payment methods.

## Key Endpoints

### Payments
- `POST /payments` - Create payment
- `GET /payments/{id}` - Retrieve payment status
- `POST /payments/{id}/refund` - Process refund

### Payment Methods
- `POST /customers/{id}/payment-methods` - Add card
- `DELETE /payment-methods/{id}` - Remove card

## Quick Reference
**Authentication:** Bearer token in header
**Timeout:** 30 seconds for payment operations
**Webhooks:** Supported for payment status updates
```

## Special Considerations

**For Very Long Documents:**
- Consider providing both short and detailed summaries
- Offer to summarize specific sections if full summary is still too long
- Use progressive disclosure: overview first, details on request

**For Multiple Documents:**
- Summarize each document separately
- Then provide a synthesized summary of all documents
- Note relationships and contradictions between documents

**For Code:**
- Focus on purpose and functionality
- Note key algorithms or patterns used
- Don't summarize line-by-line; explain architectural intent

**For Non-English Text:**
- Maintain the original language in the summary
- If user requests English summary, provide both original and translated
