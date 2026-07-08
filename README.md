# Data Format Converter

A Python program that converts data between different formats: XML, JSON, and YAML.

## Project Overview

This project is developed incrementally across multiple tasks:

- **Task 1**: ✅ Command-line argument parsing and validation
- **Task 2**: File reading from various formats
- **Task 3**: Data object creation and JSON verification
- **Task 4**: YAML format reading and verification
- **Task 5**: XML format reading and verification
- **Task 6**: YAML format writing and verification
- **Task 7**: XML format writing and verification
- **Task 8**: PyQt UI implementation
- **Task 9**: Console version with async operations

## Supported Formats

- `.xml` - XML format
- `.json` - JSON format
- `.yaml` / `.yml` - YAML format

## Usage

```bash
python main.py <input_file> <output_file>
```

**Examples:**
```bash
python main.py data.json output.xml
python main.py config.yaml data.json
python main.py input.xml result.yaml
```

## Requirements

- Python 3.7+
- PyYAML (for YAML parsing in later tasks)
- PyQt5 (for UI implementation in Task 8)

## Project Structure

```
├── main.py              # Main entry point
├── arg_parser.py        # Command-line argument parsing (Task 1)
├── requirements.txt     # Project dependencies
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## Current Status

- ✅ Task 1: Argument parsing implemented
- ✅ Task 2: JSON file reading and syntax validation
- ✅ Task 3: JSON file writing and syntax verification
- ✅ Task 4: YAML file reading and syntax validation
- 🔄 Task 5-9: To be implemented

## How to Run

1. Ensure Python is installed
2. Run the program:
   ```bash
   python main.py input_file output_file
   ```
3. The program will validate the arguments and proceed with conversion
