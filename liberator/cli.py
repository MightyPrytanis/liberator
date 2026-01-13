#!/usr/bin/env python3
"""
Liberator CLI - Command-line interface for liberating apps.
"""

import argparse
import sys
import tempfile
from pathlib import Path
from typing import Optional

from .core.platform_detector import PlatformDetector
from .portability.exporter import PortableExporter
from .analyzer.dependency_analyzer import DependencyAnalyzer
from .analyzer.code_analyzer import CodeAnalyzer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Liberate apps from proprietary platforms (Base44, Replit, etc.)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Liberate a Replit project
  liberator extract /path/to/replit-project -o ./liberated-app

  # Liberate from GitHub URL
  liberator extract https://github.com/user/repo -o ./liberated-app

  # Liberate and push to new GitHub repo
  liberator extract /path/to/project -o ./liberated-app --github "new:my-repo"

  # Liberate and push to existing GitHub repo
  liberator extract /path/to/project -o ./liberated-app --github "https://github.com/user/repo"

  # Liberate a Base44 project
  liberator extract /path/to/base44-project -o ./liberated-app

  # Analyze dependencies only
  liberator analyze /path/to/project

  # Export to portable format
  liberator export /path/to/project -o ./portable-app
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract project from proprietary platform')
    extract_parser.add_argument('source', help='Source path or URL (GitHub, GitLab, etc.) of the project to extract')
    extract_parser.add_argument('-o', '--output', required=True, help='Output directory for liberated project')
    extract_parser.add_argument('--platform', choices=['auto', 'base44', 'replit', 'generic'],
                               default='auto', help='Platform type (default: auto-detect)')
    extract_parser.add_argument('--analyze', action='store_true', help='Analyze code after extraction')
    extract_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    extract_parser.add_argument('--github', help='Push to GitHub (repo URL or "new:repo-name" to create)')
    extract_parser.add_argument('--github-private', action='store_true', help='Create private GitHub repository')
    extract_parser.add_argument('--github-branch', default='main', help='GitHub branch name (default: main)')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze project dependencies and structure')
    analyze_parser.add_argument('source', help='Source path of the project to analyze')
    analyze_parser.add_argument('--output', help='Output file for analysis results (JSON)')
    analyze_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export project to portable format')
    export_parser.add_argument('source', help='Source path of the project to export')
    export_parser.add_argument('-o', '--output', required=True, help='Output directory')
    export_parser.add_argument('--docker', action='store_true', help='Generate Docker files')
    export_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'extract':
            handle_extract(args)
        elif args.command == 'analyze':
            handle_analyze(args)
        elif args.command == 'export':
            handle_export(args)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def handle_extract(args):
    """Handle extract command."""
    from ..core.url_handler import URLHandler
    
    source = args.source
    
    # Check if source is a URL
    if URLHandler.is_url(source):
        print(f"🌐 Source is a URL: {source}")
        print(f"📥 Downloading/cloning project...")
        
        try:
            temp_dir = Path(tempfile.mkdtemp(prefix='liberator_'))
            source_path = URLHandler.download_from_url(source, temp_dir)
            print(f"✅ Downloaded to: {source_path}")
            is_url_source = True
        except Exception as e:
            print(f"❌ Error downloading from URL: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        source_path = Path(source)
        if not source_path.exists():
            print(f"Error: Source path does not exist: {source_path}", file=sys.stderr)
            sys.exit(1)
        is_url_source = False
    
    print(f"🔍 Detecting platform for: {source_path}")
    
    # Get extractor
    if args.platform == 'auto':
        extractor_class = PlatformDetector.detect_platform(str(source_path))
        print(f"✓ Detected platform: {extractor_class.__name__}")
    else:
        from .extractors import Base44Extractor, ReplitExtractor, GenericExtractor
        extractor_map = {
            'base44': Base44Extractor,
            'replit': ReplitExtractor,
            'generic': GenericExtractor
        }
        extractor_class = extractor_map[args.platform]
        print(f"✓ Using platform: {args.platform}")
    
    extractor = extractor_class(str(source_path))
    
    print(f"📦 Extracting files...")
    result = extractor.extract()
    
    print(f"✓ Extracted {len(result.files)} files")
    print(f"✓ Found {len(result.dependencies)} dependencies")
    
    if result.errors:
        print(f"\n⚠️  Errors encountered:")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.warnings:
        print(f"\n⚠️  Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    # Export to portable format
    print(f"\n📤 Exporting to portable format...")
    output_path = Path(args.output)
    exporter = PortableExporter(str(output_path))
    export_result = exporter.export(result)
    
    print(f"\n✅ Successfully liberated project!")
    print(f"   Output: {output_path}")
    print(f"   Files: {export_result['files_exported']}")
    print(f"   Dependencies: {sum(len(deps) for deps in export_result['dependencies'].values())}")
    
    # Push to GitHub if requested
    if args.github:
        print(f"\n🐙 Pushing to GitHub...")
        from .integrations.github import GitHubIntegration
        
        github = GitHubIntegration()
        output_path_obj = Path(output_path)
        
        if args.github.startswith('new:'):
            # Create new repository
            repo_name = args.github.replace('new:', '')
            print(f"   Creating repository: {repo_name}")
            success, repo_url = github.create_repository(
                repo_name,
                description="Liberated from proprietary platform",
                private=args.github_private
            )
            if success:
                print(f"   ✅ Repository created: {repo_url}")
            else:
                print(f"   ❌ Failed to create repository: {repo_url}")
                sys.exit(1)
        else:
            # Use existing repository
            repo_url = args.github
        
        # Push to repository
        success, message = github.push_to_repository(
            output_path_obj,
            repo_url,
            branch=args.github_branch,
            commit_message="Initial commit: Liberated project"
        )
        
        if success:
            print(f"   ✅ {message}")
            print(f"   🔗 View at: {repo_url}")
        else:
            print(f"   ❌ {message}")
            sys.exit(1)
    
    # Cleanup temp directory if source was a URL
    if is_url_source:
        try:
            from ..core.url_handler import URLHandler
            URLHandler.cleanup_temp_dir(temp_dir)
            print(f"🧹 Cleaned up temporary files")
        except:
            pass
    
    if args.analyze:
        print(f"\n🔬 Analyzing code structure...")
        analyzer = CodeAnalyzer()
        for file_path, content in result.files.items():
            analysis = analyzer.analyze_file(file_path, content)
            if args.verbose:
                print(f"  {file_path}: {analysis['language']} - {len(analysis['functions'])} functions")


def handle_analyze(args):
    """Handle analyze command."""
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source path does not exist: {source_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"🔬 Analyzing project: {source_path}")
    
    dependency_analyzer = DependencyAnalyzer()
    code_analyzer = CodeAnalyzer()
    
    # Analyze all files
    analysis_results = {
        'files': [],
        'dependencies': set(),
        'languages': set()
    }
    
    for file_path in source_path.rglob('*'):
        if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                relative_path = str(file_path.relative_to(source_path))
                
                # Analyze code
                code_analysis = code_analyzer.analyze_file(relative_path, content)
                analysis_results['files'].append(code_analysis)
                analysis_results['languages'].add(code_analysis['language'])
                
                # Analyze dependencies
                deps = dependency_analyzer.analyze_code(content, relative_path)
                analysis_results['dependencies'].update(deps)
                
            except Exception as e:
                if args.verbose:
                    print(f"  ⚠️  Could not analyze {file_path}: {e}")
    
    # Normalize dependencies
    normalized_deps = dependency_analyzer.normalize_dependencies(list(analysis_results['dependencies']))
    
    # Print results
    print(f"\n📊 Analysis Results:")
    print(f"   Files analyzed: {len(analysis_results['files'])}")
    print(f"   Languages: {', '.join(sorted(analysis_results['languages']))}")
    print(f"\n📦 Dependencies:")
    for dep_type, deps in normalized_deps.items():
        if deps:
            print(f"   {dep_type.upper()}: {len(deps)}")
            if args.verbose:
                for dep in sorted(deps)[:10]:  # Show first 10
                    print(f"     - {dep}")
                if len(deps) > 10:
                    print(f"     ... and {len(deps) - 10} more")
    
    # Save to file if requested
    if args.output:
        import json
        output_data = {
            'files': analysis_results['files'],
            'dependencies': normalized_deps,
            'languages': list(analysis_results['languages'])
        }
        Path(args.output).write_text(json.dumps(output_data, indent=2))
        print(f"\n💾 Analysis saved to: {args.output}")


def handle_export(args):
    """Handle export command."""
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source path does not exist: {source_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"📤 Exporting project: {source_path}")
    
    # Extract first
    extractor_class = PlatformDetector.detect_platform(str(source_path))
    extractor = extractor_class(str(source_path))
    result = extractor.extract()
    
    # Export
    exporter = PortableExporter(str(args.output))
    export_result = exporter.export(result)
    
    print(f"\n✅ Successfully exported project!")
    print(f"   Output: {args.output}")
    print(f"   Files: {export_result['files_exported']}")


if __name__ == '__main__':
    main()
