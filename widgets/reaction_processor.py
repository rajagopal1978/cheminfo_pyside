"""
🔬 Reaction Processor Widget
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QMessageBox, QTextBrowser
)
from rdkit_handler import RDKitHandler
from theme_manager import ThemeManager


class ReactionProcessorWidget(QWidget):
    """Widget for process and analyze chemical reactions"""

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
        title = QLabel("🔬 Reaction Processor")
        title.setStyleSheet(self.theme_manager.get_title_style("large"))
        layout.addWidget(title)

        subtitle = QLabel("Process and analyze chemical reactions")
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
        self.process_btn = QPushButton("🔬 Process Reaction")
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
            QMessageBox.warning(self, "Input Required", "Please enter a reaction SMARTS on the first line and reactant sets below")
            return

        try:
            lines = [l.strip() for l in input_data.splitlines() if l.strip()]
            if len(lines) < 2:
                QMessageBox.warning(self, "Input Required", "Please enter reaction SMARTS on the first line and at least one reactant set (comma or dot-separated) on following lines")
                return

            reaction = lines[0]
            # Each following line is a reactant set (reactants separated by '.' or ',')
            reactant_sets = []
            for ln in lines[1:]:
                parts = [p.strip() for p in ln.replace(',', '.').split('.') if p.strip()]
                reactant_sets.append(parts)

            res = self.rdkit.process_reaction(reaction, reactant_sets)

            output = f"<h3 style='color: #1e40af;'>🔬 Reaction Processor</h3>"
            output += f"<p><b>Reaction:</b> {res.get('reaction', '')}</p>"
            output += f"<p><b>Results:</b></p><ul>"
            for r in res.get('results',[]):
                prods = r.get('products', [])
                output += f"<li><b>Reactants:</b> {', '.join(r.get('reactants',[]))} -> <b>Products:</b> {', '.join(prods) if prods else '&mdash;'} (<i>{r.get('status')}</i>)</li>"
            output += "</ul>"

            self.results_text.setHtml(output)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
