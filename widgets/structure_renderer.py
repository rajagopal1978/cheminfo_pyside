"""
Structure Renderer Widget
Render 2D and 3D molecular structures
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import base64
from rdkit_handler import RDKitHandler
from theme_manager import ThemeManager


class StructureRendererWidget(QWidget):
    """Widget for rendering molecular structures"""

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
        title = QLabel("🖼️ Structure Renderer")
        title.setStyleSheet(self.theme_manager.get_title_style("large"))
        layout.addWidget(title)

        subtitle = QLabel("Generate 2D molecular structure visualizations")
        subtitle.setStyleSheet(self.theme_manager.get_subtitle_style())
        layout.addWidget(subtitle)

        # Input group
        input_group = QGroupBox("Settings")
        input_layout = QVBoxLayout()

        # SMILES input
        smiles_label = QLabel("SMILES:")
        smiles_label.setStyleSheet("font-weight: 700; font-size: 14px;")
        self.smiles_input = QTextEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES notation (e.g., CCO for ethanol)")
        self.smiles_input.setMaximumHeight(70)
        input_layout.addWidget(smiles_label)
        input_layout.addWidget(self.smiles_input)

        # Render options with SpinBoxes
        options_layout = QHBoxLayout()
        options_layout.setSpacing(15)

        # Image size label
        size_label = QLabel("Image Size:")
        size_label.setStyleSheet("font-weight: 700; font-size: 14px;")
        options_layout.addWidget(size_label)

        # Width TextBox
        width_label = QLabel("Width (px):")
        width_label.setStyleSheet("font-weight: 600;")
        self.width_input = QLineEdit()
        self.width_input.setText("600")
        self.width_input.setPlaceholderText("200-1200")
        self.width_input.setMinimumWidth(100)
        self.width_input.setMaximumWidth(120)

        options_layout.addWidget(width_label)
        options_layout.addWidget(self.width_input)

        # Height TextBox
        height_label = QLabel("Height (px):")
        height_label.setStyleSheet("font-weight: 600;")
        self.height_input = QLineEdit()
        self.height_input.setText("400")
        self.height_input.setPlaceholderText("200-1200")
        self.height_input.setMinimumWidth(100)
        self.height_input.setMaximumWidth(120)

        options_layout.addWidget(height_label)
        options_layout.addWidget(self.height_input)
        options_layout.addStretch()

        input_layout.addLayout(options_layout)

        # Render button
        self.render_btn = QPushButton("🎨 Render Structure")
        self.render_btn.setStyleSheet(self.theme_manager.get_button_style("success"))
        self.render_btn.clicked.connect(self.render_structure)
        input_layout.addWidget(self.render_btn)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                min-height: 400px;
            }
        """)
        self.image_label.setText("Structure will appear here")
        self.image_label.setStyleSheet(self.image_label.styleSheet() + " color: #94a3b8;")
        layout.addWidget(self.image_label)
        layout.addStretch()

    def render_structure(self):
        """Render the molecular structure"""
        smiles = self.smiles_input.toPlainText().strip()

        if not smiles:
            QMessageBox.warning(self, "Input Required", "Please enter a SMILES string")
            return

        try:
            # Validate and get width
            try:
                width = int(self.width_input.text())
                if width < 200 or width > 1200:
                    raise ValueError("Width must be between 200 and 1200")
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", f"Width error: {str(e)}")
                return

            # Validate and get height
            try:
                height = int(self.height_input.text())
                if height < 200 or height > 1200:
                    raise ValueError("Height must be between 200 and 1200")
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", f"Height error: {str(e)}")
                return

            # Generate image using local RDKit
            img_base64 = self.rdkit.generate_2d_image(
                smiles,
                width=width,
                height=height
            )

            # Decode and display
            img_data = base64.b64decode(img_base64.split(',')[1])
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            self.image_label.setPixmap(pixmap)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
