"""
Core utilities and base classes.
"""

from .extractor import BaseExtractor, ExtractionResult
from .platform_detector import PlatformDetector

__all__ = ['BaseExtractor', 'ExtractionResult', 'PlatformDetector']
