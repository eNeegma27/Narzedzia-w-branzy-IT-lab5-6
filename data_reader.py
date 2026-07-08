"""
Data reader module for reading files in various formats.
Task 2: Reading data from JSON files and verifying syntax.
Task 4: Reading data from YAML files and verifying syntax.
"""

import json
import os
from pathlib import Path
import yaml


class DataReaderError(Exception):
    """Base exception for data reading errors."""
    pass


class FileNotFoundError(DataReaderError):
    """Raised when file does not exist."""
    pass


class SyntaxError(DataReaderError):
    """Raised when file has invalid syntax."""
    pass


def read_json_file(file_path):
    """
    Read and parse a JSON file.
    Task 2: Reading JSON file into object and verifying syntax.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict or list: Parsed JSON data
        
    Raises:
        FileNotFoundError: If file does not exist
        SyntaxError: If JSON syntax is invalid
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: '{file_path}'")
    
    # Check if it's actually a file (not a directory)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"'{file_path}' is not a file")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise SyntaxError(
            f"Invalid JSON syntax in '{file_path}':\n"
            f"  Line {e.lineno}, Column {e.colno}: {e.msg}"
        )
    except UnicodeDecodeError as e:
        raise SyntaxError(
            f"Cannot decode file '{file_path}' as UTF-8:\n"
            f"  {e}"
        )
    except Exception as e:
        raise SyntaxError(f"Error reading JSON file '{file_path}':\n  {e}")


def read_yaml_file(file_path):
    """
    Read and parse a YAML file.
    Task 4: Reading YAML file into object and verifying syntax.
    
    Args:
        file_path (str): Path to the YAML file
        
    Returns:
        dict or list: Parsed YAML data
        
    Raises:
        FileNotFoundError: If file does not exist
        SyntaxError: If YAML syntax is invalid
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: '{file_path}'")
    
    # Check if it's actually a file (not a directory)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"'{file_path}' is not a file")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Handle case where YAML file is empty
        if data is None:
            data = {}
        
        return data
    except yaml.YAMLError as e:
        raise SyntaxError(
            f"Invalid YAML syntax in '{file_path}':\n"
            f"  {e}"
        )
    except UnicodeDecodeError as e:
        raise SyntaxError(
            f"Cannot decode file '{file_path}' as UTF-8:\n"
            f"  {e}"
        )
    except Exception as e:
        raise SyntaxError(f"Error reading YAML file '{file_path}':\n  {e}")


def read_file(file_path, file_format):
    """
    Read file based on its format.
    Currently supports JSON (Task 2) and YAML (Task 4).
    
    Args:
        file_path (str): Path to the file
        file_format (str): File format ('json', 'xml', 'yaml', 'yml')
        
    Returns:
        dict or list: Parsed data
        
    Raises:
        DataReaderError: If file cannot be read or format is not supported
    """
    if file_format == 'json':
        return read_json_file(file_path)
    elif file_format in ('yaml', 'yml'):
        return read_yaml_file(file_path)
    else:
        raise DataReaderError(
            f"Format '{file_format}' is not yet supported for reading.\n"
            f"Currently supported: json, yaml, yml"
        )


def validate_data_structure(data, expected_type=None):
    """
    Validate parsed data structure.
    
    Args:
        data: Parsed data to validate
        expected_type (type): Expected data type (dict, list, etc.)
        
    Returns:
        bool: True if data is valid
        
    Raises:
        SyntaxError: If data structure is invalid
    """
    if data is None:
        raise SyntaxError("Parsed data is empty (None)")
    
    if expected_type and not isinstance(data, expected_type):
        raise SyntaxError(
            f"Invalid data structure. Expected {expected_type.__name__}, "
            f"got {type(data).__name__}"
        )
    
    return True
