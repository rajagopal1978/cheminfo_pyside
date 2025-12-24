"""
Conformer Generator Widget
Generate 3D conformers for molecules
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QLineEdit, QMessageBox, QTextBrowser
)
from PySide6.QtCore import Qt
from rdkit_handler import RDKitHandler
from theme_manager import ThemeManager


class ConformerGeneratorWidget(QWidget):
    """Widget for generating molecular conformers"""

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
        title = QLabel("🔄 Conformer Generator")
        title.setStyleSheet(self.theme_manager.get_title_style("large"))
        layout.addWidget(title)

        subtitle = QLabel("Generate 3D molecular conformers using RDKit")
        subtitle.setStyleSheet(self.theme_manager.get_subtitle_style())
        layout.addWidget(subtitle)

        # Input group
        input_group = QGroupBox("Molecule Input")
        input_layout = QVBoxLayout()

        smiles_label = QLabel("SMILES:")
        smiles_label.setStyleSheet("font-weight: 700; font-size: 14px;")
        self.smiles_input = QTextEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES notation (e.g., CCO)")
        self.smiles_input.setMaximumHeight(70)
        input_layout.addWidget(smiles_label)
        input_layout.addWidget(self.smiles_input)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Settings group
        settings_group = QGroupBox("Generation Settings")
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(15)

        # Number of conformers
        num_label = QLabel("Number of Conformers:")
        num_label.setStyleSheet("font-weight: 700; font-size: 14px;")
        self.num_input = QLineEdit()
        self.num_input.setText("10")
        self.num_input.setPlaceholderText("1-100")
        self.num_input.setMinimumWidth(100)
        self.num_input.setMaximumWidth(120)

        settings_layout.addWidget(num_label)
        settings_layout.addWidget(self.num_input)
        settings_layout.addStretch()

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Generate button
        self.generate_btn = QPushButton("🔄 Generate Conformers")
        self.generate_btn.setStyleSheet(self.theme_manager.get_button_style("primary"))
        self.generate_btn.clicked.connect(self.generate_conformers)
        layout.addWidget(self.generate_btn)

        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()

        self.results_text = QTextBrowser()
        self.results_text.setMinimumHeight(200)
        results_layout.addWidget(self.results_text)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        layout.addStretch()

    def generate_conformers(self):
        """Generate 3D conformers"""
        smiles = self.smiles_input.toPlainText().strip()

        if not smiles:
            QMessageBox.warning(self, "Input Required", "Please enter a SMILES string")
            return

        try:
            # Validate number of conformers
            try:
                num_conf = int(self.num_input.text())
                if num_conf < 1 or num_conf > 100:
                    raise ValueError("Number of conformers must be between 1 and 100")
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", f"Error: {str(e)}")
                return

            # Generate conformers
            results = self.rdkit.generate_conformers(smiles, num_conf)

            # Display results
            output = f"<h3 style='color: #1e40af;'>Conformer Generation Results</h3>"
            output += f"<p><b>SMILES:</b> {smiles}</p>"
            output += f"<p><b>Requested Conformers:</b> {num_conf}</p>"
            output += f"<p><b>Generated Conformers:</b> {results.get('num_conformers', 0)}</p>"
            output += f"<p><b>Status:</b> <span style='color: #10b981;'>{results.get('status', 'Unknown')}</span></p>"

            if 'energies' in results and results['energies']:
                output += "<h4 style='color: #1e40af;'>Conformer Energies (kcal/mol):</h4><ul>"
                for i, energy in enumerate(results['energies'][:10], 1):
                    output += f"<li>Conformer {i}: {energy:.4f}</li>"
                output += "</ul>"

            self.results_text.setHtml(output)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
