# 📁 generated_full_code.py

def generate_full_python_code(file_path, sheet_name):
    code = f"""import pandas as pd

# 📥 Load data from Excel
data = pd.read_excel("{file_path}", sheet_name="{sheet_name}")

"""
    # Append the generated logic from file
    try:
        with open("generated_logic.py", "r") as f:
            logic = f.read()
        code += "\n" + logic + "\n"
        code += """
# ▶️ Run calculation
result = calculate(data)
print(result)
"""
    except Exception as e:
        code += f"\n# ⚠️ Error loading generated logic: {e}\n"

    return code
