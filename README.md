# RDKit Tools - Standalone PySide6 Desktop Application

A **monolithic standalone** desktop application for RDKit chemistry tools built with PySide6 (Qt for Python). No external dependencies or API connections required - all RDKit processing happens locally within the application.

## Features

- **🎯 Standalone Application**: No backend server needed - everything runs locally
- **📁 Tree Menu Navigation**: Browse 36 RDKit tools organized in 10 categories
- **🎨 Interactive Widgets**: Rich UI for each tool with real-time molecule visualization
- **⚡ Direct RDKit Integration**: Fast local processing using rdkit_handler.py
- **💅 Modern UI**: Clean, responsive interface with Tailwind-inspired styling
- **📦 Monolithic Design**: All logic in one application, no API calls

## Implemented Tools

1. **Molecule Builder** ⚛️ - Build molecules from SMILES and display 11 properties
2. **Structure Renderer** 🖼️ - Generate 2D molecular structure visualizations
3. **Property Calculator** 🧮 - Calculate comprehensive molecular descriptors
4. **Lipinski Rule Checker** 💊 - Check drug-likeness using Lipinski's Rule of Five
5. **Fingerprint Generator** 👆 - Generate 5 types of molecular fingerprints
6. **Similarity Search** 🔬 - Find similar molecules using Tanimoto similarity

## Requirements

```bash
pip install PySide6 rdkit
```

## Project Structure

```
pyside6/
├── main.py                          # Main application (220 lines)
├── rdkit_handler.py                 # RDKit processing logic (230 lines)
├── tool_structure.py                # Tool menu structure (103 lines)
├── tree_menu.py                     # Tree menu widget (70 lines)
├── widgets/
│   ├── __init__.py                  # Package init
│   ├── molecule_builder.py          # Molecule builder widget (247 lines)
│   ├── structure_renderer.py        # Structure renderer widget (135 lines)
│   ├── property_calculator.py       # Property calculator widget (129 lines)
│   ├── lipinski_checker.py          # Lipinski checker widget (150 lines)
│   ├── fingerprint_generator.py     # Fingerprint generator widget (132 lines)
│   └── similarity_search.py         # Similarity search widget (168 lines)
├── requirements.txt
└── README.md
```

**All files kept under 300 lines for maintainability.**

## Installation

### 1. Install Dependencies

```bash
cd pyside6
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

**That's it!** No backend server needed.

## Usage

1. **Navigate**: Click on categories in the left tree menu to expand them
2. **Select Tool**: Click on a tool name to load it in the main area
3. **Use Tool**: Each tool has its own interface with input fields and action buttons
4. **View Results**: Results are displayed instantly in formatted panels

## Example Workflows

### Molecule Builder
1. Enter SMILES notation (e.g., "CCO" for ethanol)
2. Or click a quick example button (Aspirin, Caffeine, Benzene)
3. Click "🔨 Build Molecule"
4. View 2D structure image and 11 molecular properties in colorful cards
5. See canonical SMILES representation

### Lipinski Rule Checker
1. Enter SMILES notation
2. Click "✓ Check Lipinski Rules"
3. See instant pass/fail results for:
   - Molecular Weight ≤ 500 Da
   - LogP ≤ 5
   - H-Bond Donors ≤ 5
   - H-Bond Acceptors ≤ 10
4. Color-coded results (green = pass, red = fail)

### Similarity Search
1. Enter query molecule SMILES
2. Enter target molecules (one per line)
3. Set similarity threshold (0.0 - 1.0)
4. Click "🔍 Search Similar Molecules"
5. View ranked results with Tanimoto similarity scores

## Architecture

### Monolithic Design

All RDKit processing happens in `rdkit_handler.py`:

```python
class RDKitHandler:
    @staticmethod
    def parse_molecule(smiles) -> dict

    @staticmethod
    def generate_2d_image(smiles, width, height) -> str

    @staticmethod
    def generate_fingerprint(smiles, fp_type) -> dict

    @staticmethod
    def calculate_similarity(query, targets, threshold) -> list

    @staticmethod
    def check_lipinski(smiles) -> dict
```

Each widget imports and uses `RDKitHandler` directly - no network calls, no API endpoints.

## Adding New Tools

To add a new tool widget:

1. Create new widget file in `widgets/` (keep under 300 lines):
```python
from rdkit_handler import RDKitHandler

class NewToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.rdkit = RDKitHandler()
        self.setup_ui()
```

2. Import the widget in `main.py`
3. Add to `self.tool_widgets` dictionary with appropriate tool-id
4. Widget automatically appears when selected from menu

## Styling

- **Qt Fusion Style**: Cross-platform Qt style
- **Tailwind-Inspired Colors**: Blue, green, purple, orange themes
- **Responsive Layouts**: Splitters and scroll areas
- **Group Boxes**: Organized sections for inputs/results
- **Custom Buttons**: Colored buttons with hover effects

## Performance

- **Instant Results**: No network latency
- **Local Processing**: All RDKit calculations run in-process
- **Efficient**: Direct Python API calls, no serialization overhead
- **Responsive UI**: Qt event loop keeps UI responsive during calculations

## Notes

- **Standalone**: No Django or any backend server required
- **Self-Contained**: All logic in one application
- **No Network**: Works completely offline
- **Error Handling**: QMessageBox dialogs for user-friendly error messages
- **Tree Menu**: Fully expandable/collapsible categories
- **Modern UI**: Professional appearance with icons and colors

## Troubleshooting

**RDKit Import Error**:
```bash
pip install rdkit
# or conda install -c conda-forge rdkit
```

**PySide6 Issues**:
```bash
pip install --upgrade PySide6
```

## License

Open source - use for educational or commercial purposes.
