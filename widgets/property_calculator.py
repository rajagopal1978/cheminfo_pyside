"""
Property Calculator Widget
Calculate molecular properties and descriptors
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QGridLayout, QMessageBox, QScrollArea
)
from rdkit_handler import RDKitHandler


class PropertyCalculatorWidget(QWidget):
    """Widget for calculating molecular properties"""

    def __init__(self):
        super().__init__()
        self.rdkit = RDKitHandler()
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("🧮 Property Calculator")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e40af;")
        layout.addWidget(title)

        subtitle = QLabel("Calculate comprehensive molecular properties and descriptors")
        subtitle.setStyleSheet("font-size: 14px; color: #64748b; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # Input
        input_group = QGroupBox("SMILES Input")
        input_layout = QVBoxLayout()

        self.smiles_input = QTextEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES notation")
        self.smiles_input.setMaximumHeight(80)
        input_layout.addWidget(self.smiles_input)

        self.calc_btn = QPushButton("📊 Calculate Properties")
        self.calc_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #7c3aed; }
        """)
        self.calc_btn.clicked.connect(self.calculate_properties)
        input_layout.addWidget(self.calc_btn)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Results
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        scroll.setWidget(self.results_widget)
        layout.addWidget(scroll)

    def calculate_properties(self):
        """Calculate molecular properties"""
        smiles = self.smiles_input.toPlainText().strip()

        if not smiles:
            QMessageBox.warning(self, "Input Required", "Please enter a SMILES string")
            return

        try:
            data = self.rdkit.parse_molecule(smiles)

            if not data.get('valid'):
                QMessageBox.critical(self, "Error", data.get('error', 'Invalid SMILES'))
                return

            self.display_properties(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_properties(self, data):
        """Display calculated properties"""
        # Clear previous results
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Create properties grid
        group = QGroupBox("Calculated Properties")
        grid = QGridLayout()

        properties = [
            ("Molecular Formula", data.get('formula', 'N/A')),
            ("Molecular Weight", f"{data.get('molecular_weight', 0):.2f} g/mol"),
            ("Atom Count", str(data.get('atom_count', 0))),
            ("Bond Count", str(data.get('bond_count', 0))),
            ("Ring Count", str(data.get('ring_count', 0))),
            ("Aromatic Rings", str(data.get('aromatic_rings', 0))),
            ("LogP", f"{data.get('logp', 0):.2f}"),
            ("TPSA", f"{data.get('tpsa', 0):.2f} Ų"),
            ("H-Bond Donors", str(data.get('h_bond_donors', 0))),
            ("H-Bond Acceptors", str(data.get('h_bond_acceptors', 0))),
            ("Rotatable Bonds", str(data.get('rotatable_bonds', 0))),
            ("Canonical SMILES", data.get('canonical_smiles', 'N/A')),
        ]

        for i, (name, value) in enumerate(properties):
            name_label = QLabel(name + ":")
            name_label.setStyleSheet("font-weight: bold;")
            value_label = QLabel(str(value))
            value_label.setStyleSheet("color: #1e40af;")

            grid.addWidget(name_label, i, 0)
            grid.addWidget(value_label, i, 1)

        group.setLayout(grid)
        self.results_layout.addWidget(group)
