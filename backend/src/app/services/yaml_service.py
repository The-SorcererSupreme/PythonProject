# /services/yaml_service.py
import yaml
import re
import logging
import json
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

        def process_yaml_data(yaml_data, parent_key=None, parent_id=None):
            """Recursively process YAML and match it to indexed lines"""
            output = []
            line_counter = 1  # Initialize line counter
        
            if isinstance(yaml_data, dict):
                for key, value in yaml_data.items():
                    matching_line = next((item for item in indexed_lines
                                          if f"{key}:" in item["line"].replace(" ", "")
                                          and item["line_num"] not in used_lines), None)
        
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
                        entry["fields"] = process_yaml_data(value, key, parent_id)
        
                    elif isinstance(value, list):
                        entry["fields"] = []
                        if parent_id is None:  # Top-level lists like "tags"
                            list_line_num = line_num
                        else:  # Nested lists, such as "flags"
                            list_line_num = parent_id + 1
        
                        for index, item in enumerate(value):
                            if isinstance(item, dict):
                                processed_fields = []
                                current_line_num = list_line_num + index
        
                                for sub_key, sub_value in item.items():
                                    sub_matching_line = next((l for l in indexed_lines if f"{sub_key}:" in l["line"] and l["line_num"] not in used_lines), None)
        
                                    if sub_matching_line:
                                        sub_line_num = sub_matching_line["line_num"]
                                        used_lines.add(sub_line_num)
                                    else:
                                        current_line_num += 1
                                        sub_line_num = current_line_num
        
                                    processed_fields.append({
                                        "type": type(sub_value).__name__,
                                        "name": sub_key,
                                        "value": sub_value,
                                        "line_num": sub_line_num,
                                        "show_name": True  # For dict items, always set show_name to True
                                    })
        
                                entry["fields"].append({
                                    "type": "dict",
                                    "name": f"{key}[{index}]",
                                    "value": None,
                                    "line_num": list_line_num + index,
                                    "fields": processed_fields
                                })
                            else:
                                entry["fields"].append({
                                    "type": type(item).__name__,
                                    "name": f"{key}[{index}]",
                                    "value": item,
                                    "line_num": list_line_num + index,
                                    "show_name": isinstance(item, dict)  # Set show_name to True only for dict items
                                })
        
                        line_counter += len(value)  # Increment line counter by the number of items in the list
        
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

def convert_json_array_to_yaml(json_data):
    try:
        json_array = json.loads(json_data)
        yaml_output = []
        
        def log_processing(item, output_line_num, parent=None):
            """Prints debugging info about the item being processed."""
            print(f"Processing Item: {item}")
            print(f"  - Type: {item.get('type')}")
            print(f"  - Name: {item.get('name')}")
            print(f"  - Value: {item.get('value')}")
            print(f"  - Detected Line Number: {item.get('line_num')}")
            print(f"  - Placed in YAML Line: {output_line_num}")
            if parent:
                print(f"  - Parent: {parent.get('name')} (Line {parent.get('line_num')})")
            print("-" * 50)

        def wrap_string(value):
            """Ensures the string value is wrapped with quotes."""
            # If the string contains double quotes, wrap in single quotes
            if '"' in value:
                return f"'{value}'"
            # If the string contains single quotes, wrap in double quotes
            elif "'" in value:
                return f'"{value}"'
            else:
                return f'"{value}"'  # Default case, wrap in double quotes

        for item in json_array:
            line_num = item.get("line_num")
            name = item.get("name")
            value = item.get("value")
            item_type = item.get("type")
            output_line_num = len(yaml_output) + 1  

            log_processing(item, output_line_num)

            # Process comments
            if item_type == "comment":
                yaml_output.append(f"{value.strip()}")
                continue
            
            # Process empty lines
            if item_type == "empty":
                yaml_output.append("")
                continue
            
            # Process strings and integers
            if item_type in ["str", "int"]:
                # Wrap string values in quotes
                if item_type == "str":
                    value = wrap_string(value)
                yaml_output.append(f"{name}: {value}")
                continue
            
            # Process lists
            if item_type == "list":
                yaml_output.append(f"{name}:")
                list_items = item.get("fields", [])

                for sub_item in list_items:
                    log_processing(sub_item, len(yaml_output) + 1, item)
                    
                    sub_name = sub_item.get("name")
                    sub_value = sub_item.get("value")
                    sub_type = sub_item.get("type")

                    # If it's a complex list (dict inside a list)
                    if re.match(r".*\[\d+\]$", sub_name) and sub_type == "dict":
                        sub_fields = sub_item.get("fields", [])
                        if sub_fields:
                            first_field = sub_fields[0]
                            yaml_output.append(f"  - {first_field.get('name')}: {first_field.get('value')}")
                            for sub_field in sub_fields[1:]:
                                yaml_output.append(f"    {sub_field.get('name')}: {sub_field.get('value')}")
                    else:
                        # Wrap value in quotes for strings
                        if sub_type == "str":
                            sub_value = wrap_string(sub_value)
                        yaml_output.append(f"  - {sub_value}")
                continue
            
            # Process dictionaries
            if item_type == "dict":
                yaml_output.append(f"{name}:")
                for sub_item in item.get("fields", []):
                    log_processing(sub_item, len(yaml_output) + 1, item)
                    yaml_output.append(f"  {sub_item.get('name')}: {sub_item.get('value')}")

        return "\n".join(yaml_output)
    
    except Exception as e:
        print(f"Error converting JSON to YAML: {e}")
        return json.dumps({"error": str(e)})

def flatten_json(data):
    """
    Flattens a nested JSON structure by moving all 'fields' items to the root list.
    """
    flat_list = []

    def extract_fields(item):
        flat_list.append(item)  # Add current item to the flattened list

        # Recursively add nested fields
        if "fields" in item and isinstance(item["fields"], list):
            for sub_item in item["fields"]:
                extract_fields(sub_item)  # Add subfields to flat list
            del item["fields"]  # Remove 'fields' key after flattening

    for entry in data:
        extract_fields(entry)

    return flat_list

def normalize_line_numbers(json_data):
    """
    Ensures line numbers are continuous and corrects any missing ones.
    Handles nested lists and dictionaries.
    """
    line_counter = 1  # Start numbering from 1

    def assign_line_numbers(data):
        nonlocal line_counter
        for item in data:
            if "line_num" in item:
                print(f"Updating {item['line_num']} to {line_counter}")
                item["line_num"] = line_counter  # Assign new line number
                line_counter += 1

            # If it's a list or dictionary, recursively update its fields
            if "fields" in item and isinstance(item["fields"], list):
                assign_line_numbers(item["fields"])

    print(f"Reassigning numbers for: {json_data}")
    assign_line_numbers(json_data)
    return json_data



def process_list(item):
    """
    Handles list-type entries, ensuring correct formatting.
    """
    if "fields" in item:
        return [process_dict(field) for field in item["fields"]]
    return []


def process_dict(item):
    """
    Handles dictionary-type entries and converts them to nested YAML structures.
    """
    if "fields" in item:
        nested_dict = {}
        for field in item["fields"]:
            nested_dict[field["name"]] = field["value"]
        return nested_dict
    return {}