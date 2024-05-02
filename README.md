# Swagger File Parser

This application parses Swagger files (JSON or YAML) and displays the contents in a user-friendly format.
![image](files:screenshot.png)

## Features

- **File Uploader**: Users can upload Swagger files in JSON or YAML format.
- **CSV Conversion**: The uploaded Swagger file is processed and converted into a CSV file.
- **Download Link**: Users can download the resulting CSV file.
- **Data Display**: The contents of the CSV are displayed as a DataFrame in the app.

## How to Use

1. Run the Streamlit app.
2. Use the file uploader to upload your Swagger file.
3. Wait for the file to be processed; a success message will appear upon completion.
4. Download the CSV file using the provided link.
5. View the DataFrame in the app.

## Requirements

- streamlit
- PyYAML
- watchdog

## Installation

To install the required packages, run the following command:

```shell
pip install streamlit pyyaml watchdog
```

Usage
```shell
streamlit run app.py
