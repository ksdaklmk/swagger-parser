import csv
import os
import json
import yaml


def read_swagger_file(file_content, file_type):
    """
    Read the Swagger file content and parse it based on the file type.

    Args:
        file_content (str): The content of the Swagger file.
        file_type (str): The type of the Swagger file ('json', 'yaml', or 'yml').

    Returns:
        dict: The parsed Swagger data.

    Raises:
        ValueError: If the file format is not supported (only JSON and YAML are supported).
    """
    if file_type == 'json':
        return json.loads(file_content)
    if file_type in ['yaml', 'yml']:
        return yaml.safe_load(file_content)

    raise ValueError("Unsupported file format. Only JSON and YAML are supported.")


def parse_swagger(swagger_data):
    """
    Parse the Swagger data and extract relevant information.

    Args:
        swagger_data (dict): The parsed Swagger data.

    Returns:
        list: A list of dictionaries containing the parsed information for each API endpoint.
    """
    parsed_data = []

    for path, methods in swagger_data.get('paths', {}).items():
        for method, details in methods.items():
            item = {
                'path': path,
                'method': method.upper(),
                'summary': details.get('summary', ''),
                'description': details.get('description', ''),
                'parameters': ', '.join([param.get('name', '') for param in details.get('parameters', [])]),
                'responses': ', '.join([str(code) for code in details.get('responses', {}).keys()])
            }
            parsed_data.append(item)

    return parsed_data


def extract_schemas(swagger_data):
    """
    Extract information about schemas and their properties from the Swagger data.

    Args:
        swagger_data (dict): The parsed Swagger data.

    Returns:
        list: A list of dictionaries containing the parsed information for each schema property.
    """
    schemas = swagger_data.get('components', {}).get('schemas', {})
    parsed_data = []
    
    for schema_name, schema in schemas.items():
        properties = schema.get('properties', {})
        required = schema.get('required', [])

        for prop_name, prop in properties.items():
            enum = prop.get('enum', [])
            item = {
                'schema name': schema_name,
                'properties name': prop_name,
                'type': prop.get('type'),
                'format': prop.get('format'),
                'description': prop.get('description'),
                'example': prop.get('example'),
                'required': prop_name in required,
                'enum': ', '.join(enum) if enum else ''
            }
            parsed_data.append(item)
    return parsed_data


def write_to_csv(data, output_file):
    """
    Write the parsed data to a CSV file.

    Args:
        data (list): The parsed data to be written.
        output_file (str): The path to the output CSV file.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        # Layout for extract_schemas function
        writer = csv.DictWriter(file, fieldnames=['schema name', 'properties name', 'type', 'format', 'description', 'example', 'required', 'enum'])

        writer.writeheader()
        writer.writerows(data)


def process_swagger_file(file_content, file_type, output_file):
    """
    Process the Swagger file, parse the data, and write it to a CSV file.

    Args:
        file_content (str): The content of the Swagger file.
        file_type (str): The type of the Swagger file ('json', 'yaml', or 'yml').
        output_file (str): The path to the output CSV file.
    """
    swagger_data = read_swagger_file(file_content, file_type)
    parsed_data = extract_schemas(swagger_data)
    write_to_csv(parsed_data, output_file)
