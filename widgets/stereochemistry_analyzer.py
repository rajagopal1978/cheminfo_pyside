"""
Stereochemistry Analyzer Widget
Analyze stereochemical properties of molecules
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QMessageBox, QTextBrowser
)
from rdkit_handler import RDKitHandler
from theme_manager import ThemeManager


class StereochemistryAnalyzerWidget(QWidget):
    """Widget for analyzing molecular stereochemistry"""

    def __init__(self):
        super().__init__()
        self.rdkit = RDKitHandler()
        self.theme_manager = ThemeManager("scientific_blue")
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("🔬 Stereochemistry Analyzer")
        title.setStyleSheet(self.theme_manager.get_title_style("large"))
        layout.addWidget(title)

        subtitle = QLabel("Analyze chiral centers and stereochemical properties")
        subtitle.setStyleSheet(self.theme_manager.get_subtitle_style())
        layout.addWidget(subtitle)

        # Input
        input_group = QGroupBox("Molecule Input")
        input_layout = QVBoxLayout()

        self.smiles_input = QTextEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES notation")
        self.smiles_input.setMaximumHeight(70)
        input_layout.addWidget(self.smiles_input)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Analyze button
        self.analyze_btn = QPushButton("🔬 Analyze Stereochemistry")
        self.analyze_btn.setStyleSheet(self.theme_manager.get_button_style("primary"))
        self.analyze_btn.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_btn)

        # Results
        results_group = QGroupBox("Analysis Results")
        results_layout = QVBoxLayout()

        self.results_text = QTextBrowser()
        self.results_text.setMinimumHeight(300)
        results_layout.addWidget(self.results_text)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        layout.addStretch()

    def analyze(self):
        """Analyze stereochemistry"""
        smiles = self.smiles_input.toPlainText().strip()

        if not smiles:
            QMessageBox.warning(self, "Input Required", "Please enter a SMILES string")
            return

        try:
            results = self.rdkit.analyze_stereochemistry(smiles)

            output = f"<h3 style='color: #1e40af;'>Stereochemistry Analysis</h3>"
            output += f"<p><b>SMILES:</b> {smiles}</p>"
            output += f"<p><b>Chiral Centers:</b> {results.get('chiral_centers', 0)}</p>"
            output += f"<p><b>Stereoisomers Possible:</b> {results.get('possible_stereoisomers', 0)}</p>"
            output += f"<p><b>Has Stereo Defined:</b> {results.get('has_stereo', 'No')}</p>"

            self.results_text.setHtml(output)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
