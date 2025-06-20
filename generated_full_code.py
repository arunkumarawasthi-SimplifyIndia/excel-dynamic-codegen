# 📁 generated_full_code.py

def generate_full_python_code(file_path, sheet_name):
    code = f"""import pandas as pd

# 📥 Load data from Excel
data = pd.read_excel("{file_path}", sheet_name="{sheet_name}")

"""
    try:
        with open("generated_logic.py", "r") as f:
            logic = f.read()

        # Add the function logic
        code += "\n" + logic + "\n"

        # Dynamically run the calculate function
        code += """
# ▶️ Run calculation
try:
    result = calculate(data)
    print(result)
except Exception as e:
    print("❌ Error while executing generated logic:", e)
"""

    except Exception as e:
        code += f"# ⚠️ Could not load logic: {e}\n"

    return code
