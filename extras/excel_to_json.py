import pandas as pd
import json
import numpy as np


def replace_invalid_chars(value):
    if isinstance(value, str):
        value = value.replace('.', ' ').replace('/', '|')
    return value

def excel_to_json(excel_file_path):
    # Read the Excel file
    xls = pd.ExcelFile(excel_file_path)
    data = {}

    # Iterate over each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        # Replace NaN, Infinity, -Infinity values with None (which will be converted to null in JSON)
        df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
        # Convert all float values to int
        df = df.apply(lambda x: int(x) if isinstance(x, (np.float64, np.float32, float)) else x)
        # Replace invalid characters in DataFrame values
        df = df.apply(replace_invalid_chars)
        # Replace invalid characters in DataFrame column names
        df.columns = [replace_invalid_chars(col) for col in df.columns]
        # Use the first row as keys and convert DataFrame to JSON
        data[sheet_name] = df.to_dict(orient='records')

    return data


# Example usage
excel_file_path = 'placement-edited.xlsx'  # Change this to your Excel file path
json_data = excel_to_json(excel_file_path)

# Validate and pretty-print JSON data
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)
