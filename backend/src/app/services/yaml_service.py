# /services/yaml_service.py
import yaml
import logging
from flask import jsonify

ALLOWED_FILE_EXTENSIONS = ['.yml', '.yaml']

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)

def is_allowed_file_extension(file_path):
    """Checks if the file path has an allowed extension."""
    return any(file_path.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS)

def preprocess_special_characters(content):
    """Replaces <br/> with \\n to ensure JSON compatibility."""
    return content.replace("<br/>", "\\n")

def convert_yaml_to_json_array(data, path):
    if not is_allowed_file_extension(path):
        return {"content": data, "success": True}

    try:
        content = data.get('content', '')

        # Step 1: Index all lines
        lines = content.splitlines()
        indexed_lines = []
        
        for line_num, line in enumerate(lines, 1):
            line = line.rstrip()  # Remove trailing spaces
            
            if line.startswith("#"):
                indexed_lines.append({"type": "comment", "line": line, "line_num": line_num})
            elif line.strip() == "":
                indexed_lines.append({"type": "empty", "line": "", "line_num": line_num})
            else:
                indexed_lines.append({"type": "data", "line": line, "line_num": line_num})

        # Step 2: Extract only YAML data lines
        yaml_content = "\n".join([item["line"] for item in indexed_lines if item["type"] == "data"])
        yaml_dict = yaml.safe_load(yaml_content) if yaml_content.strip() else {}

        # Step 3: Match parsed data back to original indexed lines
        json_array = []
        used_lines = set()

        def process_yaml_data(yaml_data, parent_key=None):
            """Recursively process YAML and match it to indexed lines"""
            output = []

            if isinstance(yaml_data, dict):
                for key, value in yaml_data.items():
                    matching_line = next((item for item in indexed_lines if item["line"].startswith(f"{key}:") and item["line_num"] not in used_lines), None)

                    line_num = matching_line["line_num"] if matching_line else None
                    if line_num:
                        used_lines.add(line_num)

                    entry = {
                        "type": type(value).__name__,
                        "name": key,
                        "value": None if isinstance(value, (dict, list)) else value,
                        "line_num": line_num
                    }

                    if isinstance(value, dict):
                        entry["fields"] = process_yaml_data(value, key)

                    elif isinstance(value, list):
                        entry["fields"] = []
                        for item in value:
                            if isinstance(item, dict):
                                entry["fields"].append({
                                    "type": "dict",
                                    "name": None,
                                    "value": None,
                                    "fields": process_yaml_data(item, key)
                                })
                            else:
                                # Find correct line number for list items
                                list_line = next((l for l in indexed_lines if f"- {item}" in l["line"] and l["line_num"] not in used_lines), None)
                                list_item = {
                                    "type": type(item).__name__,
                                    "name": None,
                                    "value": item,
                                    "line_num": list_line["line_num"] if list_line else None
                                }
                                if list_line:
                                    used_lines.add(list_line["line_num"])

                                entry["fields"].append(list_item)

                    output.append(entry)

            return output

        # Step 4: Convert parsed YAML into JSON format
        json_array = process_yaml_data(yaml_dict)

        # Step 5: Append comments and empty lines back into the JSON array
        for line in indexed_lines:
            if line["type"] in ["comment", "empty"]:
                json_array.append({
                    "type": line["type"],
                    "name": None,
                    "value": line["line"],
                    "line_num": line["line_num"]
                })

        # Sort by line number to preserve order
        json_array.sort(key=lambda x: x["line_num"] if x["line_num"] is not None else float('inf'))

        return {"data": json_array, "success": True}

    except Exception as e:
        return {"content": f"Error: Failed to parse YAML due to {str(e)}", "success": False}
