"""Custom exceptions for CareerLens AI pipeline orchestration."""

from __future__ import annotations


class PipelineError(Exception):
    """Base exception for pipeline orchestration failures."""


class InvalidPipelineInputError(PipelineError):
    """Raised when pipeline input validation fails."""


class PipelineExecutionError(PipelineError):
    """Raised when pipeline execution fails during orchestration."""
