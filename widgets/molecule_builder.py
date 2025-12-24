"""
Molecule Builder Widget
Build molecules from SMILES and display properties
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGridLayout, QGroupBox, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import base64
from rdkit_handler import RDKitHandler


class MoleculeBuilderWidget(QWidget):
    """Widget for building molecules from SMILES notation"""

    def __init__(self):
        super().__init__()
        self.rdkit = RDKitHandler()
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("⚛️ Molecule Builder")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e40af; margin-bottom: 10px;")
        layout.addWidget(title)

        subtitle = QLabel("Build molecules from SMILES and display properties")
        subtitle.setStyleSheet("font-size: 14px; color: #64748b; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # Input section
        input_group = QGroupBox("SMILES Input")
        input_layout = QVBoxLayout()

        self.smiles_input = QTextEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES notation (e.g., CCO for ethanol)")
        self.smiles_input.setMaximumHeight(80)
        self.smiles_input.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 13px;
            }
        """)
        input_layout.addWidget(self.smiles_input)

        # Example buttons
        examples_label = QLabel("Quick Examples:")
        examples_label.setStyleSheet("font-size: 12px; color: #64748b; margin-top: 10px;")
        input_layout.addWidget(examples_label)

        examples_layout = QHBoxLayout()
        examples = [
            ("Ethanol", "CCO"),
            ("Aspirin", "CC(=O)Oc1ccccc1C(=O)O"),
            ("Caffeine", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"),
            ("Benzene", "c1ccccc1"),
        ]

        for name, smiles in examples:
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f1f5f9;
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                    padding: 6px 12px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #e0e7ff;
                    border-color: #6366f1;
                }
            """)
            btn.clicked.connect(lambda checked, s=smiles: self.smiles_input.setText(s))
            examples_layout.addWidget(btn)

        input_layout.addLayout(examples_layout)

        # Build button
        self.build_btn = QPushButton("🔨 Build Molecule")
        self.build_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.build_btn.clicked.connect(self.build_molecule)
        input_layout.addWidget(self.build_btn)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Results area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        scroll.setWidget(self.results_widget)

        layout.addWidget(scroll)

    def build_molecule(self):
        """Build molecule and display results"""
        smiles = self.smiles_input.toPlainText().strip()

        if not smiles:
            QMessageBox.warning(self, "Input Required", "Please enter a SMILES string")
            return

        try:
            # Clear previous results
            self.clear_results()

            # Parse molecule using local RDKit
            data = self.rdkit.parse_molecule(smiles)

            if not data.get('valid'):
                QMessageBox.critical(self, "Error", data.get('error', 'Invalid SMILES'))
                return

            # Generate 2D image
            img_base64 = self.rdkit.generate_2d_image(smiles, width=500, height=350)

            # Display results
            self.display_results(data, img_base64)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def display_results(self, data, img_base64):
        """Display molecule properties and 2D structure"""
        # 2D Structure
        self.add_2d_structure(img_base64)

        # Properties
        self.add_properties(data)

    def add_2d_structure(self, base64_image):
        """Add 2D structure image"""
        group = QGroupBox("2D Structure")
        layout = QVBoxLayout()

        # Decode base64 image
        img_data = base64.b64decode(base64_image.split(',')[1])
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)

        img_label = QLabel()
        img_label.setPixmap(pixmap)
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setStyleSheet("background-color: #f8fafc; border-radius: 8px; padding: 10px;")

        layout.addWidget(img_label)
        group.setLayout(layout)
        self.results_layout.addWidget(group)

    def add_properties(self, data):
        """Add molecular properties grid"""
        group = QGroupBox("Molecular Properties")
        grid = QGridLayout()
        grid.setSpacing(10)

        properties = [
            ("Formula", data.get('formula', 'N/A'), "#dbeafe"),
            ("Molecular Weight", f"{data.get('molecular_weight', 0):.2f} g/mol", "#dcfce7"),
            ("Atoms", str(data.get('atom_count', 0)), "#fef3c7"),
            ("Bonds", str(data.get('bond_count', 0)), "#fce7f3"),
            ("Rings", str(data.get('ring_count', 0)), "#e0e7ff"),
            ("Aromatic Rings", str(data.get('aromatic_rings', 0)), "#fce7f3"),
            ("LogP", f"{data.get('logp', 0):.2f}", "#fef3c7"),
            ("TPSA", f"{data.get('tpsa', 0):.2f} Ų", "#dcfce7"),
            ("H-Bond Donors", str(data.get('h_bond_donors', 0)), "#dbeafe"),
            ("H-Bond Acceptors", str(data.get('h_bond_acceptors', 0)), "#fce7f3"),
            ("Rotatable Bonds", str(data.get('rotatable_bonds', 0)), "#e0e7ff"),
        ]

        row, col = 0, 0
        for prop_name, prop_value, bg_color in properties:
            prop_widget = self.create_property_card(prop_name, prop_value, bg_color)
            grid.addWidget(prop_widget, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        group.setLayout(grid)
        self.results_layout.addWidget(group)

        # Canonical SMILES
        canonical_group = QGroupBox("Canonical SMILES")
        canonical_layout = QVBoxLayout()
        canonical_label = QLabel(data.get('canonical_smiles', 'N/A'))
        canonical_label.setStyleSheet("font-family: 'Courier New'; padding: 10px; background-color: #f1f5f9; border-radius: 4px;")
        canonical_label.setWordWrap(True)
        canonical_layout.addWidget(canonical_label)
        canonical_group.setLayout(canonical_layout)
        self.results_layout.addWidget(canonical_group)

    def create_property_card(self, name, value, bg_color):
        """Create a property card widget"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 11px; color: #64748b;")

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b;")

        layout.addWidget(name_label)
        layout.addWidget(value_label)

        return widget

    def clear_results(self):
        """Clear all results"""
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
