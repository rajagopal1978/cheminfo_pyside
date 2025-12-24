"""
🎯 SMARTS Matcher Widget
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QMessageBox, QTextBrowser
)
from rdkit_handler import RDKitHandler
from theme_manager import ThemeManager


class SMARTSMatcherWidget(QWidget):
    """Widget for match molecules against smarts patterns"""

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
        title = QLabel("🎯 SMARTS Matcher")
        title.setStyleSheet(self.theme_manager.get_title_style("large"))
        layout.addWidget(title)

        subtitle = QLabel("Match molecules against SMARTS patterns")
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
        self.process_btn = QPushButton("🎯 Match Pattern")
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
            QMessageBox.warning(self, "Input Required", "Please enter SMARTS on the first line and SMILES (one per line) below")
            return

        try:
            lines = [l.strip() for l in input_data.splitlines() if l.strip()]
            if len(lines) < 2:
                QMessageBox.warning(self, "Input Required", "Please enter SMARTS on the first line and at least one SMILES on following lines")
                return

            smarts = lines[0]
            smiles = lines[1:]
            res = self.rdkit.match_smarts(smarts, smiles)

            output = f"<h3 style='color: #1e40af;'>🎯 SMARTS Matcher</h3>"
            output += f"<p><b>Pattern:</b> {res.get('pattern','')}</p>"
            output += f"<p><b>Matched Molecules:</b> {res.get('num_matched',0)} / {len(smiles)}</p>"
            output += "<ul>"
            for m in res.get('matches',[]):
                output += f"<li><b>{m['smiles']}</b>: {'✅' if m['matched'] else '❌'} (matches: {m['match_count']})</li>"
            output += "</ul>"

            self.results_text.setHtml(output)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
