"""
🧩 MCS Finder Widget
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QMessageBox, QTextBrowser
)
from rdkit_handler import RDKitHandler
from theme_manager import ThemeManager


class MCSFinderWidget(QWidget):
    """Widget for find maximum common substructure between molecules"""

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
        title = QLabel("🧩 MCS Finder")
        title.setStyleSheet(self.theme_manager.get_title_style("large"))
        layout.addWidget(title)

        subtitle = QLabel("Find maximum common substructure between molecules")
        subtitle.setStyleSheet(self.theme_manager.get_subtitle_style())
        layout.addWidget(subtitle)

        # Input
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter SMILES or input data")
        self.input_text.setMinimumHeight(100)
        input_layout.addWidget(self.input_text)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Process button
        self.process_btn = QPushButton("🧩 Find MCS")
        self.process_btn.setStyleSheet(self.theme_manager.get_button_style("primary"))
        self.process_btn.clicked.connect(self.process)
        layout.addWidget(self.process_btn)

        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()

        self.results_text = QTextBrowser()
        self.results_text.setMinimumHeight(300)
        results_layout.addWidget(self.results_text)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        layout.addStretch()

    def process(self):
        """Process the input"""
        input_data = self.input_text.toPlainText().strip()

        if not input_data:
            QMessageBox.warning(self, "Input Required", "Please enter input data")
            return

        try:
            # Parse input into SMILES list (split by newline, comma or whitespace)
            tokens = [t.strip() for t in input_data.replace(',', '\n').splitlines()]
            smiles_list = [t for t in tokens if t]

            if len(smiles_list) < 2:
                QMessageBox.warning(self, "Input Required", "Please enter at least two SMILES (one per line or comma-separated)")
                return

            res = self.rdkit.find_mcs(smiles_list)

            output = f"<h3 style='color: #1e40af;'>🧩 MCS Finder</h3>"
            output += f"<p><b>Input Count:</b> {res.get('num_molecules', 0)}</p>"
            output += f"<p><b>MCS SMARTS:</b> {res.get('smarts', '') or '&mdash;'}</p>"
            output += f"<p><b>MCS as SMILES:</b> {res.get('smarts_smiles', '') or '&mdash;'}</p>"
            output += f"<p><b>Atoms in MCS:</b> {res.get('num_atoms', 0)}</p>"
            output += f"<p><b>Bonds in MCS:</b> {res.get('num_bonds', 0)}</p>"
            output += f"<p><b>Status:</b> <span style='color: #10b981;'>{res.get('status')}</span></p>"

            self.results_text.setHtml(output)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
