"""OxyGent Preset Skills.

This package contains built-in skills for the OxyGent framework.
These skills are automatically discovered and available to all agents.

Available Skills:
    - code-reviewer: Review code for quality and security
    - web-researcher: Research topics on the web
    - summarizer: Summarize long documents
    - technical-writer: Write technical documentation
"""

from pathlib import Path

__all__ = ["PRESET_SKILLS_DIR"]

PRESET_SKILLS_DIR = Path(__file__).parent
