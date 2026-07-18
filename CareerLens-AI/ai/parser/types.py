"""
Common parser type definitions and contract models.
"""

from __future__ import annotations

from typing import Optional, TypedDict


class ParserResult(TypedDict):
    """Typed dictionary representing the parser contract response."""

    success: bool
    file_name: str
    file_type: str
    pages: int
    text: str
    error: Optional[str]
