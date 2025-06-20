# 📁 generated_full_code.py

def generate_full_python_code(file_path, sheet_name):
    code = f"""import pandas as pd

# 📥 Load Excel data
data = pd.read_excel("{file_path}", sheet_name="{sheet_name}")

"""

    try:
        with open("generated_logic.py", "r") as f:
            logic = f.read()

        code += "# 🧠 Injected Logic from Excel formulas\n"
        code += logic + "\n"

        code += """\n
# ▶️ Run the logic
try:
    result = calculate(data)
    print(result)
except Exception as e:
    print("❌ Error during execution:", e)
"""

    except Exception as e:
        code += f"# ⚠️ Could not read generated_logic.py: {e}"

    return code
