"""
Theme Manager for RDKit Tools Application
Tailwind-style QSS Architecture with High Visibility
- Bold, clear fonts with proper sizing
- Visible spinner arrows and controls
- Optimal button proportions
- High contrast for all elements
"""

from color_themes import ColorThemes


class ThemeManager:
    """Manage and apply color themes to Qt application"""

    def __init__(self, theme_name="scientific_blue"):
        self.current_theme = ColorThemes.get_theme(theme_name)
        self.theme_name = theme_name

    def set_theme(self, theme_name):
        """Change the current theme"""
        self.current_theme = ColorThemes.get_theme(theme_name)
        self.theme_name = theme_name

    def get_main_stylesheet(self):
        """
        Tailwind-style QSS Architecture
        - All text bold and highly visible
        - Proper button proportions
        - Visible spinner arrows
        - Optimal font sizes
        """
        theme = self.current_theme

        return f"""
            /* ========== BASE STYLES ========== */
            QMainWindow {{
                background-color: #ffffff;
                font-family: "Segoe UI", "Arial", sans-serif;
            }}

            QWidget {{
                color: #1e293b;
                background-color: #ffffff;
                font-size: 14px;
                font-weight: 600;
            }}

            /* ========== TREE NAVIGATION ========== */
            QTreeWidget {{
                background-color: #ffffff;
                border: none;
                border-right: 2px solid #cbd5e1;
                padding: 10px;
                font-size: 14px;
                font-weight: 600;
                color: #1e293b;
            }}

            QTreeWidget::item {{
                padding: 10px 8px;
                border-radius: 6px;
                color: #334155;
                font-weight: 600;
            }}

            QTreeWidget::item:hover {{
                background-color: #f1f5f9;
                color: #1e40af;
                font-weight: 700;
            }}

            QTreeWidget::item:selected {{
                background-color: #dbeafe;
                color: #1e40af;
                font-weight: 700;
            }}

            QTreeWidget::branch {{
                background: #ffffff;
            }}

            /* ========== STACKED WIDGET ========== */
            QStackedWidget {{
                background-color: #ffffff;
            }}

            /* ========== GROUP BOX ========== */
            QGroupBox {{
                font-weight: 700;
                font-size: 15px;
                color: {theme['primary']};
                border: 2px solid #94a3b8;
                border-radius: 8px;
                margin-top: 14px;
                padding-top: 20px;
                background-color: #ffffff;
            }}

            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 10px;
                background-color: #ffffff;
                color: {theme['primary']};
                font-weight: 700;
                font-size: 15px;
            }}

            /* ========== TEXT INPUTS ========== */
            QTextEdit, QLineEdit {{
                border: 2px solid #94a3b8;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
                background-color: #ffffff;
                color: #0f172a;
            }}

            QTextEdit:focus, QLineEdit:focus {{
                border-color: {theme['primary']};
                border-width: 2px;
                background-color: #ffffff;
            }}

            /* ========== COMBOBOX ========== */
            QComboBox {{
                border: 2px solid #94a3b8;
                border-radius: 8px;
                padding: 10px 12px;
                min-width: 140px;
                min-height: 36px;
                background-color: #ffffff;
                color: #0f172a;
                font-size: 14px;
                font-weight: 700;
            }}

            QComboBox:hover {{
                border-color: {theme['secondary']};
                border-width: 2px;
            }}

            QComboBox:focus {{
                border-color: {theme['primary']};
                border-width: 3px;
            }}

            QComboBox::drop-down {{
                border: none;
                width: 30px;
                subcontrol-origin: padding;
                subcontrol-position: center right;
                padding-right: 8px;
            }}

            QComboBox::down-arrow {{
                image: none;
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid {theme['primary']};
            }}

            QComboBox QAbstractItemView {{
                background-color: #ffffff;
                color: #0f172a;
                border: 2px solid #94a3b8;
                selection-background-color: #dbeafe;
                selection-color: #1e40af;
                font-weight: 600;
                padding: 4px;
            }}

            /* ========== SPINBOX & DOUBLESPINBOX ========== */
            QSpinBox, QDoubleSpinBox {{
                border: 2px solid #94a3b8;
                border-radius: 8px;
                padding: 10px 12px;
                padding-right: 40px;
                min-width: 120px;
                min-height: 38px;
                background-color: #ffffff;
                color: #0f172a;
                font-size: 14px;
                font-weight: 700;
            }}

            QSpinBox:hover, QDoubleSpinBox:hover {{
                border-color: {theme['secondary']};
                border-width: 2px;
            }}

            QSpinBox:focus, QDoubleSpinBox:focus {{
                border-color: {theme['primary']};
                border-width: 3px;
            }}

            /* Spinner Up Button - Default Qt style with better visibility */
            QSpinBox::up-button, QDoubleSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 32px;
                height: 19px;
                border-left: 2px solid #cbd5e1;
                border-bottom: 1px solid #cbd5e1;
                border-top-right-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #e5e7eb);
            }}

            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f9ff, stop:1 #dbeafe);
            }}

            QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bfdbfe, stop:1 #93c5fd);
            }}

            /* Spinner Down Button - Default Qt style with better visibility */
            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 32px;
                height: 19px;
                border-left: 2px solid #cbd5e1;
                border-top: 1px solid #cbd5e1;
                border-bottom-right-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #e5e7eb);
            }}

            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f9ff, stop:1 #dbeafe);
            }}

            QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bfdbfe, stop:1 #93c5fd);
            }}

            /* Spinner Up Arrow - Larger and more visible */
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                image: none;
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-bottom: 8px solid #475569;
            }}

            QSpinBox::up-arrow:hover, QDoubleSpinBox::up-arrow:hover {{
                border-bottom-color: {theme['primary']};
            }}

            QSpinBox::up-arrow:pressed, QDoubleSpinBox::up-arrow:pressed {{
                border-bottom-color: #1e3a8a;
            }}

            /* Spinner Down Arrow - Larger and more visible */
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                image: none;
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #475569;
            }}

            QSpinBox::down-arrow:hover, QDoubleSpinBox::down-arrow:hover {{
                border-top-color: {theme['primary']};
            }}

            QSpinBox::down-arrow:pressed, QDoubleSpinBox::down-arrow:pressed {{
                border-top-color: #1e3a8a;
            }}

            /* ========== SCROLL BAR ========== */
            QScrollBar:vertical {{
                border: none;
                background: #f1f5f9;
                width: 14px;
                border-radius: 7px;
                margin: 2px;
            }}

            QScrollBar::handle:vertical {{
                background: #94a3b8;
                border-radius: 7px;
                min-height: 40px;
            }}

            QScrollBar::handle:vertical:hover {{
                background: {theme['primary']};
            }}

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            QScrollBar:horizontal {{
                border: none;
                background: #f1f5f9;
                height: 14px;
                border-radius: 7px;
                margin: 2px;
            }}

            QScrollBar::handle:horizontal {{
                background: #94a3b8;
                border-radius: 7px;
                min-width: 40px;
            }}

            QScrollBar::handle:horizontal:hover {{
                background: {theme['primary']};
            }}

            /* ========== LABELS ========== */
            QLabel {{
                color: #0f172a;
                background-color: transparent;
                font-weight: 600;
                font-size: 14px;
            }}

            /* ========== TABLE WIDGET ========== */
            QTableWidget {{
                border: 2px solid #94a3b8;
                border-radius: 8px;
                gridline-color: #cbd5e1;
                background-color: #ffffff;
                color: #0f172a;
                font-weight: 600;
                font-size: 14px;
            }}

            QTableWidget::item {{
                padding: 10px;
                color: #0f172a;
                background-color: #ffffff;
            }}

            QTableWidget::item:selected {{
                background-color: #dbeafe;
                color: #1e40af;
                font-weight: 700;
            }}

            QTableWidget::item:alternate {{
                background-color: #f8fafc;
            }}

            QHeaderView::section {{
                background-color: #f1f5f9;
                color: {theme['primary']};
                padding: 12px;
                border: 1px solid #94a3b8;
                font-weight: 700;
                font-size: 14px;
            }}

            /* ========== TEXT BROWSER ========== */
            QTextBrowser {{
                background-color: #ffffff;
                border: 2px solid #94a3b8;
                border-radius: 8px;
                padding: 14px;
                color: #0f172a;
                font-weight: 600;
                font-size: 14px;
                line-height: 1.6;
            }}

            /* ========== SCROLL AREA ========== */
            QScrollArea {{
                border: none;
                background-color: #ffffff;
            }}

            /* ========== MESSAGE BOX ========== */
            QMessageBox {{
                background-color: #ffffff;
                color: #0f172a;
                font-weight: 600;
            }}

            QMessageBox QLabel {{
                color: #0f172a;
                font-weight: 600;
                font-size: 14px;
            }}

            QMessageBox QPushButton {{
                min-width: 80px;
                min-height: 32px;
                font-weight: 700;
            }}
        """

    def get_button_style(self, button_type="primary"):
        """
        Tailwind-style button styles with optimal proportions
        - Bold, clear text
        - Proper padding and sizing
        - High contrast
        """
        theme = self.current_theme

        styles = {
            "primary": f"""
                QPushButton {{
                    background-color: {theme['primary']};
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                    padding: 14px 24px;
                    min-height: 44px;
                    font-size: 15px;
                    font-weight: 700;
                }}
                QPushButton:hover {{
                    background-color: {theme['secondary']};
                    color: #ffffff;
                }}
                QPushButton:pressed {{
                    background-color: #1e3a8a;
                    padding-top: 16px;
                    padding-bottom: 12px;
                }}
                QPushButton:disabled {{
                    background-color: #cbd5e1;
                    color: #64748b;
                }}
            """,
            "success": f"""
                QPushButton {{
                    background-color: {theme['success']};
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                    padding: 14px 24px;
                    min-height: 44px;
                    font-size: 15px;
                    font-weight: 700;
                }}
                QPushButton:hover {{
                    background-color: #059669;
                    color: #ffffff;
                }}
                QPushButton:pressed {{
                    background-color: #047857;
                    padding-top: 16px;
                    padding-bottom: 12px;
                }}
            """,
            "warning": f"""
                QPushButton {{
                    background-color: {theme['warning']};
                    color: #0f172a;
                    border: none;
                    border-radius: 8px;
                    padding: 14px 24px;
                    min-height: 44px;
                    font-size: 15px;
                    font-weight: 700;
                }}
                QPushButton:hover {{
                    background-color: #d97706;
                    color: #0f172a;
                }}
                QPushButton:pressed {{
                    background-color: #b45309;
                    padding-top: 16px;
                    padding-bottom: 12px;
                }}
            """,
            "danger": f"""
                QPushButton {{
                    background-color: {theme['danger']};
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                    padding: 14px 24px;
                    min-height: 44px;
                    font-size: 15px;
                    font-weight: 700;
                }}
                QPushButton:hover {{
                    background-color: #dc2626;
                    color: #ffffff;
                }}
                QPushButton:pressed {{
                    background-color: #b91c1c;
                    padding-top: 16px;
                    padding-bottom: 12px;
                }}
            """,
            "secondary": f"""
                QPushButton {{
                    background-color: #ffffff;
                    color: {theme['primary']};
                    border: 2px solid #94a3b8;
                    border-radius: 8px;
                    padding: 12px 22px;
                    min-height: 44px;
                    font-size: 15px;
                    font-weight: 700;
                }}
                QPushButton:hover {{
                    background-color: #f1f5f9;
                    border-color: {theme['primary']};
                    border-width: 3px;
                    color: {theme['primary']};
                }}
                QPushButton:pressed {{
                    background-color: #dbeafe;
                    border-color: #1e3a8a;
                }}
            """,
        }

        return styles.get(button_type, styles["primary"])

    def get_property_card_colors(self):
        """Get transparent cards with colored text only"""
        theme = self.current_theme

        # Return list of tuples (background_color, text_color, border_color)
        return [
            ("#ffffff", theme['primary'], "#cbd5e1"),
            ("#ffffff", theme['success'], "#cbd5e1"),
            ("#ffffff", theme['warning'], "#cbd5e1"),
            ("#ffffff", theme['secondary'], "#cbd5e1"),
            ("#ffffff", "#1e293b", "#cbd5e1"),
        ]

    def get_title_style(self, size="large"):
        """
        Title label styles with bold, high-visibility text
        """
        theme = self.current_theme

        sizes = {
            "large": ("32px", "800"),
            "medium": ("22px", "700"),
            "small": ("18px", "700"),
        }

        font_size, font_weight = sizes.get(size, ("32px", "800"))

        return f"""
            font-size: {font_size};
            font-weight: {font_weight};
            color: {theme['primary']};
            margin-bottom: 12px;
            background-color: transparent;
        """

    def get_subtitle_style(self):
        """Subtitle label style - medium gray, bold text"""
        return f"""
            font-size: 15px;
            font-weight: 600;
            color: #475569;
            margin-bottom: 20px;
            background-color: transparent;
        """

    def get_card_style(self, color_index=0):
        """
        Card style with visible borders and high contrast
        No colored backgrounds - only borders and text colors
        """
        colors = [
            "#1e40af",  # Blue
            "#10b981",  # Green
            "#f59e0b",  # Amber
            "#8b5cf6",  # Purple
            "#0f172a",  # Dark Gray
        ]

        border_color = colors[color_index % len(colors)]

        return f"""
            QWidget {{
                background-color: #ffffff;
                border: 2px solid #94a3b8;
                border-left: 5px solid {border_color};
                border-radius: 8px;
                padding: 16px;
            }}
            QLabel {{
                background-color: transparent;
                font-weight: 600;
            }}
        """


# Convenience function to get themed stylesheet
def get_app_stylesheet(theme_name="scientific_blue"):
    """Get complete application stylesheet for a theme"""
    manager = ThemeManager(theme_name)
    return manager.get_main_stylesheet()
