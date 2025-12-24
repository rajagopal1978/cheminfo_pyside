"""
Tree Menu Widget for RDKit Tools
Creates the left sidebar navigation tree
"""

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from tool_structure import TOOLS_STRUCTURE


class ToolTreeMenu(QTreeWidget):
    """Tree widget displaying all RDKit tools organized by category"""

    def __init__(self):
        super().__init__()
        self.setHeaderLabel("RDKit Tools")
        self.setMinimumWidth(250)
        self.setMaximumWidth(400)
        self.populate_tree()
        self.expandAll()
        self.apply_stylesheet()

    def populate_tree(self):
        """Populate tree with categories and tools"""
        for category_data in TOOLS_STRUCTURE:
            category_item = QTreeWidgetItem(self)
            category_item.setText(0, f"{category_data['icon']} {category_data['category']}")
            category_item.setData(0, Qt.UserRole, "category")

            # Set category font
            font = QFont()
            font.setBold(True)
            category_item.setFont(0, font)

            # Add tools
            for tool_data in category_data["tools"]:
                tool_item = QTreeWidgetItem(category_item)
                tool_item.setText(0, f"  {tool_data['icon']} {tool_data['name']}")
                tool_item.setData(0, Qt.UserRole, tool_data['id'])

    def apply_stylesheet(self):
        """Apply custom styles to tree widget"""
        self.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
                border-right: 1px solid #e2e8f0;
                padding: 10px;
                font-size: 13px;
            }

            QTreeWidget::item {
                padding: 8px;
                border-radius: 4px;
            }

            QTreeWidget::item:hover {
                background-color: #f1f5f9;
            }

            QTreeWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }

            QTreeWidget::branch {
                background: white;
            }
        """)
