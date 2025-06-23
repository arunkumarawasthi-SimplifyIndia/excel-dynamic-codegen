def generate_python_code(df, sheet_name, filename):
    code = f"import pandas as pd\n"
    code += f"df = pd.read_excel('{filename}', sheet_name='{sheet_name}')\n"
    code += "# Sample logic\n"
    code += "print('Data preview:')\n"
    code += "print(df.head())\n"
    return code
