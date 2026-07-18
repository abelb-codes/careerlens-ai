# ai/parser/docx_parser.py
"""
DOCX parser module for extracting raw text from Microsoft Word documents.
"""

from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Optional

from ai.parser.types import ParserResult

logger = logging.getLogger(__name__)


def parse_docx(file_path: str | Path) -> ParserResult:
    """
    Extract text and metadata from a DOCX file.

    Parameters
    ----------
    file_path : str | Path
        The path to the DOCX file.

    Returns
    -------
    ParserResult
        A dictionary matching the Parser Contract.
    """
    path = Path(file_path).resolve()
    result: ParserResult = {
        "success": False,
        "file_name": path.name,
        "file_type": "docx",
        "pages": 0,
        "text": "",
        "error": None,
    }

    try:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        docx_module = importlib.import_module("docx")
        Document = getattr(docx_module, "Document")
        doc = Document(str(path))
        extracted_text_parts = []

        # 1. Extract standard paragraphs
        for p in doc.paragraphs:
            p_text = p.text.strip()
            if p_text:
                extracted_text_parts.append(p_text)

        # 2. Extract table cell content
        for table in doc.tables:
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    if cell_text:
                        # Avoid duplicating text from merged cells in the same row
                        if not row_text or row_text[-1] != cell_text:
                            row_text.append(cell_text)
                if row_text:
                    extracted_text_parts.append(" | ".join(row_text))

        result["text"] = "\n".join(extracted_text_parts).strip()
        result["success"] = True

    except Exception as exc:
        logger.exception("Failed to parse DOCX file at %s", path)
        result["success"] = False
        result["error"] = str(exc)

    return result
