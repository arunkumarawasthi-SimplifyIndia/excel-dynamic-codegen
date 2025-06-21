import pandas as pd
from openpyxl import load_workbook
import re

def parse_range(cell_range):
    match = re.match(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', cell_range)
    if match:
        start_col, start_row, end_col, end_row = match.groups()
        return start_col, int(start_row), end_col, int(end_row)
    return None

def convert_formula_to_python(formula):
    if formula.startswith('=XLOOKUP'):
        match = re.match(r'=XLOOKUP\((.*?),(.*?),(.*?),(.*?)\)', formula)
        if match:
            lookup_val, lookup_range, return_range, not_found = match.groups()
            _, _, lookup_col, _ = parse_range(lookup_range)
            _, _, return_col, _ = parse_range(return_range)
            return (
                f"match_row = data[data['{lookup_col}'] == {lookup_val}]\n"
                f"xlookup_result = match_row['{return_col}'].values[0] if not match_row.empty else {not_found}\n"
                f"data['XLOOKUP_Result'] = xlookup_result"
            )

    elif formula.startswith('=OFFSET'):
        match = re.match(r'=OFFSET\(([A-Z]+)(\d+),(\d+),(\d+)\)', formula)
        if match:
            col, row, row_offset, col_offset = match.groups()
            iloc_row = int(row) - 1 + int(row_offset)
            return (
                f"offset_result = data.iloc[{iloc_row}, 1]  # Adjust column index if needed\n"
                f"data['OFFSET_Result'] = offset_result"
            )

    elif formula.startswith('=INDEX'):
        match = re.match(r'=INDEX\((.*?),(\d+)\)', formula)
        if match:
            cell_range, row_num = match.groups()
            _, _, col, _ = parse_range(cell_range)
            iloc_index = int(row_num) - 1
            return (
                f"index_result = data['{col}'].iloc[{iloc_index}]\n"
                f"data['INDEX_Result'] = index_result"
            )

    return "# Unsupported formula"

def read_excel_and_generate_code(file_path, sheet_name):
    wb = load_workbook(filename=file_path, data_only=False)
    sheet = wb[sheet_name]
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    formulas = {}
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                formulas[cell.coordinate] = cell.value

    # Build the calculate() logic
    logic_lines = []
    python_code = "def calculate(data):\n"
    for coord, formula in formulas.items():
        logic = convert_formula_to_python(formula)
        for line in logic.split("\n"):
            python_code += f"    {line}\n"
            logic_lines.append(f"    {line}")
    python_code += "    return data\n"

    with open("generated_logic.py", "w") as f:
        f.write(python_code)

    # Full code assumes `data` is passed externally (no file path, no sheet name)
    full_script = (
        "def calculate(data):\n"
        f"{chr(10).join(logic_lines)}\n"
        "    return data\n\n"
        "result = calculate(data)\n"
        "print(result)\n"
    )

    with open("generated_full_code.py", "w") as f:
        f.write(full_script)

    print("✅ generated_logic.py created")
    print("✅ generated_full_code.py created (clean, no file/sheet dependency)")
