# ai/parser/__init__.py
"""
Resume parsing subpackage.
Exposes the high-level parse_resume orchestrator.
"""

from ai.parser.parser import parse_resume
from ai.parser.types import ParserResult

__all__ = ["parse_resume", "ParserResult"]
