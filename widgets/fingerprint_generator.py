"""
Fingerprint Generator Widget
Generate molecular fingerprints for similarity analysis
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QComboBox, QMessageBox, QTextBrowser
)
from rdkit_handler import RDKitHandler


class FingerprintGeneratorWidget(QWidget):
    """Widget for generating molecular fingerprints"""

    def __init__(self):
        super().__init__()
        self.rdkit = RDKitHandler()
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("👆 Fingerprint Generator")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e40af;")
        layout.addWidget(title)

        subtitle = QLabel("Generate molecular fingerprints for similarity calculations")
        subtitle.setStyleSheet("font-size: 14px; color: #64748b; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # Settings
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()

        # SMILES input
        self.smiles_input = QTextEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES notation")
        self.smiles_input.setMaximumHeight(80)
        settings_layout.addWidget(QLabel("SMILES:"))
        settings_layout.addWidget(self.smiles_input)

        # Fingerprint type
        type_label = QLabel("Fingerprint Type:")
        self.fp_type = QComboBox()
        self.fp_type.addItems([
            "morgan",
            "rdkit",
            "atompair",
            "torsion",
            "maccs"
        ])
        settings_layout.addWidget(type_label)
        settings_layout.addWidget(self.fp_type)

        # Generate button
        self.gen_btn = QPushButton("🔑 Generate Fingerprint")
        self.gen_btn.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover { background-color: #d97706; }
        """)
        self.gen_btn.clicked.connect(self.generate_fingerprint)
        settings_layout.addWidget(self.gen_btn)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Results
        results_group = QGroupBox("Fingerprint")
        results_layout = QVBoxLayout()

        self.results_browser = QTextBrowser()
        self.results_browser.setMinimumHeight(300)
        self.results_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #f8fafc;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
        """)
        results_layout.addWidget(self.results_browser)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

    def generate_fingerprint(self):
        """Generate molecular fingerprint"""
        smiles = self.smiles_input.toPlainText().strip()

        if not smiles:
            QMessageBox.warning(self, "Input Required", "Please enter a SMILES string")
            return

        try:
            fp_type = self.fp_type.currentText()
            data = self.rdkit.generate_fingerprint(smiles, fp_type)
            self.display_fingerprint(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_fingerprint(self, data):
        """Display fingerprint results"""
        fingerprint = data.get('fingerprint', '')

        html = f"""
        <div style='padding: 10px;'>
            <h3 style='color: #1e40af;'>Fingerprint Type: {data['type'].upper()}</h3>
            <p><b>Length:</b> {data['length']} bits</p>
            <p><b>Set Bits:</b> {data['set_bits']}</p>
            <hr>
            <h4>Binary Representation:</h4>
            <pre style='background-color: #f1f5f9; padding: 10px; border-radius: 4px; overflow-wrap: break-word;'>
{fingerprint}
            </pre>
        </div>
        """

        self.results_browser.setHtml(html)
