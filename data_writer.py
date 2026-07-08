"""
Data writer module for writing files in various formats.
Task 3: Writing data from object to JSON file with proper syntax.
"""

import json
import os
from pathlib import Path
from datetime import date, datetime


class DataWriterError(Exception):
    """Base exception for data writing errors."""
    pass


def serialize_for_json(obj):
    """
    Custom JSON serializer for objects not serializable by default json code.
    Handles date and datetime objects.
    
    Args:
        obj: Object to serialize
        
    Returns:
        str: ISO format string for dates, or raises TypeError
    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def write_json_file(file_path, data, indent=2):
    """
    Write data to a JSON file with proper formatting.
    Task 3: Writing data from object to JSON file and verifying syntax.
    
    Args:
        file_path (str): Path to the output JSON file
        data (dict or list): Python object to write
        indent (int): Number of spaces for indentation (default: 2)
        
    Returns:
        bool: True if write was successful
        
    Raises:
        DataWriterError: If file cannot be written
    """
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            raise DataWriterError(
                f"Cannot create directory '{directory}':\n  {e}"
            )
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False, default=serialize_for_json)
        return True
    except TypeError as e:
        raise DataWriterError(
            f"Cannot serialize data to JSON:\n"
            f"  {e}\n"
            f"  Note: Only dict, list, str, int, float, bool, None, and date/datetime are JSON-serializable"
        )
    except Exception as e:
        raise DataWriterError(
            f"Error writing JSON file '{file_path}':\n  {e}"
        )


def write_file(file_path, data, file_format):
    """
    Write file based on its format.
    Currently supports JSON (Task 3).
    
    Args:
        file_path (str): Path to the output file
        data (dict or list): Python object to write
        file_format (str): File format ('json', 'xml', 'yaml', 'yml')
        
    Returns:
        bool: True if write was successful
        
    Raises:
        DataWriterError: If file cannot be written or format is not supported
    """
    if file_format == 'json':
        return write_json_file(file_path, data)
    else:
        raise DataWriterError(
            f"Format '{file_format}' is not yet supported for writing.\n"
            f"Currently supported: json"
        )


def validate_json_syntax(file_path):
    """
    Verify that a JSON file has valid syntax.
    
    Args:
        file_path (str): Path to the JSON file to validate
        
    Returns:
        bool: True if JSON is valid
        
    Raises:
        DataWriterError: If JSON syntax is invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        raise DataWriterError(
            f"Invalid JSON syntax in '{file_path}':\n"
            f"  Line {e.lineno}, Column {e.colno}: {e.msg}"
        )
    except Exception as e:
        raise DataWriterError(
            f"Cannot validate JSON file '{file_path}':\n  {e}"
        )
