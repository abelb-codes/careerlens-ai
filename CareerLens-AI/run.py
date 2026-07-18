#!/usr/bin/env python3
"""HTTP service for the CareerLens AI analysis engine."""

from __future__ import annotations

import json
import logging
import os
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

# Configure structured logging before any imports
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("careerlens.ai_service")
SERVICE_TOKEN = os.getenv("AI_SERVICE_TOKEN", "")

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai.pipeline.applicant_pipeline import ApplicantPipeline


class AnalysisRequestHandler(BaseHTTPRequestHandler):

    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024
    ALLOWED_SUFFIXES = {".pdf", ".docx"}

    def do_GET(self) -> None:  # noqa: N802
        if not self._is_authorized():
            return
        if self.path == "/health":
            self._send_json(200, {"status": "ok", "service": "CareerLens AI Engine"})
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self) -> None:  # noqa: N802
        if not self._is_authorized():
            return
        if self.path != "/analyze":
            self._send_json(404, {"error": "Not Found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "Invalid Content-Length"})
            return

        filename = Path(self.headers.get("X-Filename", "")).name
        suffix = Path(filename).suffix.lower()
        if not filename or suffix not in self.ALLOWED_SUFFIXES:
            self._send_json(400, {"error": "X-Filename must name a PDF or DOCX file"})
            return
        if not 0 < content_length <= self.MAX_DOCUMENT_SIZE:
            self._send_json(413, {"error": "Document must be between 1 byte and 10MB"})
            return

        document_bytes = self.rfile.read(content_length)
        if len(document_bytes) != content_length:
            self._send_json(400, {"error": "Incomplete request body"})
            return

        job_profile = {
            "title": "Software Engineer",
            "required_skills": [],
            "experience_level": "mid",
        }

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            temp_file.write(document_bytes)
            document_path = temp_file.name

        logger.info("Analyzing document: %s", filename)
        try:
            pipeline = ApplicantPipeline()
            result = pipeline.process_applicant(document_path, job_profile, config={})
        except Exception as exc:
            logger.exception("Pipeline failed for %s: %s", filename, exc)
            self._send_json(500, {"error": "Resume analysis failed"})
            return
        finally:
            try:
                os.unlink(document_path)
            except OSError:
                logger.warning("Could not remove temporary file for %s", filename)

        response = build_analysis_response(result)
        logger.info(
            "Analysis complete — ATS: %s, Score: %s, Skills: %d",
            response.get("ats_score"),
            response.get("resume_score"),
            len(response.get("skills", [])),
        )
        self._send_json(200, response)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        # Delegate HTTP access logs to the Python logger instead of stderr
        logger.debug(format, *args)

    def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _is_authorized(self) -> bool:
        """Require a shared token only when one is configured for deployment."""
        if not SERVICE_TOKEN or self.headers.get("Authorization") == f"Bearer {SERVICE_TOKEN}":
            return True
        self._send_json(401, {"error": "Unauthorized"})
        return False


def build_analysis_response(result: dict[str, Any]) -> dict[str, Any]:
    resume_profile = result.get("resume_profile") or {}
    resume_analysis = result.get("resume_analysis") or {}
    suggestions = resume_analysis.get("suggestions") or []
    interview_questions = result.get("interview_questions") or []

    return {
        "ats_score": int(resume_analysis.get("ats_score", 0) or 0),
        "resume_score": int(resume_analysis.get("resume_score", 0) or 0),
        "skills": resume_profile.get("skills") or [],
        "experience": resume_profile.get("experience") or [],
        "education": resume_profile.get("education") or [],
        "strengths": resume_analysis.get("strengths") or [],
        "weaknesses": resume_analysis.get("weaknesses") or [],
        "suggestions": suggestions,
        "recommendations": suggestions,
        "interview_questions": interview_questions,
        "matching_result": result.get("matching_result") or {},
        "candidate_report": result.get("candidate_report"),
        "error": result.get("error", ""),
    }


def main() -> None:
    port = int(os.getenv("AI_SERVICE_PORT", "8001"))
    server = ThreadingHTTPServer(("0.0.0.0", port), AnalysisRequestHandler)
    logger.info("CareerLens AI Engine listening on http://0.0.0.0:%d", port)
    logger.info("Endpoints: POST /analyze | GET /health")
    server.serve_forever()


if __name__ == "__main__":
    main()
