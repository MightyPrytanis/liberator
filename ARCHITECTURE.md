# Liberator Architecture

## Overview

Liberator is built with a modular, extensible architecture that separates concerns into distinct components:

1. **Extractors** - Platform-specific extraction logic
2. **Analyzers** - Code and dependency analysis
3. **Exporters** - Portable format generation
4. **Utilities** - Reverse engineering and substitution tools

## Component Architecture

```
liberator/
├── core/                    # Core abstractions and utilities
│   ├── extractor.py        # Base extractor class
│   ├── platform_detector.py # Auto-detection logic
│   └── utils.py            # Shared utilities
│
├── extractors/              # Platform-specific extractors
│   ├── base44.py          # Base44 platform extractor
│   ├── replit.py          # Replit platform extractor
│   └── __init__.py        # Extractor registry
│
├── analyzer/               # Analysis engines
│   ├── dependency_analyzer.py # Dependency detection
│   └── code_analyzer.py   # Code structure analysis
│
├── portability/            # Portability layer
│   └── exporter.py        # Portable format exporter
│
├── utils/                  # Advanced utilities
│   ├── reverse_engineer.py # Reverse engineering tools
│   └── substitution.py    # Code substitution utilities
│
└── cli.py                  # Command-line interface
```

## Data Flow

```
Source Project
    │
    ├─→ Platform Detector
    │       │
    │       └─→ Select Extractor (Base44/Replit/Generic)
    │
    ├─→ Extractor
    │       │
    │       ├─→ Extract Files
    │       ├─→ Extract Dependencies
    │       └─→ Extract Configuration
    │
    ├─→ Dependency Analyzer
    │       │
    │       ├─→ Analyze Code Imports
    │       ├─→ Normalize Dependencies
    │       └─→ Categorize by Type
    │
    ├─→ Code Analyzer
    │       │
    │       ├─→ Parse Code Structure
    │       ├─→ Identify Functions/Classes
    │       └─→ Detect Patterns
    │
    └─→ Portable Exporter
            │
            ├─→ Generate Config Files
            ├─→ Create Docker Setup
            ├─→ Generate Documentation
            └─→ Export All Files
```

## Core Components

### 1. Base Extractor (`core/extractor.py`)

Abstract base class for all extractors. Defines the interface:

- `detect()` - Detect if extractor can handle the source
- `extract()` - Extract files, dependencies, and config
- Returns `ExtractionResult` with all extracted data

### 2. Platform Extractors (`extractors/`)

Platform-specific implementations:

- **Base44Extractor**: Handles Base44 projects
  - Detects `.base44` config files
  - Extracts Base44-specific metadata
  - Preserves project structure

- **ReplitExtractor**: Handles Replit projects
  - Detects `.replit` and `replit.nix` files
  - Extracts Replit configuration
  - Handles multiple language runtimes

- **GenericExtractor**: Fallback for unknown platforms
  - Extracts all files recursively
  - Attempts to detect dependencies from common config files
  - Works with any directory structure

### 3. Dependency Analyzer (`analyzer/dependency_analyzer.py`)

Analyzes code to find dependencies:

- Parses import statements (Python, JavaScript, Go, Rust)
- Filters out standard library modules
- Normalizes dependencies by package manager type
- Categorizes: npm, pip, go, cargo

### 4. Code Analyzer (`analyzer/code_analyzer.py`)

Deep code structure analysis:

- Language detection from file extensions
- AST parsing (Python) or regex (other languages)
- Extracts functions, classes, imports, exports
- Identifies code patterns

### 5. Portable Exporter (`portability/exporter.py`)

Creates portable project structure:

- Generates standard config files (package.json, requirements.txt, etc.)
- Creates Dockerfile and docker-compose.yml
- Generates .env.example template
- Creates comprehensive README.md
- Adds LICENSE and .gitignore

### 6. Reverse Engineering Utils (`utils/reverse_engineer.py`)

Advanced analysis tools:

- Detects API endpoints
- Finds database connections
- Identifies secrets and API keys
- Suggests open-source alternatives

### 7. Code Substitution (`utils/substitution.py`)

Code modification utilities:

- Pattern-based code substitution
- Suggests open-source alternatives
- Replaces proprietary services

## Extension Points

### Adding a New Platform Extractor

1. Create new file in `extractors/`:
```python
from ..core.extractor import BaseExtractor, ExtractionResult

class NewPlatformExtractor(BaseExtractor):
    def detect(self) -> bool:
        # Check for platform-specific markers
        return (self.source_path / '.newplatform').exists()
    
    def extract(self) -> ExtractionResult:
        result = ExtractionResult()
        # Extract files, dependencies, config
        return result
```

2. Register in `extractors/__init__.py`
3. Add to `PlatformDetector.EXTRACTORS` list

### Adding a New Analyzer

Create analyzer in `analyzer/`:
```python
class CustomAnalyzer:
    def analyze(self, code: str) -> Dict:
        # Your analysis logic
        return results
```

### Custom Export Formats

Extend `PortableExporter`:
```python
class CustomExporter(PortableExporter):
    def export(self, result: ExtractionResult):
        # Custom export logic
        super().export(result)  # Or override completely
```

## Design Principles

1. **Modularity** - Each component is independent and testable
2. **Extensibility** - Easy to add new platforms and features
3. **No External Dependencies** - Uses only Python standard library
4. **Fail-Safe** - Graceful degradation when extraction fails
5. **Transparency** - All operations are logged and auditable

## Error Handling

- Extractors catch and report errors without crashing
- Missing files are logged as warnings
- Invalid configurations are skipped with warnings
- Extraction continues even if some files fail

## Performance Considerations

- File reading is lazy (only when needed)
- Large files are handled with streaming where possible
- Analysis can be parallelized (future enhancement)
- Caching of analysis results (future enhancement)

## Security Considerations

- Secrets are detected and masked in output
- Environment variables are templated, not copied
- No code execution during extraction
- All file operations are read-only on source

## Testing Strategy

- Unit tests for each component
- Integration tests for full workflows
- Test fixtures for each supported platform
- Mock extractors for testing exporters

## Future Enhancements

1. **Parallel Processing** - Multi-threaded extraction
2. **Caching** - Cache analysis results
3. **GUI** - Graphical interface
4. **Cloud Extraction** - Direct API access to platforms
5. **CI/CD Integration** - Automated liberation pipelines
6. **Database Migration** - Extract and migrate databases
7. **Version Control** - Git history extraction

---

This architecture ensures Liberator is maintainable, extensible, and reliable.
