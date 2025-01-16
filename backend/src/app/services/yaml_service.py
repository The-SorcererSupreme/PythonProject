# /services/yaml_service.py
import yaml
from flask import jsonify

def parse_yaml(file_path):
    """Parse the YAML file from the given path and return a dictionary."""
    try:
        print('Parsing yaml file')
        with open(file_path, 'r') as file:
            yaml_content = yaml.safe_load(file)  # Load YAML content
        return yaml_content
    except Exception as e:
        return {"error": f"Failed to parse YAML: {str(e)}"}

def analyze_value(value):
    """Analyze the type of the value and return the field type."""
    if isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "object"
    else:
        return "unknown"

def generate_form_structure(yaml_data):
    """Recursively create a form structure based on YAML data."""
    form_structure = []
    for key, value in yaml_data.items():
        field_type = analyze_value(value)
        if field_type == "object":
            # Recurse into nested objects
            form_structure.append({
                "type": field_type,
                "name": key,
                "fields": generate_form_structure(value)
            })
        else:
            form_structure.append({
                "type": field_type,
                "name": key,
                "value": value
            })
    return form_structure

def analyze_yaml(yaml_content):
    """Analyze the YAML content and return a structure for form fields."""
    return generate_form_structure(yaml_content)
