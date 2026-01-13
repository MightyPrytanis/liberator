"""
Main window for Liberator GUI application.
"""

import sys
import os
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTextEdit, QFileDialog, QProgressBar, QTabWidget,
    QGroupBox, QLineEdit, QMessageBox, QComboBox, QCheckBox,
    QListWidget, QListWidgetItem, QSplitter, QTreeWidget, QTreeWidgetItem,
    QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon, QDragEnterEvent, QDropEvent, QAction, QKeySequence

from ..core.platform_detector import PlatformDetector
from ..portability.exporter import PortableExporter
from ..analyzer.dependency_analyzer import DependencyAnalyzer
from ..analyzer.code_analyzer import CodeAnalyzer


class ExtractionThread(QThread):
    """Thread for running extraction operations."""
    
    finished = pyqtSignal(object, str)  # result, message
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, source_path: str, output_path: str, platform: str = 'auto', target_platforms=None):
        super().__init__()
        self.source_path = source_path
        self.output_path = output_path
        self.platform = platform
        self.target_platforms = target_platforms or []
    
    def get_target_platforms(self):
        """Get selected target platforms - placeholder, will be set by main window."""
        return self.target_platforms
    
    def run(self):
        """Run the extraction."""
        try:
            self.progress.emit("Detecting platform...")
            
            # Get extractor
            if self.platform == 'auto':
                extractor_class = PlatformDetector.detect_platform(self.source_path)
            else:
                from ..extractors import Base44Extractor, ReplitExtractor, GenericExtractor
                extractor_map = {
                    'base44': Base44Extractor,
                    'replit': ReplitExtractor,
                    'generic': GenericExtractor
                }
                extractor_class = extractor_map.get(self.platform, GenericExtractor)
            
            self.progress.emit(f"Using extractor: {extractor_class.__name__}")
            
            extractor = extractor_class(self.source_path)
            self.progress.emit("Extracting files...")
            result = extractor.extract()
            
            self.progress.emit(f"Extracted {len(result.files)} files")
            self.progress.emit("Exporting to portable format...")
            
            exporter = PortableExporter(self.output_path, target_platforms=self.target_platforms)
            export_result = exporter.export(result)
            
            message = f"Successfully liberated project!\n\nFiles: {export_result['files_exported']}\nOutput: {self.output_path}"
            self.finished.emit(result, message)
            
        except Exception as e:
            self.error.emit(str(e))


