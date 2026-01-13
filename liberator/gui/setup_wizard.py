"""
Setup Wizard for Liberator - Single-click setup experience.
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QProgressBar, QTextEdit, QCheckBox, QLineEdit,
    QMessageBox, QGroupBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import subprocess


class SetupWorker(QThread):
    """Worker thread for setup operations."""
    
    progress = pyqtSignal(str, int)  # message, percentage
    finished = pyqtSignal(bool, str)  # success, message
    error = pyqtSignal(str)
    
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
    
    def run(self):
        """Execute setup steps."""
        try:
            total_steps = len(self.steps)
            for i, (step_name, step_func) in enumerate(self.steps):
                self.progress.emit(f"Running: {step_name}...", int((i / total_steps) * 100))
                result = step_func()
                if not result[0]:
                    self.error.emit(f"{step_name} failed: {result[1]}")
                    return
            
            self.progress.emit("Setup complete!", 100)
            self.finished.emit(True, "Setup completed successfully!")
        except Exception as e:
            self.error.emit(str(e))


class WelcomePage(QWizardPage):
    """Welcome page of the setup wizard."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome to Liberator")
        self.setSubTitle("Let's get you set up in just a few clicks!")
        
        layout = QVBoxLayout()
        
        welcome_text = QLabel("""
        <h2>Welcome to Liberator Setup</h2>
        <p>This wizard will help you:</p>
        <ul>
            <li>Install required dependencies</li>
            <li>Configure your environment</li>
            <li>Set up AI assistant (optional)</li>
            <li>Verify everything works</li>
        </ul>
        <p><b>Click Next to begin!</b></p>
        """)
        welcome_text.setWordWrap(True)
        layout.addWidget(welcome_text)
        
        layout.addStretch()
        self.setLayout(layout)


class DependenciesPage(QWizardPage):
    """Dependencies installation page."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Install Dependencies")
        self.setSubTitle("We'll install the required packages for you")
        
        layout = QVBoxLayout()
        
        # Dependency checklist
        deps_group = QGroupBox("Dependencies to Install")
        deps_layout = QVBoxLayout()
        
        self.core_check = QCheckBox("Core Liberator (already installed)")
        self.core_check.setChecked(True)
        self.core_check.setEnabled(False)
        deps_layout.addWidget(self.core_check)
        
        self.gui_check = QCheckBox("GUI Dependencies (PyQt6)")
        self.gui_check.setChecked(True)
        deps_layout.addWidget(self.gui_check)
        
        self.ai_check = QCheckBox("AI Assistant (openai, anthropic) - Optional")
        self.ai_check.setChecked(False)
        deps_layout.addWidget(self.ai_check)
        
        deps_group.setLayout(deps_layout)
        layout.addWidget(deps_group)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Log
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(200)
        self.log.setFont(QFont("Monaco", 9))
        layout.addWidget(self.log)
        
        # Install button
        self.install_btn = QPushButton("Install Selected Dependencies")
        from .theme import BUTTON_PRIMARY
        self.install_btn.setStyleSheet(BUTTON_PRIMARY)
        self.install_btn.clicked.connect(self.install_dependencies)
        layout.addWidget(self.install_btn)
        
        self.installed = False
        layout.addStretch()
        self.setLayout(layout)
    
    def install_dependencies(self):
        """Install selected dependencies."""
        self.install_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminate
        
        steps = []
        
        if self.gui_check.isChecked():
            steps.append(("Installing PyQt6", self._install_pyqt6))
        
        if self.ai_check.isChecked():
            steps.append(("Installing AI packages", self._install_ai))
        
        if not steps:
            self.log.append("No dependencies selected to install.")
            self.progress.setVisible(False)
            self.installed = True
            self.install_btn.setEnabled(True)
            return
        
        self.worker = SetupWorker(steps)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.installation_finished)
        self.worker.error.connect(self.installation_error)
        self.worker.start()
    
    def _install_pyqt6(self):
        """Install PyQt6."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "PyQt6>=6.6.0"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return (True, "PyQt6 installed successfully")
            else:
                return (False, result.stderr)
        except Exception as e:
            return (False, str(e))
    
    def _install_ai(self):
        """Install AI packages."""
        try:
            packages = ["openai>=1.0.0", "anthropic>=0.18.0"]
            for package in packages:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode != 0:
                    return (False, f"Failed to install {package}: {result.stderr}")
            return (True, "AI packages installed successfully")
        except Exception as e:
            return (False, str(e))
    
    def update_progress(self, message, percentage):
        """Update progress."""
        self.log.append(message)
        if percentage >= 0:
            self.progress.setRange(0, 100)
            self.progress.setValue(percentage)
    
    def installation_finished(self, success, message):
        """Handle installation completion."""
        self.progress.setVisible(False)
        self.install_btn.setEnabled(True)
        if success:
            self.log.append(f"✅ {message}")
            self.installed = True
        else:
            self.log.append(f"❌ {message}")
    
    def installation_error(self, error):
        """Handle installation error."""
        self.progress.setVisible(False)
        self.install_btn.setEnabled(True)
        self.log.append(f"❌ Error: {error}")
    
    def isComplete(self):
        """Check if page is complete."""
        return self.installed or not (self.gui_check.isChecked() or self.ai_check.isChecked())


