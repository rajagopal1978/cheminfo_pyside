"""
Lipinski Rule Checker Widget
Check drug-likeness using Lipinski's Rule of Five
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from rdkit_handler import RDKitHandler


class LipinskiCheckerWidget(QWidget):
    """Widget for checking Lipinski's Rule of Five"""

    def __init__(self):
        super().__init__()
        self.rdkit = RDKitHandler()
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("💊 Lipinski Rule Checker")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e40af;")
        layout.addWidget(title)

        subtitle = QLabel("Evaluate drug-likeness using Lipinski's Rule of Five")
        subtitle.setStyleSheet("font-size: 14px; color: #64748b; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # Info box
        info_group = QGroupBox("Lipinski's Rule of Five")
        info_layout = QVBoxLayout()
        info_text = QLabel(
            "A compound is considered drug-like if it meets these criteria:\n\n"
            "• Molecular Weight ≤ 500 Da\n"
            "• LogP ≤ 5\n"
            "• H-Bond Donors ≤ 5\n"
            "• H-Bond Acceptors ≤ 10\n\n"
            "Compounds meeting these rules are more likely to have good oral bioavailability."
        )
        info_text.setStyleSheet("padding: 10px; background-color: #eff6ff; border-radius: 8px;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Input
        input_group = QGroupBox("Molecule Input")
        input_layout = QVBoxLayout()

        self.smiles_input = QTextEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES notation")
        self.smiles_input.setMaximumHeight(80)
        input_layout.addWidget(self.smiles_input)

        self.check_btn = QPushButton("✓ Check Lipinski Rules")
        self.check_btn.setStyleSheet("""
            QPushButton {
                background-color: #ec4899;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #db2777; }
        """)
        self.check_btn.clicked.connect(self.check_lipinski)
        input_layout.addWidget(self.check_btn)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Results
        self.results_group = QGroupBox("Results")
        self.results_layout = QVBoxLayout()
        self.results_label = QLabel()
        self.results_label.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(self.results_label)
        self.results_group.setLayout(self.results_layout)
        self.results_group.hide()
        layout.addWidget(self.results_group)

        layout.addStretch()

    def check_lipinski(self):
        """Check Lipinski's rules"""
        smiles = self.smiles_input.toPlainText().strip()

        if not smiles:
            QMessageBox.warning(self, "Input Required", "Please enter a SMILES string")
            return

        try:
            data = self.rdkit.check_lipinski(smiles)
            self.display_results(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_results(self, data):
        """Display Lipinski rule check results"""
        mw = data['molecular_weight']
        logp = data['logp']
        hbd = data['h_bond_donors']
        hba = data['h_bond_acceptors']
        violations = data['violations']

        # Create results HTML
        result_html = f"""
        <div style='padding: 20px; background-color: #f8fafc; border-radius: 8px;'>
            <h2 style='color: {'#10b981' if violations == 0 else '#ef4444'}; text-align: center;'>
                {'✓ PASS' if violations == 0 else f'✗ FAIL ({violations} violations)'}
            </h2>
            <table style='width: 100%; margin-top: 20px; border-collapse: collapse;'>
                <tr style='background-color: {'#d1fae5' if data['mw_pass'] else '#fee2e2'}'>
                    <td style='padding: 10px;'><b>Molecular Weight</b></td>
                    <td style='padding: 10px;'>{mw:.2f} Da</td>
                    <td style='padding: 10px;'>{'✓ ≤ 500' if data['mw_pass'] else '✗ > 500'}</td>
                </tr>
                <tr style='background-color: {'#d1fae5' if data['logp_pass'] else '#fee2e2'}'>
                    <td style='padding: 10px;'><b>LogP</b></td>
                    <td style='padding: 10px;'>{logp:.2f}</td>
                    <td style='padding: 10px;'>{'✓ ≤ 5' if data['logp_pass'] else '✗ > 5'}</td>
                </tr>
                <tr style='background-color: {'#d1fae5' if data['hbd_pass'] else '#fee2e2'}'>
                    <td style='padding: 10px;'><b>H-Bond Donors</b></td>
                    <td style='padding: 10px;'>{hbd}</td>
                    <td style='padding: 10px;'>{'✓ ≤ 5' if data['hbd_pass'] else '✗ > 5'}</td>
                </tr>
                <tr style='background-color: {'#d1fae5' if data['hba_pass'] else '#fee2e2'}'>
                    <td style='padding: 10px;'><b>H-Bond Acceptors</b></td>
                    <td style='padding: 10px;'>{hba}</td>
                    <td style='padding: 10px;'>{'✓ ≤ 10' if data['hba_pass'] else '✗ > 10'}</td>
                </tr>
            </table>
        </div>
        """

        self.results_label.setText(result_html)
        self.results_label.setTextFormat(Qt.RichText)
        self.results_group.show()
