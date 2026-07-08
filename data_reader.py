"""
Data reader module for reading files in various formats.
Task 2: Reading data from JSON files and verifying syntax.
Task 4: Reading data from YAML files and verifying syntax.
Task 6: Reading data from XML files and verifying syntax.
"""

import json
import os
from pathlib import Path
import yaml
import xml.etree.ElementTree as ET


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


def xml_element_to_dict(element):
    """
    Convert an XML element tree to a Python dictionary.
    
    Args:
        element: An xml.etree.ElementTree.Element
        
    Returns:
        dict or str: Dictionary representation of the XML element, or string for simple elements
    """
    result = {}
    
    # Add attributes if present
    if element.attrib:
        result['@attributes'] = element.attrib
    
    # Get text content
    text_content = element.text.strip() if element.text else None
    
    # Process child elements
    children = {}
    for child in element:
        child_data = xml_element_to_dict(child)
        
        if child.tag in children:
            # If tag already exists, convert to list
            if not isinstance(children[child.tag], list):
                children[child.tag] = [children[child.tag]]
            children[child.tag].append(child_data)
        else:
            children[child.tag] = child_data
    
    # If there are no children and no attributes, return just the text
    if not children and not element.attrib:
        return text_content if text_content else None
    
    # If there are children but no text content and no attributes
    if children and not text_content and not element.attrib:
        return children
    
    # Build result
    if children:
        result.update(children)
    
    if text_content and children:
        result['#text'] = text_content
    elif text_content and element.attrib:
        result['#text'] = text_content
    
    return result if result else None


def read_xml_file(file_path):
    """
    Read and parse an XML file.
    Task 6: Reading XML file into object and verifying syntax.
    
    Args:
        file_path (str): Path to the XML file
        
    Returns:
        dict: Parsed XML data as dictionary
        
    Raises:
        FileNotFoundError: If file does not exist
        SyntaxError: If XML syntax is invalid
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: '{file_path}'")
    
    # Check if it's actually a file (not a directory)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"'{file_path}' is not a file")
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Convert XML to dictionary with root element as key
        data = {root.tag: xml_element_to_dict(root)}
        return data
        
    except ET.ParseError as e:
        raise SyntaxError(
            f"Invalid XML syntax in '{file_path}':\n"
            f"  {e}"
        )
    except UnicodeDecodeError as e:
        raise SyntaxError(
            f"Cannot decode file '{file_path}' as UTF-8:\n"
            f"  {e}"
        )
    except Exception as e:
        raise SyntaxError(f"Error reading XML file '{file_path}':\n  {e}")


def read_file(file_path, file_format):
    """
    Read file based on its format.
    Currently supports JSON (Task 2), YAML (Task 4), and XML (Task 6).
    
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
    elif file_format == 'xml':
        return read_xml_file(file_path)
    else:
        raise DataReaderError(
            f"Format '{file_format}' is not yet supported for reading.\n"
            f"Currently supported: json, yaml, yml, xml"
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
