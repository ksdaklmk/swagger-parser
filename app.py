import os
import base64
import pandas as pd
import streamlit as st
from swagger_parser import process_swagger_file


def get_download_link(file_path):
    with open(file_path, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{os.path.basename(file_path)}">Download CSV file</a>'
        return href


def display_dataframe(file_path):
    df = pd.read_csv(file_path)
    st.dataframe(df)


st.set_page_config(page_title="Swagger File Parser", layout="wide")
st.title('Swagger File Parser')
uploaded_file = st.file_uploader("Upload a Swagger file (JSON or YAML)", type=['json', 'yaml', 'yml'])
if uploaded_file is not None:
    try:
        file_type = uploaded_file.name.split('.')[-1]
        file_content = uploaded_file.getvalue()
        base_name = os.path.splitext(uploaded_file.name)[0]
        output_file = f'{base_name}_output.csv'

        process_swagger_file(file_content, file_type, output_file)

        st.success('Processing has completed.')
        download_link = get_download_link(output_file)
        st.markdown(download_link, unsafe_allow_html=True)

        display_dataframe(output_file)
    except Exception as e:
        st.error(f"Error processing file: {e}")
