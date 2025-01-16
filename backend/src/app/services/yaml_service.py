# /services/yaml_service.py
import yaml
import json
import re
from flask import jsonify
import logging
from pprint import pformat
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)

ALLOWED_FILE_EXTENSIONS = ['.yml', '.yaml']



def is_allowed_file_extension(file_path):
    """
    Checks if the file path has an allowed extension.
    """
    return any(file_path.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS)



def convert_yaml_to_json_array(data, path):
    logging.info(f"File extension for '{path}' is allowed, analyzing YAML...")
    if is_allowed_file_extension(path):
        try:
            content = data.get('content', '')
    
            # Capture the comments first using a regex
            comment_pattern = re.compile(r'#(.*)')
            comments = comment_pattern.findall(content)
    
            # Remove comments from the content for YAML parsing
            content_without_comments = re.sub(r'#.*', '', content)
    
            # Parse the YAML content into a dictionary
            yaml_dict = yaml.safe_load(content_without_comments)
    
            # Initialize the resulting JSON array
            json_array = []
    
            # Add comments to the JSON array
            for comment in comments:
                json_array.append({
                "type": "comment",
                "name": "comment",
                "value": comment.strip()
            })
    
            # Recursive function to process each key-value pair
            def process_element(name, value):
                element = {
                    "type": type(value).__name__,
                    "name": name,
                    "value": value
                }
        
                # If the value is a dictionary or list, we should process it further
                if isinstance(value, dict):
                    element["fields"] = []
                    for sub_name, sub_value in value.items():
                        element["fields"].append(process_element(sub_name, sub_value))
                elif isinstance(value, list):
                    element["fields"] = []
                    for sub_value in value:
                        element["fields"].append(process_element("item", sub_value))
        
                return element

            # Process each item in the parsed YAML dictionary
            for key, value in yaml_dict.items():
                json_array.append(process_element(key, value))
            
            logging.info('Reading json string...')
            json_string = json.dumps(json_array)
            return json_string
        
        except Exception as e:
            logging.error(f"Failed to analyze YAML: {str(e)}")
            return {
                "content": f"Error: Failed to parse YAML due to {str(e)}",
                "success": False
            }
    else:
        logging.warning(f"File extension for '{path}' is not allowed.")
        return {
            "content": data,
            "success": True
        }