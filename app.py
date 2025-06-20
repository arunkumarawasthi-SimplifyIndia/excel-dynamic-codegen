import streamlit as st
import pandas as pd
import os
from openpyxl import load_workbook
from generate_code import read_excel_and_generate_code
import importlib.util

st.set_page_config(page_title="Excel → Python Converter", layout="wide")
st.title("🧠 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    # Step 1: Save file locally
    os.makedirs("temp_uploaded", exist_ok=True)
    file_path = os.path.join("temp_uploaded", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Step 2: Show available sheets
    xls = pd.ExcelFile(file_path)
    selected_sheet = st.selectbox("📑 Select worksheet", xls.sheet_names)

    # Step 3: Read and display selected worksheet
    df = pd.read_excel(file_path, sheet_name=selected_sheet)
    st.subheader("📊 Excel Sheet Preview")
    st.dataframe(df)

    # Step 4: Generate code from selected worksheet
    if selected_sheet:
        read_excel_and_generate_code(file_path, selected_sheet)
        st.success("✅ Code generated successfully.")

    # Step 5: Show logic-only Python function
    st.subheader("🛠️ Generated Function (calculate)")
    with open("generated_logic.py", "r") as f:
