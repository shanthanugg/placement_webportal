import pandas as pd
import numpy as np
import json


def replace_invalid_chars(value):
    if isinstance(value, str):
        value = value.replace('.', ' ').replace('/', '|')
    return value

def excel_to_json(excel_file_path, condition_str, key):
    # Read the Excel file
    xls = pd.ExcelFile(excel_file_path)
    data = {}

    # Iterate over each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        # Filter DataFrame based on condition
        df = df[df[key] == condition_str]
        # Replace NaN, Infinity, -Infinity values with None (which will be converted to null in JSON)
        df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
        # Convert all float values to int
        df = df.apply(lambda x: int(x) if isinstance(x, (np.float64, np.float32, float)) else x)
        # Replace invalid characters in DataFrame values
        df = df.apply(replace_invalid_chars)
        # Replace invalid characters in DataFrame column names
        df.columns = [replace_invalid_chars(col) for col in df.columns]
        # Convert DataFrame to JSON
        data[sheet_name] = df.to_dict(orient='records')

    return data

# Example usage
excel_file_path = 'placement-edited.xlsx'  # Change this to your Excel file path
condition_str = "Information Technology"
key = "Branch"

json_data = excel_to_json(excel_file_path, condition_str, key)

# Validate and pretty-print JSON data
with open('data_it.json', 'w', encoding='utf-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)
