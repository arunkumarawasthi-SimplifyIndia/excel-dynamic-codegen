# 📁 app.py
import streamlit as st
import pandas as pd
import io
from openpyxl import load_workbook
from generate_code import read_excel_and_generate_code
import importlib.util
import os

st.set_page_config(page_title="Excel → Python Code Generator", layout="wide")

st.title("🧠 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx", "xlsm"])
import os
from generate_code import read_excel_and_generate_code

if uploaded_file is not None:
    # Step 1: Save uploaded file to local temp directory
    os.makedirs("temp_uploaded", exist_ok=True)
    file_path = os.path.join("temp_uploaded", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Step 2: Load Excel to get sheet names
    xls = pd.ExcelFile(file_path)
    selected_sheet = st.selectbox("📑 Choose worksheet", xls.sheet_names)

    # Step 3: Call the updated code generator with actual file + sheet name
    if selected_sheet:
        read_excel_and_generate_code(file_path, selected_sheet)
        st.success("✅ Python code generated successfully from uploaded Excel + selected sheet.")

if uploaded_file:
    st.success("✅ File uploaded successfully")

    file_path = "uploaded_excel.xlsx"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Step 1: Show sheet names
    wb = load_workbook(file_path, data_only=False)
    sheetnames = wb.sheetnames
    selected_sheet = st.selectbox("📑 Select worksheet to analyze", sheetnames)

    # Step 2: Preview selected sheet
    df = pd.read_excel(file_path, sheet_name=selected_sheet)
    st.subheader("📊 Excel Preview")
    st.dataframe(df)

    # Step 3: Run code generation from selected sheet only
    def extract_formulas_from_sheet(path, sheet):
        wb = load_workbook(path, data_only=False)
        ws = wb[sheet]
        formulas = {}
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    formulas[cell.coordinate] = cell.value
        return formulas

    formulas = extract_formulas_from_sheet(file_path, selected_sheet)
    st.subheader("📐 Extracted Formulas")
    st.json(formulas)

    # Generate Python logic file based on selected formulas
    from generate_code import convert_formula_to_python

    python_code = "def calculate(data):\n"
    for coord, formula in formulas.items():
        logic = convert_formula_to_python(formula)
        for line in logic.split("\n"):
            python_code += f"    {line}\n"
    python_code += "    return data\n"

    with open("generated_logic.py", "w") as f:
        f.write(python_code)

    st.subheader("🛠️ Generated Python Code")
    st.code(python_code, language='python')

    if st.button("▶️ Run Code and Show Output"):
        try:
            spec = importlib.util.spec_from_file_location("generated_logic", "generated_logic.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            result = module.calculate(df)
            st.subheader("📤 Output after Python Logic")
            st.dataframe(result)
        except Exception as e:
            st.error(f"❌ Error while executing generated code: {e}")

    # New Section: Full Generated Script
    if os.path.exists("generated_full_code.py"):
        st.subheader("📦 Full Generated Python Script")
        with open("generated_full_code.py", "r") as f:
            full_script = f.read()
            st.code(full_script, language='python')
            st.download_button(
                label="📥 Download Full Python File",
                data=full_script,
                file_name="generated_full_code.py",
                mime="text/x-python"
            )
