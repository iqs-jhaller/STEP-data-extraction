# STP Data Extraction

This Python module provides a suite of tools for extracting useful data from STP (STEP) files. It includes tools for:

1. **Color Analysis**: Extracting color values for each component in the assembly.
2. **Geometric Analysis**: Extracting geometric dimensions, physical properties, and origin locations of each component.
3. **Visualization**: Generating and saving PNG images of the assembly and individual components.
4. **Component Export**: Exporting individual components of the assembly as separate STP files.
5. **Topology Analysis**: Analysis of the assembly's hierarchical structure and geometric topology.
6. **Relationship Mapping**: Generating relationship matrices and assembly structure analysis.

## Requirements

- **Python 3.11** (Cannot be newer for pythonocc-core 7.9.0)
- **pythonocc-core 7.9.0** (OpenCASCADE Python bindings)
- **Pandas** (Data manipulation and analysis)
- **PrettyTable** (Formatted console output)
- **Conda environment** recommended for dependency management

## Environment Setup

**Recommended**: Use conda environment with pythonocc-core from conda-forge:

```bash
conda create -n your_env_name python=3.11
conda activate your_env_name
conda install -c conda-forge pythonocc-core=7.9.0
pip install pandas prettytable
```

## Usage

### Basic Usage

1. **Set the STEP file path** in `main.py`: (hardcoded paths to be removed in the future)
   ```python
   filename = "path/to/your/file.step"  # or .stp
   ```

2. **Run the main script**:
   ```bash
   python main.py
   ```

The script will perform comprehensive analysis including:
- Color extraction (if available)
- Geometric feature analysis
- Topology analysis with detailed hierarchy mapping
- Component relationship analysis
- Visual structure representation

### Output Examples

**Topology Analysis:**
```
Number of faces: 354
<class 'TopoDS_Compound'>
..<class 'TopoDS_Solid'>
..<class 'TopoDS_Solid'>
...
```

**Assembly Structure:**
```
Main Assembly: MainAssembly
  └─ Component_1
  └─ Component_2
  └─ Component_3
  ...
```

**Relationship Matrix:**
- For complex assemblies: 3-level hierarchy matrix (Parent → Child → Grandchild)
- For flat assemblies: 2-level relationship table (Assembly → Components)

## Key Features & Compatibility

### Recent Updates (Fork in September 2025)
- **Fixed pythonocc-core 7.9.0 compatibility** (API changes from older versions)
- **Enhanced topology analysis** with detailed shape hierarchy
- **Improved relationship matrix** handling for both flat and complex assemblies
- **Robust error handling** with fallback strategies for component naming
- **Generic component naming** when OCAF-based extraction fails

### Supported File Types
- STEP files (.step, .stp)
- Complex assemblies with sub-assemblies
- Flat assemblies with direct components

### Architecture
- **Modular design** with separate modules for different analysis types
- **Pandas DataFrames** for all tabular outputs (easily exportable to CSV, Excel, MongoDB)
- **OpenCASCADE integration** for robust geometric analysis
- **Flexible naming system** with fallback to generic names when needed

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure you're using the correct conda environment with pythonocc-core 7.9.0
2. **Empty relationship matrix**: Normal for flat assemblies without sub-assemblies
3. **Component naming failures**: Script automatically falls back to generic naming (Component_1, Component_2, etc.)

### API Compatibility Notes
- **pythonocc-core 7.9.0**: Uses `topods.Edge`/`topods.Vertex` (not `topods_Edge`/`topods_Vertex`)
- **Hash functions**: Uses `hash()` instead of deprecated `HashCode()` method
- **OCAF functionality**: May require additional setup for advanced component naming

## Output Data Formats

All tabular outputs are pandas DataFrames that can be easily:
- Exported to CSV: `df.to_csv('output.csv')`
- Exported to Excel: `df.to_excel('output.xlsx')`
- Loaded into MongoDB with minimal preprocessing
- Integrated into larger data analysis pipelines

## Module Structure

- `main.py`: Main execution script
- `Step_GetTopology.py`: Core topology analysis
- `Step_GetName.py`: Component naming extraction
- `Step_FileReader.py`: STEP file loading utilities
- `Step_GetGeometricFeatures.py`: Geometric analysis
- `Step_GetProperties.py`: Physical properties extraction
- `Step_GetColor_2.py`: Color analysis
- `utils.py`: Utility functions including relationship matrix generation


