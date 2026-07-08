"""
Argument parser module for the data format converter.
Task 1: Parsing command-line arguments passed to the program.
"""

import sys
import os
from pathlib import Path


SUPPORTED_FORMATS = {'.xml', '.json', '.yaml', '.yml'}


def validate_file_path(file_path):
    """
    Validate a file path.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if path is valid, False otherwise
    """
    if not file_path:
        return False
    
    # Check if file has an extension
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_FORMATS


def get_file_format(file_path):
    """
    Extract file format from file path.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File extension (lowercase) without the dot, or None if invalid
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext in SUPPORTED_FORMATS:
        return ext.lstrip('.')
    return None


def parse_arguments(args=None):
    """
    Parse command-line arguments for the data format converter.
    
    Expected usage: program.exe input_file output_file
    Where input_file and output_file must have different formats
    from the supported formats: .xml, .json, .yaml, .yml
    
    Args:
        args (list): Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        dict: Dictionary with keys 'input_file', 'output_file', 'input_format', 'output_format'
              or raises ValueError with error message
              
    Raises:
        ValueError: If arguments are invalid
    """
    if args is None:
        args = sys.argv[1:]
    
    # Check if correct number of arguments provided
    if len(args) != 2:
        raise ValueError(
            f"Invalid number of arguments. Expected 2, got {len(args)}.\n"
            f"Usage: program.exe <input_file> <output_file>\n"
            f"Supported formats: .xml, .json, .yaml, .yml"
        )
    
    input_file, output_file = args
    
    # Validate input file
    if not validate_file_path(input_file):
        raise ValueError(
            f"Invalid input file: '{input_file}'\n"
            f"File must have one of these extensions: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    # Validate output file
    if not validate_file_path(output_file):
        raise ValueError(
            f"Invalid output file: '{output_file}'\n"
            f"File must have one of these extensions: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    input_format = get_file_format(input_file)
    output_format = get_file_format(output_file)
    
    # Check if formats are different
    if input_format == output_format:
        raise ValueError(
            f"Input and output files must have different formats.\n"
            f"Input: .{input_format}, Output: .{output_format}"
        )
    
    return {
        'input_file': input_file,
        'output_file': output_file,
        'input_format': input_format,
        'output_format': output_format
    }


def print_usage():
    """Print usage information to the console."""
    print("Data Format Converter")
    print("=" * 50)
    print("Usage: program.exe <input_file> <output_file>")
    print("\nSupported formats: .xml, .json, .yaml, .yml")
    print("Note: Input and output files must have different formats")
    print("\nExample:")
    print("  program.exe data.json output.xml")
    print("  program.exe config.yaml data.json")