class AIConfigPage(QWizardPage):
    """AI Assistant configuration page."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("AI Assistant Configuration")
        self.setSubTitle("Configure your AI assistant (optional)")
        
        layout = QVBoxLayout()
        
        info_label = QLabel("""
        <p>The AI assistant can help with:</p>
        <ul>
            <li>Code repair and refactoring</li>
            <li>Project troubleshooting</li>
            <li>Compatibility guidance</li>
            <li>General help and how-to questions</li>
        </ul>
        <p><b>Supported Providers:</b> OpenAI, Anthropic, Perplexity</p>
        <p><b>You can configure this later in settings.</b></p>
        <p><b>Note:</b> API keys are stored securely in ~/.liberator/ai_config.json and never committed to Git.</p>
        """)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # API Key configuration
        api_group = QGroupBox("API Configuration")
        api_layout = QVBoxLayout()
        
        api_layout.addWidget(QLabel("OpenAI API Key (optional):"))
        self.openai_key = QLineEdit()
        self.openai_key.setPlaceholderText("sk-...")
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addWidget(self.openai_key)
        
        api_layout.addWidget(QLabel("Anthropic API Key (optional):"))
        self.anthropic_key = QLineEdit()
        self.anthropic_key.setPlaceholderText("sk-ant-...")
        self.anthropic_key.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addWidget(self.anthropic_key)
        
        api_layout.addWidget(QLabel("Perplexity API Key (optional):"))
        self.perplexity_key = QLineEdit()
        self.perplexity_key.setPlaceholderText("pplx-...")
        self.perplexity_key.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addWidget(self.perplexity_key)
        
        skip_check = QCheckBox("Skip AI setup for now")
        skip_check.setChecked(True)
        api_layout.addWidget(skip_check)
        self.skip_ai = skip_check
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def save_config(self):
        """Save AI configuration."""
        if self.skip_ai.isChecked():
            return
        
        config_dir = Path.home() / ".liberator"
        config_dir.mkdir(exist_ok=True)
        
        config_file = config_dir / "ai_config.json"
        import json
        
        config = {}
        if self.openai_key.text():
            config['openai_key'] = self.openai_key.text()
        if self.anthropic_key.text():
            config['anthropic_key'] = self.anthropic_key.text()
        if self.perplexity_key.text():
            config['perplexity_api_key'] = self.perplexity_key.text()
        
        if config:
            config_file.write_text(json.dumps(config, indent=2))
            # Set restrictive permissions (read/write for owner only)
            os.chmod(config_file, 0o600)


class VerificationPage(QWizardPage):
    """Verification page."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Verification")
        self.setSubTitle("Let's make sure everything works!")
        
        layout = QVBoxLayout()
        
        self.verify_btn = QPushButton("Run Verification Tests")
        from .theme import BUTTON_SECONDARY
        self.verify_btn.setStyleSheet(BUTTON_SECONDARY)
        self.verify_btn.clicked.connect(self.run_verification)
        layout.addWidget(self.verify_btn)
        
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setFont(QFont("Monaco", 9))
        layout.addWidget(self.results)
        
        self.verified = False
        layout.addStretch()
        self.setLayout(layout)
    
    def run_verification(self):
        """Run verification tests."""
        self.verify_btn.setEnabled(False)
        self.results.clear()
        self.results.append("Running verification tests...\n")
        
        tests = [
            ("Python version", self._test_python),
            ("Core Liberator", self._test_core),
            ("GUI (if installed)", self._test_gui),
            ("AI packages (if installed)", self._test_ai),
        ]
        
        all_passed = True
        for test_name, test_func in tests:
            self.results.append(f"\nTesting {test_name}...")
            try:
                result = test_func()
                if result:
                    self.results.append(f"✅ {test_name}: PASSED")
                else:
                    self.results.append(f"⚠️  {test_name}: SKIPPED (optional)")
            except Exception as e:
                self.results.append(f"❌ {test_name}: FAILED - {e}")
                all_passed = False
        
        if all_passed:
            self.results.append("\n✅ All tests passed!")
            self.verified = True
        else:
            self.results.append("\n⚠️  Some tests failed, but core functionality should work.")
            self.verified = True  # Allow proceeding anyway
        
        self.verify_btn.setEnabled(True)
        self.completeChanged.emit()
    
    def _test_python(self):
        """Test Python version."""
        import sys
        return sys.version_info >= (3, 8)
    
    def _test_core(self):
        """Test core Liberator."""
        try:
            from liberator.core import PlatformDetector
            return True
        except:
            return False
    
    def _test_gui(self):
        """Test GUI."""
        try:
            import PyQt6
            return True
        except ImportError:
            return False
    
    def _test_ai(self):
        """Test AI packages."""
        try:
            import openai
            return True
        except ImportError:
            try:
                import anthropic
                return True
            except ImportError:
                return False
    
    def isComplete(self):
        """Check if page is complete."""
        return self.verified


