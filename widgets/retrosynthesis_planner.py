"""
🔙 Retrosynthesis Planner Widget
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QMessageBox, QTextBrowser
)
from rdkit_handler import RDKitHandler
from theme_manager import ThemeManager


class RetrosynthesisPlannerWidget(QWidget):
    """Widget for plan retrosynthetic routes for target molecules"""

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
        title = QLabel("🔙 Retrosynthesis Planner")
        title.setStyleSheet(self.theme_manager.get_title_style("large"))
        layout.addWidget(title)

        subtitle = QLabel("Plan retrosynthetic routes for target molecules")
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
        self.process_btn = QPushButton("🔙 Plan Retrosynthesis")
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
            QMessageBox.warning(self, "Input Required", "Please enter a target SMILES on a single line")
            return

        try:
            lines = [l.strip() for l in input_data.splitlines() if l.strip()]
            target = lines[0]
            res = self.rdkit.plan_retrosynthesis(target)

            output = f"<h3 style='color: #1e40af;'>🔙 Retrosynthesis Planner</h3>"
            output += f"<p><b>Target:</b> {res.get('target','')}</p>"
            output += f"<p><b>Suggestions:</b> {len(res.get('suggestions',[]))}</p>"
            output += "<ol>"
            for s in res.get('suggestions',[]):
                output += f"<li>Cut bond idx {s.get('bond_idx')}: fragments - {', '.join(s.get('fragments',[]))}</li>"
            output += "</ol>"

            self.results_text.setHtml(output)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
