
import yaml
import json
from pathlib import Path
from typing import Any, Dict, Union, Optional


def load_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load a YAML file and return its contents as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")


def load_txt(file_path: Union[str, Path], default: Optional[str] = None) -> str:
    """Load a text file and return its contents as a string.
    
    Args:
        file_path: Path to the text file
        default: Default value to return if file is not found. If None, raises error.
    
    Returns:
        File contents as string, or default if file not found and default is provided
    
    Raises:
        FileNotFoundError: If file not found and no default provided
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        if default is not None:
            return default
        raise FileNotFoundError(f"Text file not found: {file_path}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Error reading text file {file_path}: cannot decode with UTF-8")


def load_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load a JSON file and return its contents as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON file {file_path}: {e}")