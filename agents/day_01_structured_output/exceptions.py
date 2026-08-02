"""
Custom exceptions for Day 01 agent.
"""

class StructuredExtractionError(Exception):
    """Base exception for extraction workflow failures."""
    pass

class SchemaValidationError(StructuredExtractionError):
    """Raised when output fails Pydantic schema validation."""
    pass

class MaxRetriesExceededError(StructuredExtractionError):
    """Raised when maximum retry count is reached without successful validation."""
    pass
