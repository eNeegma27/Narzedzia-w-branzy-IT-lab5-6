"""
Data writer module for writing files in various formats.
Task 3: Writing data from object to JSON file with proper syntax.
Task 5: Writing data from object to YAML file with proper syntax.
Task 7: Writing data from object to XML file with proper syntax.
"""

import json
import os
from pathlib import Path
from datetime import date, datetime
import yaml
import xml.etree.ElementTree as ET


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


def write_yaml_file(file_path, data):
    """
    Write data to a YAML file with proper formatting.
    Task 5: Writing data from object to YAML file and verifying syntax.
    
    Args:
        file_path (str): Path to the output YAML file
        data (dict or list): Python object to write
        
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
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        raise DataWriterError(
            f"Error writing YAML file '{file_path}':\n  {e}"
        )


def dict_to_xml_element(tag, data):
    """
    Convert a Python dictionary to an XML element.
    
    Args:
        tag (str): The XML tag name
        data: The data to convert (dict, list, str, int, float, etc.)
        
    Returns:
        xml.etree.ElementTree.Element: The XML element
    """
    element = ET.Element(tag)
    
    if isinstance(data, dict):
        for key, value in data.items():
            if key == '@attributes':
                # Handle attributes
                if isinstance(value, dict):
                    for attr_key, attr_value in value.items():
                        element.set(attr_key, str(attr_value))
            elif key == '#text':
                # Handle text content
                element.text = str(value)
            else:
                # Handle child elements
                if isinstance(value, list):
                    # Multiple elements with same tag
                    for item in value:
                        child = dict_to_xml_element(key, item)
                        element.append(child)
                else:
                    # Single element
                    child = dict_to_xml_element(key, value)
                    element.append(child)
    else:
        # Leaf node with simple value
        element.text = str(data) if data is not None else ''
    
    return element


def write_xml_file(file_path, data):
    """
    Write data to an XML file with proper formatting.
    Task 7: Writing data from object to XML file and verifying syntax.
    
    Args:
        file_path (str): Path to the output XML file
        data (dict or list): Python object to write
        
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
        # Find root element - should be only one key in the dict
        if not isinstance(data, dict):
            raise DataWriterError(
                f"XML data must be a dictionary with a single root element.\n"
                f"Got: {type(data).__name__}"
            )
        
        if len(data) != 1:
            raise DataWriterError(
                f"XML data must have exactly one root element.\n"
                f"Got {len(data)} root elements"
            )
        
        # Get the root tag and data
        root_tag = list(data.keys())[0]
        root_data = data[root_tag]
        
        # Convert to XML element
        root = dict_to_xml_element(root_tag, root_data)
        
        # Create tree and write to file with declaration
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")  # Pretty print with 2-space indent
        tree.write(file_path, encoding='UTF-8', xml_declaration=True)
        
        return True
    except DataWriterError:
        raise
    except Exception as e:
        raise DataWriterError(
            f"Error writing XML file '{file_path}':\n  {e}"
        )


def write_file(file_path, data, file_format):
    """
    Write file based on its format.
    Currently supports JSON (Task 3), YAML (Task 5), and XML (Task 7).
    
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
    elif file_format in ('yaml', 'yml'):
        return write_yaml_file(file_path, data)
    elif file_format == 'xml':
        return write_xml_file(file_path, data)
    else:
        raise DataWriterError(
            f"Format '{file_format}' is not yet supported for writing.\n"
            f"Currently supported: json, yaml, yml, xml"
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


def validate_yaml_syntax(file_path):
    """
    Verify that a YAML file has valid syntax.
    
    Args:
        file_path (str): Path to the YAML file to validate
        
    Returns:
        bool: True if YAML is valid
        
    Raises:
        DataWriterError: If YAML syntax is invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True
    except yaml.YAMLError as e:
        raise DataWriterError(
            f"Invalid YAML syntax in '{file_path}':\n"
            f"  {e}"
        )
    except Exception as e:
        raise DataWriterError(
            f"Cannot validate YAML file '{file_path}':\n  {e}"
        )


def validate_xml_syntax(file_path):
    """
    Verify that an XML file has valid syntax.
    
    Args:
        file_path (str): Path to the XML file to validate
        
    Returns:
        bool: True if XML is valid
        
    Raises:
        DataWriterError: If XML syntax is invalid
    """
    try:
        tree = ET.parse(file_path)
        return True
    except ET.ParseError as e:
        raise DataWriterError(
            f"Invalid XML syntax in '{file_path}':\n"
            f"  {e}"
        )
    except Exception as e:
        raise DataWriterError(
            f"Cannot validate XML file '{file_path}':\n  {e}"
        )
