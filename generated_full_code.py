import pandas as pd

def generate_full_python_code(excel_file, sheet_name):
    # Read Excel content into DataFrame
    data = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Load and execute generated logic
    with open("generated_logic.py", "r") as f:
        logic_code = f.read()
        exec(logic_code, globals())  # Defines `calculate()` in global scope

    # Now call the dynamically created calculate function
    result = calculate(data)
    return result
