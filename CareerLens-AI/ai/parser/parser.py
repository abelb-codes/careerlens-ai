# ai/parser/parser.py
"""
Unified Resume Parser orchestrator.

Acts as the entry point for parsing resumes, detecting file formats,
and returning normalized parser results.
"""

from __future__ import annotations

import logging
from pathlib import Path

from ai.parser.docx_parser import parse_docx
from ai.parser.pdf_parser import parse_pdf
from ai.parser.types import ParserResult

logger = logging.getLogger(__name__)


def parse_resume(file_path: str | Path) -> ParserResult:
    """
    Parse an uploaded resume file and return extracted text and metadata.

    The returned dictionary matches the Parser Contract:
    {
        "success": bool,
        "file_name": str,
        "file_type": str,
        "pages": int,
        "text": str,
        "error": Optional[str]
    }

    Parameters
    ----------
    file_path : str | Path
        Path to the resume file (PDF or DOCX).

    Returns
    -------
    ParserResult
        A dictionary conforming to the Parser Contract.
    """
    path = Path(file_path).resolve()
    
    # Base response matching contract schema
    result: ParserResult = {
        "success": False,
        "file_name": path.name,
        "file_type": "",
        "pages": 0,
        "text": "",
        "error": None,
    }

    try:
        if not path.exists():
            error_msg = f"File not found: {path}"
            logger.error(error_msg)
            result["error"] = error_msg
            return result

        if not path.is_file():
            error_msg = f"Path is not a file: {path}"
            logger.error(error_msg)
            result["error"] = error_msg
            return result

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            result["file_type"] = "pdf"
            return parse_pdf(path)
        elif suffix in (".docx", ".doc"):
            result["file_type"] = "docx"
            return parse_docx(path)
        else:
            error_msg = f"Unsupported file extension: {suffix}. Only PDF and DOCX are supported."
            logger.error(error_msg)
            result["file_type"] = suffix.lstrip(".")
            result["error"] = error_msg
            return result

    except Exception as exc:
        logger.exception("Unexpected error orchestrating resume parse for %s", path)
        result["success"] = False
        result["error"] = f"Unexpected orchestration error: {exc}"
        return result
