# A2L-Convert

A command-line toolkit for working with A2L files for ECU tuning. This toolkit helps in preparing A2L files for further processing, creates a database representation of the A2L data, exports the data to JSON format, and can generate C header files for direct memory access.

## Features

- Preprocesses A2L files to ensure compatibility
- Creates a database representation of the A2L data
- Exports A2L data to JSON format for easier processing
- Generates C header files with memory address definitions
- Command-line interface for easy integration into workflows
- Supports custom output file naming
- Includes header guards and proper C types based on variable sizes

## Requirements

- Python 3.6 or higher
- Required Python packages (install via pip):
  - pya2l
  - chardet

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/A2L-Convert.git
cd A2L-Convert
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Importing and Preprocessing A2L Files

Basic usage:
```bash
python import-a2l.py input_file.a2l
```

This will create a preprocessed file with "_preprocessed" suffix in the same directory.

To specify a custom output file:
```bash
python import-a2l.py input_file.a2l -o output_file.a2l
```

### Exporting to JSON

Basic usage:
```bash
python export-json.py input_file.a2l
```

This will create a JSON file with the same name as the input file but with a `.json` extension.

To specify a custom output file:
```bash
python export-json.py input_file.a2l -o output_file.json
```

### Converting JSON to C Header

Basic usage:
```bash
python json_to_c-header.py input_file.json
```

This will create a C header file with the same name as the input file but with a `.h` extension.

To specify a custom output file:
```bash
python json_to_c-header.py input_file.json -o output_file.h
```

The generated header file includes:
- Header guards
- Proper C types based on variable sizes (uint8_t, uint16_t, etc.)
- Memory address definitions with volatile pointers
- Bit mask support for bitfield access
- Original variable descriptions as comments

### Command-line Options

For import-a2l.py:
- `input_file`: Path to the input A2L file (required)
- `-o, --output`: Path to the output preprocessed A2L file (optional)
- `-h, --help`: Show help message and exit

For export-json.py:
- `input_file`: Path to the preprocessed A2L file (required)
- `-o, --output`: Path to the output JSON file (optional)
- `-h, --help`: Show help message and exit

For json_to_c-header.py:
- `input_file`: Path to the input JSON file (required)
- `-o, --output`: Path to the output header file (optional)
- `-h, --help`: Show help message and exit

## Typical Workflow

1. First, preprocess your A2L file:
```bash
python import-a2l.py your_file.a2l
```

2. Then export the data to JSON:
```bash
python export-json.py your_file_preprocessed.a2l
```

3. Finally, generate the C header file:
```bash
python json_to_c-header.py your_file.json
```

## Error Handling

All tools include error handling for common issues:
- Missing input files
- Processing errors
- File access problems
- Database errors
- JSON parsing errors
- Invalid data types or sizes

Error messages will be displayed in the console with appropriate exit codes.

## License

[Add your chosen license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.