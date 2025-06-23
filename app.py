
import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import openpyxl
import re

st.set_page_config(layout="wide")
st.title("Excel to Python Code Generator (Jupyter-Compatible Output)")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xlsm"])
if uploaded_file:
    try:
        in_memory_file = BytesIO(uploaded_file.read())
        wb = openpyxl.load_workbook(in_memory_file, data_only=False)
        sheet_names = wb.sheetnames
        selected_sheet = st.selectbox("Choose a sheet", sheet_names)
        ws = wb[selected_sheet]

        data_only_wb = openpyxl.load_workbook(BytesIO(uploaded_file.getvalue()), data_only=True)
        df = pd.DataFrame(data_only_wb[selected_sheet].values)
        st.subheader("Preview of Sheet Data")
        st.dataframe(df)

        formula_lines = []
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    coord = cell.coordinate
                    formula = cell.value

                    if "INDEX" in formula:
                        formula_lines.append(f"# Example translation of INDEX in {{coord}}")
                        formula_lines.append(f"value_{{coord}} = df.iloc[1:4, 2].iloc[1]  # ← replace with parsed range")
                    elif "OFFSET" in formula:
                        formula_lines.append(f"# Example translation of OFFSET in {{coord}}")
                        formula_lines.append(f"value_{{coord}} = df.iloc[2, 1]  # ← replace with parsed position")
                    elif "XLOOKUP" in formula:
                        formula_lines.append(f"# Example translation of XLOOKUP in {{coord}}")
                        formula_lines.append(f"value_{{coord}} = df[df.iloc[:, 0] == 102].iloc[0, 1] if 102 in df.iloc[:, 0].values else 'Not Found'")
                    else:
                        formula_lines.append(f"# Could not parse formula in {{coord}}: {{formula}}")

        full_code = """{template}\n{logic}\nprint(df.head())""".format(
            template="""import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Select file interactively
Tk().withdraw()
file_path = askopenfilename(title="Select your Excel file")

xls = pd.ExcelFile(file_path)
print("Available Sheets:", xls.sheet_names)
sheet_name = input("Enter sheet name to load: ")

df = pd.read_excel(file_path, sheet_name=sheet_name)

# Converted formula logic
""",
            logic="\n".join(formula_lines)
        )

        st.subheader("Generated Python Code (Jupyter Compatible)")
        st.code(full_code, language="python")

        b64 = base64.b64encode(full_code.encode()).decode()
        href = f'<a href="data:file/txt;base64,{{b64}}" download="generated_code_jupyter.py">📥 Download Python Code</a>'
        st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to process the Excel file: {{e}}")