class AnalysisThread(QThread):
    """Thread for running analysis operations."""
    
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, source_path: str):
        super().__init__()
        self.source_path = source_path
    
    def run(self):
        """Run the analysis."""
        try:
            self.progress.emit("Analyzing project...")
            
            dependency_analyzer = DependencyAnalyzer()
            code_analyzer = CodeAnalyzer()
            
            analysis_results = {
                'files': [],
                'dependencies': set(),
                'languages': set(),
                'file_analysis': []
            }
            
            source = Path(self.source_path)
            total_files = sum(1 for _ in source.rglob('*') if _.is_file() and not any(p.startswith('.') for p in _.parts))
            processed = 0
            
            for file_path in source.rglob('*'):
                if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        relative_path = str(file_path.relative_to(source))
                        
                        code_analysis = code_analyzer.analyze_file(relative_path, content)
                        analysis_results['file_analysis'].append(code_analysis)
                        analysis_results['languages'].add(code_analysis['language'])
                        
                        deps = dependency_analyzer.analyze_code(content, relative_path)
                        analysis_results['dependencies'].update(deps)
                        
                        processed += 1
                        if processed % 10 == 0:
                            self.progress.emit(f"Analyzed {processed}/{total_files} files...")
                            
                    except Exception:
                        continue
            
            normalized_deps = dependency_analyzer.normalize_dependencies(list(analysis_results['dependencies']))
            
            analysis_results['dependencies'] = normalized_deps
            analysis_results['languages'] = list(analysis_results['languages'])
            analysis_results['total_files'] = processed
            
            self.finished.emit(analysis_results)
            
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.current_source_path: Optional[str] = None
        self.current_output_path: Optional[str] = None
        self.extraction_thread: Optional[ExtractionThread] = None
        self.analysis_thread: Optional[AnalysisThread] = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Liberator - Free Your Apps from Proprietary Platforms")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon
        from pathlib import Path
        icon_paths = [
            Path(__file__).parent.parent.parent / 'assets' / 'icon.png',
            Path(__file__).parent.parent.parent / 'assets' / 'icon_512x512.png',
            Path(__file__).parent.parent.parent / 'assets' / 'icon_256x256.png',
        ]
        
        for icon_path in icon_paths:
            if icon_path.exists():
                from PyQt6.QtGui import QIcon
                self.setWindowIcon(QIcon(str(icon_path)))
                break
        
        # Apply metallic theme
        from .theme import MAIN_WINDOW_STYLE
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
        # Create central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_extract_tab(), "Extract")
        self.tabs.addTab(self.create_analyze_tab(), "Analyze")
        self.tabs.addTab(self.create_export_tab(), "Export")
        self.tabs.addTab(self.create_ai_assistant_tab(), "AI Assistant")
        self.tabs.addTab(self.create_executive_producer_tab(), "Executive Producer")
        self.tabs.addTab(self.create_projects_tab(), "Projects")
        self.tabs.addTab(self.create_github_tab(), "GitHub")
        
        layout.addWidget(self.tabs)
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
        # Create macOS menu bar
        self.create_macos_menu()
    
    def create_macos_menu(self):
        """Create macOS-style menu bar."""
        menubar = self.menuBar()
        
        # App menu (macOS specific)
        app_menu = menubar.addMenu("Liberator")
        
        about_action = QAction("About Liberator", self)
        about_action.triggered.connect(self.show_about_dialog)
        app_menu.addAction(about_action)
        
        app_menu.addSeparator()
        
        preferences_action = QAction("Preferences...", self)
        preferences_action.setShortcut("Ctrl+,")
        preferences_action.triggered.connect(self.show_preferences)
        app_menu.addAction(preferences_action)
        
        app_menu.addSeparator()
        
        quit_action = QAction("Quit Liberator", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        app_menu.addAction(quit_action)
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open Project...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.select_source_path)
        file_menu.addAction(open_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("Liberator Help", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        help_menu.addSeparator()
        
        about_qt_action = QAction("About Qt", self)
        about_qt_action.triggered.connect(lambda: QMessageBox.aboutQt(self))
        help_menu.addAction(about_qt_action)
    
    def show_about_dialog(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Liberator",
            "<h2>Liberator</h2>"
            "<p>Version 1.0.0</p>"
            "<p>Free your apps from proprietary platforms</p>"
            "<p>Liberator extracts, analyzes, and exports projects from "
            "Base44, Replit, and other proprietary platforms, making them "
            "fully portable and open-source.</p>"
            "<p><a href='https://github.com/MightyPrytanis/liberator'>GitHub</a></p>"
        )
    
    def show_preferences(self):
        """Show preferences dialog."""
        QMessageBox.information(
            self,
            "Preferences",
            "Preferences dialog coming soon!"
        )
    
    def show_help(self):
        """Show help dialog."""
        help_text = """
<h2>Liberator Help</h2>

<h3>Extract Tab</h3>
<p>1. Select folder, enter URL, or drag & drop your source project</p>
<p>2. Choose the platform (or use auto-detect)</p>
<p>3. Select output directory</p>
<p>4. Click "Liberate Project" to extract and export</p>
<p><b>URL Support:</b> Paste GitHub, GitLab, or other repository URLs directly!</p>

<h3>Analyze Tab</h3>
<p>1. Select a project folder to analyze</p>
<p>2. Click "Analyze Project" to see dependencies and code structure</p>

<h3>Tips</h3>
<ul>
<li>You can drag and drop folders directly onto the source path field</li>
<li>Use auto-detect for automatic platform detection</li>
<li>Check "Analyze code after extraction" for detailed analysis</li>
</ul>
        """
        QMessageBox.information(self, "Help", help_text)
    
    def create_extract_tab(self) -> QWidget:
        """Create the extraction tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Source selection
        source_group = QGroupBox("Source Project")
        source_layout = QVBoxLayout()
        
        source_path_layout = QHBoxLayout()
        self.source_path_edit = QLineEdit()
        self.source_path_edit.setPlaceholderText("Select folder, drag & drop, or enter URL (GitHub, GitLab, etc.)...")
        source_path_btn = QPushButton("Browse/URL...")
        source_path_btn.clicked.connect(self.select_source_path)
        source_path_layout.addWidget(self.source_path_edit)
        source_path_layout.addWidget(source_path_btn)
        source_layout.addLayout(source_path_layout)
        
        # Platform selection
        platform_layout = QHBoxLayout()
        platform_layout.addWidget(QLabel("Platform:"))
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["Auto-detect", "Base44", "Replit", "Generic"])
        platform_layout.addWidget(self.platform_combo)
        platform_layout.addStretch()
        source_layout.addLayout(platform_layout)
        
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)
        
        # Output selection
        output_group = QGroupBox("Output Directory")
        output_layout = QHBoxLayout()
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("Select output directory for liberated project...")
        output_path_btn = QPushButton("Browse...")
        output_path_btn.clicked.connect(self.select_output_path)
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(output_path_btn)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Target OS selection
        os_group = QGroupBox("Target Operating Systems")
        os_layout = QVBoxLayout()
        
        os_info = QLabel("Select OS(es) for compatibility (code will be adapted automatically):")
        os_info.setWordWrap(True)
        os_layout.addWidget(os_info)
        
        os_row1 = QHBoxLayout()
        self.windows_os_check = QCheckBox("Windows")
        self.macos_os_check = QCheckBox("macOS")
        self.linux_os_check = QCheckBox("Linux")
        os_row1.addWidget(self.windows_os_check)
        os_row1.addWidget(self.macos_os_check)
        os_row1.addWidget(self.linux_os_check)
        os_layout.addLayout(os_row1)
        
        os_row2 = QHBoxLayout()
        self.ios_os_check = QCheckBox("iOS")
        self.android_os_check = QCheckBox("Android")
        os_row2.addWidget(self.ios_os_check)
        os_row2.addWidget(self.android_os_check)
        os_row2.addStretch()
        os_layout.addLayout(os_row2)
        
        os_group.setLayout(os_layout)
        layout.addWidget(os_group)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        self.analyze_checkbox = QCheckBox("Analyze code after extraction")
        self.analyze_checkbox.setChecked(True)
        options_layout.addWidget(self.analyze_checkbox)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Extract button
        extract_btn = QPushButton("🚀 Liberate Project")
        extract_btn.setMinimumHeight(50)
        from .theme import BUTTON_PRIMARY
        extract_btn.setStyleSheet(BUTTON_PRIMARY + "font-size: 16px;")
        extract_btn.clicked.connect(self.start_extraction)
        layout.addWidget(extract_btn)
        
        # Progress
        self.extract_progress = QProgressBar()
        self.extract_progress.setVisible(False)
        layout.addWidget(self.extract_progress)
        
        # Output log
        log_group = QGroupBox("Extraction Log")
        log_layout = QVBoxLayout()
        self.extract_log = QTextEdit()
        self.extract_log.setReadOnly(True)
        self.extract_log.setFont(QFont("Monaco", 10))
        log_layout.addWidget(self.extract_log)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        layout.addStretch()
        return widget
    
    def create_analyze_tab(self) -> QWidget:
        """Create the analysis tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Source selection
        source_group = QGroupBox("Project to Analyze")
        source_layout = QHBoxLayout()
        self.analyze_source_edit = QLineEdit()
        self.analyze_source_edit.setPlaceholderText("Select project folder to analyze...")
        analyze_source_btn = QPushButton("Browse...")
        analyze_source_btn.clicked.connect(self.select_analyze_source)
        source_layout.addWidget(self.analyze_source_edit)
        source_layout.addWidget(analyze_source_btn)
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)
        
        # Analyze button
        analyze_btn = QPushButton("🔬 Analyze Project")
        analyze_btn.setMinimumHeight(50)
        from .theme import BUTTON_SUCCESS
        analyze_btn.setStyleSheet(BUTTON_SUCCESS + "font-size: 16px;")
        analyze_btn.clicked.connect(self.start_analysis)
        layout.addWidget(analyze_btn)
        
        # Progress
        self.analyze_progress = QProgressBar()
        self.analyze_progress.setVisible(False)
        layout.addWidget(self.analyze_progress)
        
        # Results splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Dependencies panel
        deps_widget = QWidget()
        deps_layout = QVBoxLayout(deps_widget)
        deps_layout.addWidget(QLabel("<b>Dependencies</b>"))
        self.deps_list = QTreeWidget()
        self.deps_list.setHeaderLabels(["Type", "Package"])
        deps_layout.addWidget(self.deps_list)
        splitter.addWidget(deps_widget)
        
        # Languages and stats panel
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.addWidget(QLabel("<b>Analysis Results</b>"))
        self.analysis_results = QTextEdit()
        self.analysis_results.setReadOnly(True)
        self.analysis_results.setFont(QFont("Monaco", 10))
        stats_layout.addWidget(self.analysis_results)
        splitter.addWidget(stats_widget)
        
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)
        
        return widget
    
    def create_export_tab(self) -> QWidget:
        """Create the export tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        info_label = QLabel(
            "The Export tab is integrated into the Extract tab.\n"
            "When you extract a project, it is automatically exported to a portable format."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 14px; padding: 20px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        return widget
    
    def create_ai_assistant_tab(self) -> QWidget:
        """Create AI assistant tab."""
        from .ai_assistant_widget import AIAssistantWidget
        return AIAssistantWidget(self)
    
    def create_executive_producer_tab(self) -> QWidget:
        """Create Executive Producer tab."""
        from .executive_producer_widget import ExecutiveProducerWidget
        return ExecutiveProducerWidget(self)
    
    def create_projects_tab(self) -> QWidget:
        """Create projects management tab."""
        from .projects_widget import ProjectsWidget
        return ProjectsWidget(self)
    
    def create_github_tab(self) -> QWidget:
        """Create GitHub integration tab."""
        from .github_integration_widget import GitHubIntegrationWidget
        return GitHubIntegrationWidget(self)
    
    def select_source_path(self):
        """Select source project path or enter URL."""
        from PyQt6.QtWidgets import QInputDialog
        
        # Ask user if they want to enter URL or browse
        choice, ok = QInputDialog.getItem(
            self,
            "Select Source",
            "Choose input method:",
            ["Browse Local Folder", "Enter URL"],
            0,
            False
        )
        
        if not ok:
            return
        
        if choice == "Enter URL":
            url, ok = QInputDialog.getText(
                self,
                "Enter URL",
                "Enter project URL (GitHub, GitLab, etc.):\n\nExamples:\n- https://github.com/user/repo\n- https://gitlab.com/user/repo.git",
                text=""
            )
            if ok and url:
                self.source_path_edit.setText(url)
                self.current_source_path = url
        else:
            path = QFileDialog.getExistingDirectory(self, "Select Source Project")
            if path:
                self.source_path_edit.setText(path)
                self.current_source_path = path
    
    def select_output_path(self):
        """Select output directory."""
        path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if path:
            self.output_path_edit.setText(path)
            self.current_output_path = path
    
    def select_analyze_source(self):
        """Select project to analyze."""
        path = QFileDialog.getExistingDirectory(self, "Select Project to Analyze")
        if path:
            self.analyze_source_edit.setText(path)
    
    def start_extraction(self):
        """Start the extraction process."""
        from ..core.url_handler import URLHandler
        import tempfile
        
        source = self.source_path_edit.text()
        output = self.output_path_edit.text()
        
        if not source:
            QMessageBox.warning(self, "Error", "Please enter a source path or URL.")
            return
        
        if not output:
            QMessageBox.warning(self, "Error", "Please select an output directory.")
            return
        
        # Check if source is a URL
        is_url = URLHandler.is_url(source)
        temp_dir = None
        
        if is_url:
            # Download from URL
            self.extract_log.append(f"🌐 Source is a URL: {source}")
            self.extract_log.append("📥 Downloading/cloning project...")
            
            try:
                temp_dir = Path(tempfile.mkdtemp(prefix='liberator_'))
                source_path = URLHandler.download_from_url(source, temp_dir)
                self.extract_log.append(f"✅ Downloaded to: {source_path}")
                source = str(source_path)
            except Exception as e:
                self.extract_log.append(f"❌ Error downloading from URL: {e}")
                QMessageBox.critical(self, "Download Error", f"Failed to download from URL:\n{e}")
                return
        elif not os.path.exists(source):
            QMessageBox.warning(self, "Error", "Please select a valid source project path.")
            return
        
        if not output:
            QMessageBox.warning(self, "Error", "Please select an output directory.")
            return
        
        # Get platform
        platform_map = {
            "Auto-detect": "auto",
            "Base44": "base44",
            "Replit": "replit",
            "Generic": "generic"
        }
        platform = platform_map.get(self.platform_combo.currentText(), "auto")
        
        # Clear log
        self.extract_log.clear()
        self.extract_progress.setVisible(True)
        self.extract_progress.setRange(0, 0)  # Indeterminate
        
        # Store temp dir for cleanup
        if is_url:
            self._temp_dir = temp_dir
        else:
            self._temp_dir = None
        
        # Get target platforms
        target_platforms = self.get_target_platforms()
        
        # Start extraction thread
        self.extraction_thread = ExtractionThread(source, output, platform, target_platforms)
        self.extraction_thread.progress.connect(self.update_extract_log)
        self.extraction_thread.finished.connect(self.extraction_finished)
        self.extraction_thread.error.connect(self.extraction_error)
        self.extraction_thread.start()
        
        self.statusBar().showMessage("Extracting...")
    
    def get_target_platforms(self):
        """Get selected target platforms."""
        from ..executive_producer.compatibility_wizard import Platform
        
        platforms = []
        if hasattr(self, 'windows_os_check') and self.windows_os_check.isChecked():
            platforms.append(Platform.WINDOWS)
        if hasattr(self, 'macos_os_check') and self.macos_os_check.isChecked():
            platforms.append(Platform.MACOS)
        if hasattr(self, 'linux_os_check') and self.linux_os_check.isChecked():
            platforms.append(Platform.LINUX)
        if hasattr(self, 'ios_os_check') and self.ios_os_check.isChecked():
            platforms.append(Platform.IOS)
        if hasattr(self, 'android_os_check') and self.android_os_check.isChecked():
            platforms.append(Platform.ANDROID)
        
        return platforms
    
    def update_extract_log(self, message: str):
        """Update extraction log."""
        self.extract_log.append(message)
        self.statusBar().showMessage(message)
    
    def extraction_finished(self, result, message: str):
        """Handle extraction completion."""
        self.extract_progress.setVisible(False)
        self.extract_log.append(f"\n✅ {message}")
        self.statusBar().showMessage("Extraction completed successfully")
        
        # Cleanup temp directory if source was a URL
        if hasattr(self, '_temp_dir') and self._temp_dir:
            try:
                from ..core.url_handler import URLHandler
                URLHandler.cleanup_temp_dir(self._temp_dir)
                self.extract_log.append("🧹 Cleaned up temporary files")
            except:
                pass
        
        # Ask if user wants to push to GitHub
        reply = QMessageBox.question(
            self,
            "Extraction Complete",
            f"{message}\n\nWould you like to push this project to GitHub?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Switch to GitHub tab and set the project path
            github_tab = self.tabs.widget(6)  # GitHub tab index
            if github_tab and hasattr(github_tab, 'project_path_label'):
                github_tab.project_path = Path(self.output_path_edit.text())
                github_tab.project_path_label.setText(self.output_path_edit.text())
                self.tabs.setCurrentIndex(6)  # Switch to GitHub tab
                QMessageBox.information(
                    self,
                    "GitHub Tab",
                    "Switched to GitHub tab. Configure your repository and push!"
                )
        else:
            QMessageBox.information(self, "Success", message)
    
    def extraction_error(self, error: str):
        """Handle extraction error."""
        self.extract_progress.setVisible(False)
        self.extract_log.append(f"\n❌ Error: {error}")
        self.statusBar().showMessage("Extraction failed")
        
        QMessageBox.critical(self, "Error", f"Extraction failed:\n{error}")
    
    def start_analysis(self):
        """Start the analysis process."""
        source = self.analyze_source_edit.text()
        
        if not source or not os.path.exists(source):
            QMessageBox.warning(self, "Error", "Please select a valid project path.")
            return
        
        # Clear results
        self.deps_list.clear()
        self.analysis_results.clear()
        self.analyze_progress.setVisible(True)
        self.analyze_progress.setRange(0, 0)  # Indeterminate
        
        # Start analysis thread
        self.analysis_thread = AnalysisThread(source)
        self.analysis_thread.progress.connect(lambda msg: self.statusBar().showMessage(msg))
        self.analysis_thread.finished.connect(self.analysis_finished)
        self.analysis_thread.error.connect(self.analysis_error)
        self.analysis_thread.start()
        
        self.statusBar().showMessage("Analyzing...")
    
    def analysis_finished(self, results: dict):
        """Handle analysis completion."""
        self.analyze_progress.setVisible(False)
        
        # Display dependencies
        self.deps_list.clear()
        for dep_type, deps in results['dependencies'].items():
            if deps:
                parent = QTreeWidgetItem(self.deps_list, [dep_type.upper(), f"{len(deps)} packages"])
                for dep in sorted(deps)[:50]:  # Limit to 50 per type
                    QTreeWidgetItem(parent, ["", dep])
                parent.setExpanded(True)
        
        # Display results
        results_text = f"""Analysis Complete!

Files Analyzed: {results['total_files']}
Languages Detected: {', '.join(sorted(results['languages']))}

Dependencies Summary:
"""
        for dep_type, deps in results['dependencies'].items():
            if deps:
                results_text += f"\n{dep_type.upper()}: {len(deps)} packages\n"
                for dep in sorted(deps)[:20]:
                    results_text += f"  - {dep}\n"
                if len(deps) > 20:
                    results_text += f"  ... and {len(deps) - 20} more\n"
        
        self.analysis_results.setText(results_text)
        self.statusBar().showMessage("Analysis completed")
    
    def analysis_error(self, error: str):
        """Handle analysis error."""
        self.analyze_progress.setVisible(False)
        self.statusBar().showMessage("Analysis failed")
        
        QMessageBox.critical(self, "Error", f"Analysis failed:\n{error}")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            path = files[0]
            if os.path.isdir(path):
                self.source_path_edit.setText(path)
                self.current_source_path = path
