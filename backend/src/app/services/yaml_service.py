# /services/yaml_service.py
import yaml
import json
import re
from flask import jsonify
import logging
from pprint import pformat

ALLOWED_FILE_EXTENSIONS = ['.yml', '.yaml']

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)

def is_allowed_file_extension(file_path):
    """
    Checks if the file path has an allowed extension.
    """
    return any(file_path.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS)

def preprocess_special_characters(content):
    """
    Preprocess special characters in the content to ensure JSON compatibility.
    - Replaces <br/> with \\n (escaped newline for JSON)
    - Keeps \n intact for YAML
    """
    return content.replace("<br/>", "\\n")  # Preserve <br/> as a visual newline in JSON

def convert_yaml_to_json_array(data, path):
    if not is_allowed_file_extension(path):
        return {
            "content": data,
            "success": True
        }

    try:
        content = data.get('content', '')

        # Preprocess special characters like <br/>
        processed_content = preprocess_special_characters(content)

        # Extract comments
        comment_pattern = re.compile(r'#(.*)')
        comments = comment_pattern.findall(processed_content)

        # Remove comments for YAML parsing
        content_without_comments = re.sub(r'#.*', '', processed_content)

        # Parse YAML into a Python dictionary
        yaml_dict = yaml.safe_load(content_without_comments)

        # Initialize the resulting JSON array
        json_array = []

        # Add extracted comments to the JSON array
        for comment in comments:
            json_array.append({
                "type": "comment",
                "name": "comment",
                "value": comment.strip()
            })

        # Recursive function to process key-value pairs
        def process_element(name, value):
            element = {
                "type": type(value).__name__,
                "name": name,
                "value": value
            }

            # Process nested structures
            if isinstance(value, dict):
                element["fields"] = [
                    process_element(sub_name, sub_value) for sub_name, sub_value in value.items()
                ]
            elif isinstance(value, list):
                element["fields"] = [
                    process_element("item", sub_value) for sub_value in value
                ]

            return element

        # Process each top-level YAML key-value pair
        for key, value in yaml_dict.items():
            json_array.append(process_element(key, value))

        # Wrap the JSON array with a success indicator
        result = {
            "data": json_array,
            "success": True
        }

        return json.dumps(result)  # Return the JSON object as a string

    except Exception as e:
        return {
            "content": f"Error: Failed to parse YAML due to {str(e)}",
            "success": False
        }