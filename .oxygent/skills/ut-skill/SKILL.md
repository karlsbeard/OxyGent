---
name: ut-skill
description: Unit test skill for testing skill configuration and retrieval
version: "1.0.0"
author: OxyGent Team

allowed-tools:
  - Read
  - Glob
  - Grep
---

# UT Skill

## Overview

This skill is used for unit testing the OxyGent skill system. It verifies that skills can be configured and retrieved properly.

## Instructions

When this skill is activated:

1. Acknowledge the skill has been loaded
2. Confirm the skill name and description
3. Return a simple test message

## Example

**User Request:** "Test ut-skill"

**Your Response:```
UT Skill is working!

Skill Info:
- Name: ut-skill
- Description: Unit test skill for testing skill configuration and retrieval
- Version: 1.0.0
```

## Purpose

This is a test skill to verify:
- Skill configuration files are parsed correctly
- Skills can be retrieved by name
- Skill metadata is accessible
