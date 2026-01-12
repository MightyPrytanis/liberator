"""
Platform detector - automatically detects which platform extractor to use.
"""

from pathlib import Path
from typing import Optional, Type
from .extractor import BaseExtractor
from ..extractors import Base44Extractor, ReplitExtractor, GenericExtractor


class PlatformDetector:
    """Detects the platform of a source project."""
    
    EXTRACTORS = [
        Base44Extractor,
        ReplitExtractor,
        GenericExtractor,  # Always last as fallback
    ]
    
    @classmethod
    def detect_platform(cls, source_path: str) -> Type[BaseExtractor]:
        """Detect which extractor to use for the source path."""
        for extractor_class in cls.EXTRACTORS:
            try:
                extractor = extractor_class(source_path)
                if extractor.detect():
                    return extractor_class
            except Exception:
                continue
        
        # Fallback to generic
        return GenericExtractor
    
    @classmethod
    def get_extractor(cls, source_path: str) -> BaseExtractor:
        """Get an extractor instance for the source path."""
        extractor_class = cls.detect_platform(source_path)
        return extractor_class(source_path)