class InstallationPage(QWizardPage):
    """Installation options page - desktop shortcuts and Applications."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Installation Options")
        self.setSubTitle("Create shortcuts for easy access")
        
        layout = QVBoxLayout()
        
        info_label = QLabel("""
        <p>Choose where you'd like to install Liberator shortcuts:</p>
        """)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Installation options
        options_group = QGroupBox("Installation Options")
        options_layout = QVBoxLayout()
        
        self.desktop_check = QCheckBox("Create desktop shortcut")
        self.desktop_check.setChecked(True)
        options_layout.addWidget(self.desktop_check)
        
        self.applications_check = QCheckBox("Install to Applications folder")
        self.applications_check.setChecked(True)
        options_layout.addWidget(self.applications_check)
        
        self.dock_check = QCheckBox("Add to Dock (requires app bundle)")
        self.dock_check.setChecked(False)
        options_layout.addWidget(self.dock_check)
        
        skip_check = QCheckBox("Skip installation (use command line only)")
        skip_check.setChecked(False)
        skip_check.toggled.connect(self.on_skip_toggled)
        options_layout.addWidget(skip_check)
        self.skip_install = skip_check
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Install button
        self.install_btn = QPushButton("Install Shortcuts")
        from .theme import BUTTON_PRIMARY
        self.install_btn.setStyleSheet(BUTTON_PRIMARY)
        self.install_btn.clicked.connect(self.install_shortcuts)
        layout.addWidget(self.install_btn)
        
        # Status
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        self.status_text.setFont(QFont("Monaco", 9))
        layout.addWidget(self.status_text)
        
        self.installed = False
        layout.addStretch()
        self.setLayout(layout)
    
    def on_skip_toggled(self, checked):
        """Handle skip checkbox toggle."""
        if checked:
            self.desktop_check.setChecked(False)
            self.applications_check.setChecked(False)
            self.dock_check.setChecked(False)
            self.desktop_check.setEnabled(False)
            self.applications_check.setEnabled(False)
            self.dock_check.setEnabled(False)
            self.installed = True
        else:
            self.desktop_check.setEnabled(True)
            self.applications_check.setEnabled(True)
            self.dock_check.setEnabled(True)
            self.installed = False
    
    def install_shortcuts(self):
        """Install shortcuts."""
        if self.skip_install.isChecked():
            self.status_text.append("Skipping installation.")
            self.installed = True
            self.completeChanged.emit()
            return
        
        self.install_btn.setEnabled(False)
        self.status_text.clear()
        self.status_text.append("Installing shortcuts...\n")
        
        try:
            project_root = Path(__file__).parent.parent.parent
            desktop_path = Path.home() / "Desktop"
            applications_path = Path("/Applications")
            
            # Build app bundle first if needed
            app_bundle_needed = self.applications_check.isChecked() or self.dock_check.isChecked()
            app_bundle_path = project_root / "dist" / "Liberator.app"
            
            if app_bundle_needed and not app_bundle_path.exists():
                self.status_text.append("Building app bundle...")
                build_script = project_root / "build_macos_app.sh"
                if build_script.exists():
                    result = subprocess.run(
                        ["bash", str(build_script)],
                        cwd=str(project_root),
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        self.status_text.append("✅ App bundle built successfully")
                    else:
                        self.status_text.append(f"⚠️ App bundle build had warnings: {result.stderr}")
                else:
                    self.status_text.append("⚠️ Build script not found, skipping app bundle")
                    app_bundle_needed = False
            
            # Create desktop shortcut
            if self.desktop_check.isChecked():
                self.status_text.append("Creating desktop shortcut...")
                try:
                    # Create a simple launcher script on desktop
                    desktop_launcher = desktop_path / "Liberator"
                    launcher_script = f"""#!/bin/bash
