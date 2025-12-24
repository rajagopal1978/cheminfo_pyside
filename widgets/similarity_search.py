"""
Similarity Search Widget
Find similar molecules using fingerprint similarity
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QLineEdit,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from rdkit_handler import RDKitHandler
from theme_manager import ThemeManager


class SimilaritySearchWidget(QWidget):
    """Widget for molecular similarity searching"""

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
        title = QLabel("🔬 Similarity Search")
        title.setStyleSheet(self.theme_manager.get_title_style("large"))
        layout.addWidget(title)

        subtitle = QLabel("Find similar molecules using Tanimoto similarity")
        subtitle.setStyleSheet(self.theme_manager.get_subtitle_style())
        layout.addWidget(subtitle)

        # Query input
        query_group = QGroupBox("Query Molecule")
        query_layout = QVBoxLayout()

        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("Enter query SMILES")
        self.query_input.setMaximumHeight(60)
        query_layout.addWidget(self.query_input)

        query_group.setLayout(query_layout)
        layout.addWidget(query_group)

        # Target molecules
        target_group = QGroupBox("Target Molecules (one per line)")
        target_layout = QVBoxLayout()

        self.target_input = QTextEdit()
        self.target_input.setPlaceholderText("Enter target SMILES (one per line)")
        self.target_input.setMinimumHeight(120)
        target_layout.addWidget(self.target_input)

        target_group.setLayout(target_layout)
        layout.addWidget(target_group)

        # Settings
        settings_group = QGroupBox("Search Settings")
        settings_layout = QVBoxLayout()

        # Similarity threshold with horizontal layout
        threshold_layout = QHBoxLayout()
        threshold_layout.setSpacing(15)

        threshold_label = QLabel("Similarity Threshold:")
        threshold_label.setStyleSheet("font-weight: 700; font-size: 14px;")

        self.threshold_input = QLineEdit()
        self.threshold_input.setText("0.7")
        self.threshold_input.setPlaceholderText("0.0 - 1.0")
        self.threshold_input.setMinimumWidth(100)
        self.threshold_input.setMaximumWidth(120)

        threshold_help = QLabel("(0.0 - 1.0, higher = more similar)")
        threshold_help.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 500;")

        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.threshold_input)
        threshold_layout.addWidget(threshold_help)
        threshold_layout.addStretch()

        settings_layout.addLayout(threshold_layout)

        # Search button
        self.search_btn = QPushButton("🔍 Search Similar Molecules")
        self.search_btn.setStyleSheet(self.theme_manager.get_button_style("primary"))
        self.search_btn.clicked.connect(self.search_similar)
        settings_layout.addWidget(self.search_btn)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Results table
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Rank", "SMILES", "Similarity"])
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.results_table.setAlternatingRowColors(True)
        results_layout.addWidget(self.results_table)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

    def search_similar(self):
        """Search for similar molecules"""
        query = self.query_input.toPlainText().strip()
        targets = [line.strip() for line in self.target_input.toPlainText().split('\n') if line.strip()]

        if not query:
            QMessageBox.warning(self, "Input Required", "Please enter a query SMILES")
            return

        if not targets:
            QMessageBox.warning(self, "Input Required", "Please enter target SMILES")
            return

        try:
            # Validate and get threshold
            try:
                threshold = float(self.threshold_input.text())
                if threshold < 0.0 or threshold > 1.0:
                    raise ValueError("Threshold must be between 0.0 and 1.0")
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", f"Threshold error: {str(e)}")
                return

            results = self.rdkit.calculate_similarity(
                query,
                targets,
                threshold=threshold
            )

            self.display_results(results)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_results(self, results):
        """Display search results"""
        self.results_table.setRowCount(0)

        # Sort by similarity (descending)
        results.sort(key=lambda x: x.get('similarity', 0), reverse=True)

        for i, result in enumerate(results):
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)

            rank_item = QTableWidgetItem(str(i + 1))
            rank_item.setTextAlignment(Qt.AlignCenter)

            smiles_item = QTableWidgetItem(result.get('smiles', ''))

            similarity = result.get('similarity', 0)
            similarity_item = QTableWidgetItem(f"{similarity:.4f}")
            similarity_item.setTextAlignment(Qt.AlignCenter)

            # Color code by similarity
            if similarity >= 0.9:
                similarity_item.setBackground(QColor("#d1fae5"))
            elif similarity >= 0.7:
                similarity_item.setBackground(QColor("#fef3c7"))

            self.results_table.setItem(row, 0, rank_item)
            self.results_table.setItem(row, 1, smiles_item)
            self.results_table.setItem(row, 2, similarity_item)

        if not results:
            QMessageBox.information(self, "No Results",
                                  "No molecules found above the similarity threshold")
