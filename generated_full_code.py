def generate_full_python_code(file_path, sheet_name):
    try:
        with open("generated_logic.py", "r") as f:
            logic_code = f.read()
    except Exception as e:
        return f"# ❌ Could not read generated_logic.py: {e}"

    script = f"""import pandas as pd

data = pd.read_excel("{file_path}", sheet_name="{sheet_name}")

{logic_code}

result = calculate(data)
print(result)
"""
    return script
