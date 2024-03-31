import json
import yaml
import csv
import os


# Function to read Swagger file
def read_swagger_file(file_content, file_type):
    """
    Read Swagger file content (either JSON or YAML) and return the parsed content.
    """
    if file_type == 'json':
        return json.loads(file_content)
    elif file_type in ['yaml', 'yml']:
        return yaml.safe_load(file_content)
    else:
        raise ValueError("Unsupported file format. Only JSON and YAML are supported.")


def parse_swagger(swagger_data):
    """
    Parse the Swagger data to extract information from paths and definitions.
    Return a list of dictionaries with the extracted data.
    """
    parsed_data = []

    # Parse paths
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


def write_to_csv(data, output_file):
    """
    Write the parsed data to a CSV file.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['path', 'method', 'summary', 'description', 'parameters', 'responses'])
        writer.writeheader()
        writer.writerows(data)


def process_swagger_file(file_content, file_type, output_file):
    """
    function to integrate with Streamlit
    """
    swagger_data = read_swagger_file(file_content, file_type)
    parsed_data = parse_swagger(swagger_data)
    write_to_csv(parsed_data, output_file)
