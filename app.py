# 📁 app.py

import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import os
from generate_code import read_excel_and_generate_code
from generated_full_code import generate_full_python_code

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="centered")

col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col2:
    st.title("Excel to Dynamic Python Code Generator")
with col3:
    st.image("edelweiss_logo.png", width=100)

st.markdown("### 🧠 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])
if uploaded_file is not None:
    file_path = os.path.join("temp_uploaded", uploaded_file.name)
    os.makedirs("temp_uploaded", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    st.success("✅ File uploaded successfully")
    
    # Load workbook and sheet names
    wb = load_workbook(file_path, data_only=False)
    sheet_names = wb.sheetnames
    selected_sheet = st.selectbox("📄 Select worksheet to process", sheet_names)
    
    # Preview selected worksheet
    df = pd.read_excel(file_path, sheet_name=selected_sheet)
    st.markdown("### 📊 Excel Preview")
    st.dataframe(df)

    # Generate and display logic code
    st.markdown("### 🛠️ Generated Python Code")
    read_excel_and_generate_code(file_path, selected_sheet)
    try:
        with open("generated_logic.py", "r") as f:
            logic_code = f.read()
            st.code(logic_code, language="python")
    except Exception as e:
        st.error(f"❌ Could not read generated logic: {e}")

    # Generate and display full script
    st.markdown("### 📦 Full Generated Python Script")
    full_code = generate_full_python_code(file_path, selected_sheet)
    st.code(full_code, language="python")

    st.download_button(
        label="⬇️ Download Full Python File",
        data=full_code,
        file_name="generated_script.py",
        mime="text/x-python"
    )

    # Run logic
    st.markdown("### ▶️ Run Code and Show Output")
    try:
        from generated_logic import calculate
        output_df = calculate(df.copy())
        st.markdown("### 📂 Output after Python Logic")
        st.dataframe(output_df)
    except Exception as e:
        st.error(f"❌ Error executing logic: {e}")
