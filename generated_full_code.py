def generate_full_python_code(file_path, sheet_name):
    try:
        with open("generated_logic.py", "r") as f:
            logic_code = f.read()
    except Exception as e:
        return f"# ❌ Could not read generated_logic.py: {e}"

    # Create a standalone Python script
    script = f"""import pandas as pd

# Load data from Excel
data = pd.read_excel("{file_path}", sheet_name="{sheet_name}")

{logic_code}

# Run the logic
result = calculate(data)
print(result)
"""

    return script
