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

if uploaded_file:
    st.success("✅ File uploaded successfully")

    file_path = "uploaded_excel.xlsx"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Step 1: Display sheet preview
    df = pd.read_excel(file_path)
    st.subheader("📊 Excel Preview")
    st.dataframe(df)

    # Step 2: Generate real Python logic based on formulas
    read_excel_and_generate_code(file_path)

    # Step 3: Load and display generated code
    with open("generated_logic.py", "r") as f:
        python_code = f.read()

    st.subheader("🛠️ Generated Python Code")
    st.code(python_code, language='python')

    # Step 4: Execute the function and show results
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