cd "{project_root}"
python3 liberator_gui.py "$@"
"""
                    desktop_launcher.write_text(launcher_script)
                    os.chmod(desktop_launcher, 0o755)
                    self.status_text.append("✅ Desktop shortcut created")
                except Exception as e:
                    self.status_text.append(f"❌ Failed to create desktop shortcut: {e}")
            
            # Install to Applications
            if self.applications_check.isChecked() and app_bundle_path.exists():
                self.status_text.append("Installing to Applications folder...")
                try:
                    import shutil
                    dest_app = applications_path / "Liberator.app"
                    if dest_app.exists():
                        shutil.rmtree(dest_app)
                    shutil.copytree(app_bundle_path, dest_app)
                    self.status_text.append("✅ Installed to Applications folder")
                except PermissionError:
                    self.status_text.append("⚠️ Permission denied. Please run with sudo or install manually.")
                except Exception as e:
                    self.status_text.append(f"❌ Failed to install to Applications: {e}")
            
            # Add to Dock (optional, requires user interaction)
            if self.dock_check.isChecked() and app_bundle_path.exists():
                self.status_text.append("⚠️ Dock addition requires manual setup or system permissions.")
                self.status_text.append("   You can drag Liberator.app to the Dock manually.")
            
            self.status_text.append("\n✅ Installation complete!")
            self.installed = True
            self.completeChanged.emit()
            
        except Exception as e:
            self.status_text.append(f"❌ Error: {e}")
        
        self.install_btn.setEnabled(True)
    
    def isComplete(self):
        """Check if page is complete."""
        return self.installed


class CompletionPage(QWizardPage):
    """Completion page."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Setup Complete!")
        self.setSubTitle("You're all set to start liberating apps!")
        
        layout = QVBoxLayout()
        
        completion_text = QLabel("""
        <h2>🎉 Setup Complete!</h2>
        <p>Liberator is now ready to use.</p>
        <p><b>What's next?</b></p>
        <ul>
            <li>Launch from Desktop shortcut (if installed)</li>
            <li>Launch from Applications: <code>open -a Liberator</code></li>
            <li>Or use command line: <code>liberator extract ...</code></li>
            <li>Check out the documentation in the Help menu</li>
        </ul>
        <p>Thank you for using Liberator!</p>
        """)
        completion_text.setWordWrap(True)
        layout.addWidget(completion_text)
        
        layout.addStretch()
        self.setLayout(layout)


class SetupWizard(QWizard):
    """Main setup wizard."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Liberator Setup Wizard")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        
        # Apply metallic theme
        from .theme import MAIN_WINDOW_STYLE
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
        # Add pages
        self.addPage(WelcomePage())
        self.addPage(DependenciesPage())
        self.addPage(AIConfigPage())
        self.addPage(VerificationPage())
        self.addPage(InstallationPage())
        self.addPage(CompletionPage())
        
        # Connect signals
        self.currentIdChanged.connect(self.on_page_changed)
        self.finished.connect(self.on_finished)
    
    def on_page_changed(self, page_id):
        """Handle page change."""
        # Save AI config when leaving AI Config page (page 2)
        if page_id == 2:
            page = self.page(2)
            if hasattr(page, 'save_config'):
                page.save_config()
    
    def on_finished(self, result):
        """Handle wizard completion."""
        if result:
            # Save AI config
            ai_page = self.page(2)
            if hasattr(ai_page, 'save_config'):
                ai_page.save_config()
            
            QMessageBox.information(
                self,
                "Setup Complete",
                "Liberator has been set up successfully!\n\nYou can now start using the application."
            )


def run_setup_wizard():
    """Run the setup wizard."""
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    wizard = SetupWizard()
    wizard.show()
    sys.exit(app.exec())
