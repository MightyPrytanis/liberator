#!/usr/bin/env python3
"""
Test script for Liberator - creates a test project and liberates it.
"""

import os
import tempfile
import shutil
from pathlib import Path

from liberator.core.platform_detector import PlatformDetector
from liberator.extractors.replit import ReplitExtractor
from liberator.portability.exporter import PortableExporter


def create_test_replit_project(base_path: Path):
    """Create a test Replit project structure."""
    project_path = base_path / 'test-replit-project'
    project_path.mkdir()
    
    # Create .replit file
    replit_config = {
        "run": "python main.py",
        "language": "python3"
    }
    import json
    (project_path / '.replit').write_text(json.dumps(replit_config))
    
    # Create main.py
    main_py = """import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Replit!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
    (project_path / 'main.py').write_text(main_py)
    
    # Create requirements.txt
    (project_path / 'requirements.txt').write_text('flask==2.3.0\n')
    
    # Create .env
    (project_path / '.env').write_text('PORT=5000\nSECRET_KEY=test123\n')
    
    return project_path


def test_extraction():
    """Test the extraction process."""
    print("🧪 Testing Liberator...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create test project
        print("📝 Creating test Replit project...")
        test_project = create_test_replit_project(tmp_path)
        
        # Test platform detection
        print("🔍 Testing platform detection...")
        extractor_class = PlatformDetector.detect_platform(str(test_project))
        assert extractor_class == ReplitExtractor, f"Expected ReplitExtractor, got {extractor_class}"
        print("✓ Platform detection works")
        
        # Test extraction
        print("📦 Testing extraction...")
        extractor = ReplitExtractor(str(test_project))
        result = extractor.extract()
        
        assert len(result.files) > 0, "No files extracted"
        assert 'main.py' in result.files, "main.py not extracted"
        assert len(result.dependencies) > 0, "No dependencies found"
        print(f"✓ Extracted {len(result.files)} files and {len(result.dependencies)} dependencies")
        
        # Test export
        print("📤 Testing export...")
        output_path = tmp_path / 'liberated'
        exporter = PortableExporter(str(output_path))
        export_result = exporter.export(result)
        
        assert export_result['status'] == 'success', "Export failed"
        assert (output_path / 'main.py').exists(), "main.py not exported"
        assert (output_path / 'requirements.txt').exists(), "requirements.txt not generated"
        assert (output_path / 'README.md').exists(), "README.md not generated"
        assert (output_path / 'LICENSE').exists(), "LICENSE not generated"
        print("✓ Export successful")
        
        print("\n✅ All tests passed!")


if __name__ == '__main__':
    try:
        test_extraction()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
