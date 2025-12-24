"""
RDKit Tools - PySide6 Application
Main application window with tree menu and tool widgets
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QSplitter
)
from PySide6.QtCore import Qt

# Import components
from tree_menu import ToolTreeMenu
from theme_manager import ThemeManager
from widgets.molecule_builder import MoleculeBuilderWidget
from widgets.structure_renderer import StructureRendererWidget
from widgets.conformer_generator import ConformerGeneratorWidget
from widgets.stereochemistry_analyzer import StereochemistryAnalyzerWidget
from widgets.property_calculator import PropertyCalculatorWidget
from widgets.lipinski_checker import LipinskiCheckerWidget
from widgets.descriptor_library import DescriptorLibraryWidget
from widgets.fingerprint_generator import FingerprintGeneratorWidget
from widgets.substructure_search import SubstructureSearchWidget
from widgets.similarity_search import SimilaritySearchWidget
from widgets.mcs_finder import MCSFinderWidget
from widgets.smarts_matcher import SMARTSMatcherWidget
from widgets.reaction_processor import ReactionProcessorWidget
from widgets.retrosynthesis_planner import RetrosynthesisPlannerWidget
from widgets.reaction_validator import ReactionValidatorWidget
from widgets.adme_predictor import ADMEPredictorWidget
from widgets.toxicity_predictor import ToxicityPredictorWidget
from widgets.fragment_generator import FragmentGeneratorWidget
from widgets.lead_optimizer import LeadOptimizerWidget
from widgets.format_converter import FormatConverterWidget
from widgets.batch_processor import BatchProcessorWidget
from widgets.database_curator import DatabaseCuratorWidget
from widgets.scaffold_analyzer import ScaffoldAnalyzerWidget
from widgets.rgroup_decomposition import RGroupDecompositionWidget
from widgets.matched_pairs import MatchedPairsWidget
from widgets.chemical_space_visualizer import ChemicalSpaceVisualizerWidget
from widgets.diversity_picker import DiversityPickerWidget
from widgets.clustering_engine import ClusteringEngineWidget
from widgets.quantum_descriptors import QuantumDescriptorsWidget
from widgets.pharmacophore_detector import PharmacophoreDetectorWidget
from widgets.shape_similarity import ShapeSimilarityWidget
from widgets.molecular_alignment import MolecularAlignmentWidget
from widgets.protein_ligand_analyzer import ProteinLigandAnalyzerWidget
from widgets.fragment_library_generator import FragmentLibraryGeneratorWidget
from widgets.bioavailability_optimizer import BioavailabilityOptimizerWidget
from widgets.salt_stripper import SaltStripperWidget


class RDKitToolsApp(QMainWindow):
    """Main application window for RDKit Chemistry Tools"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RDKit Chemistry Tools")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize theme manager with Scientific Blue theme
        self.theme_manager = ThemeManager("scientific_blue")

        self.setup_ui()
        self.apply_stylesheet()

    def setup_ui(self):
        """Setup the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)

        # Create left panel (tree menu)
        self.tree_widget = ToolTreeMenu()
        splitter.addWidget(self.tree_widget)

        # Create right panel (stacked widget for tools)
        self.stacked_widget = QStackedWidget()
        self.create_tool_widgets()
        splitter.addWidget(self.stacked_widget)

        # Set splitter sizes (20% tree, 80% content)
        splitter.setSizes([280, 1120])

        main_layout.addWidget(splitter)

        # Connect tree selection to tool display
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)

        # Show welcome page by default
        self.show_welcome_page()

    def create_tool_widgets(self):
        """Create all tool widgets and add to stacked widget"""
        # Welcome page
        welcome = self.create_welcome_page()
        self.stacked_widget.addWidget(welcome)

        # Tool widgets mapping - All 36 tools
        self.tool_widgets = {
            "tool-1": MoleculeBuilderWidget(),
            "tool-2": StructureRendererWidget(),
            "tool-3": ConformerGeneratorWidget(),
            "tool-4": StereochemistryAnalyzerWidget(),
            "tool-5": PropertyCalculatorWidget(),
            "tool-6": LipinskiCheckerWidget(),
            "tool-7": DescriptorLibraryWidget(),
            "tool-8": FingerprintGeneratorWidget(),
            "tool-9": SubstructureSearchWidget(),
            "tool-10": SimilaritySearchWidget(),
            "tool-11": MCSFinderWidget(),
            "tool-12": SMARTSMatcherWidget(),
            "tool-13": ReactionProcessorWidget(),
            "tool-14": RetrosynthesisPlannerWidget(),
            "tool-15": ReactionValidatorWidget(),
            "tool-16": ADMEPredictorWidget(),
            "tool-17": ToxicityPredictorWidget(),
            "tool-18": FragmentGeneratorWidget(),
            "tool-19": LeadOptimizerWidget(),
            "tool-20": FormatConverterWidget(),
            "tool-21": BatchProcessorWidget(),
            "tool-22": DatabaseCuratorWidget(),
            "tool-23": ScaffoldAnalyzerWidget(),
            "tool-24": RGroupDecompositionWidget(),
            "tool-25": MatchedPairsWidget(),
            "tool-26": ChemicalSpaceVisualizerWidget(),
            "tool-27": DiversityPickerWidget(),
            "tool-28": ClusteringEngineWidget(),
            "tool-29": QuantumDescriptorsWidget(),
            "tool-30": PharmacophoreDetectorWidget(),
            "tool-31": ShapeSimilarityWidget(),
            "tool-32": MolecularAlignmentWidget(),
            "tool-33": ProteinLigandAnalyzerWidget(),
            "tool-34": FragmentLibraryGeneratorWidget(),
            "tool-35": BioavailabilityOptimizerWidget(),
            "tool-36": SaltStripperWidget(),
        }

        # Add tool widgets to stacked widget
        for tool_id, widget in self.tool_widgets.items():
            self.stacked_widget.addWidget(widget)

        # Placeholder for not implemented tools
        self.placeholder_widget = self.create_placeholder_widget()
        self.stacked_widget.addWidget(self.placeholder_widget)

    def create_welcome_page(self):
        """Create the welcome page widget"""
        welcome = QWidget()
        welcome_layout = QVBoxLayout(welcome)
        welcome_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("🧬 RDKit Chemistry Tools")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #1e40af;")
        welcome_layout.addWidget(title)

        subtitle = QLabel("Select a tool from the menu to get started")
        subtitle.setStyleSheet("font-size: 18px; color: #64748b; margin-top: 10px;")
        welcome_layout.addWidget(subtitle)

        info = QLabel("36 tools across 10 categories")
        info.setStyleSheet("font-size: 14px; color: #94a3b8; margin-top: 20px;")
        welcome_layout.addWidget(info)

        return welcome

    def create_placeholder_widget(self):
        """Create placeholder for tools not yet implemented"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        icon = QLabel("🔧")
        icon.setStyleSheet("font-size: 72px;")
        layout.addWidget(icon)

        title = QLabel("Tool Coming Soon")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #64748b; margin-top: 20px;")
        layout.addWidget(title)

        info = QLabel("This tool is currently under development")
        info.setStyleSheet("font-size: 14px; color: #94a3b8; margin-top: 10px;")
        layout.addWidget(info)

        return widget

    def show_welcome_page(self):
        """Show the welcome page"""
        self.stacked_widget.setCurrentIndex(0)

    def on_tree_item_clicked(self, item, column):
        """Handle tree item click event"""
        tool_id = item.data(0, Qt.UserRole)

        # Ignore category clicks
        if tool_id == "category":
            return

        # Show appropriate tool widget
        if tool_id in self.tool_widgets:
            widget = self.tool_widgets[tool_id]
            self.stacked_widget.setCurrentWidget(widget)
        else:
            # Show placeholder for not implemented tools
            self.stacked_widget.setCurrentWidget(self.placeholder_widget)

    def apply_stylesheet(self):
        """Apply global stylesheet using ThemeManager"""
        # Use ThemeManager's high-contrast, white background stylesheet
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Set application metadata
    app.setApplicationName("RDKit Tools")
    app.setOrganizationName("Cheminformatics")

    # Create and show main window
    window = RDKitToolsApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
