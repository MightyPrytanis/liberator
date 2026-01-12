"""
Platform-specific extractors.
"""

from .base44 import Base44Extractor
from .replit import ReplitExtractor
from ..core.extractor import GenericExtractor

__all__ = ['Base44Extractor', 'ReplitExtractor', 'GenericExtractor']
