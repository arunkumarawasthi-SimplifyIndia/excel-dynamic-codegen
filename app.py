import streamlit as st
import pandas as pd
import os
from generate_code import read_excel_and_generate_code

st.set_page_config(layout="wide")

# UI with logos
col1, col2, col3 = st.columns([1, 5, 1])
with col1:
    try: st.image("simplify_logo.png", width=100)
    except: st.warning("Logo load failed")
with col2:
    st.title("Excel to Dynamic Python Code Generator")
with col3:
    try: st.image("edelweiss_logo.png", width=100)
    except: st.warning("Logo load failed")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsm", "xlsx"])

if uploaded_file:
    with open("temp_uploaded_file.xlsx", "wb") as f:
        f.write(uploaded_file.read())

    df = pd.read_excel("temp_uploaded_file.xlsx", sheet_name=0)
    st.subheader("Excel Preview")
    st.dataframe(df)

    if st.button("▶️ Generate Python Code"):
        python_code = read_excel_and_generate_code("temp_uploaded_file.xlsx")
        st.success("✅ Code generated successfully.")
        st.subheader("🧠 Generated Python Code")
        st.code(python_code, language="python")

    if os.path.exists("generated_logic.py") and st.button("▶️ Run Logic and Show Output"):
        from generated_logic import calculate_logic
        result = calculate_logic(df.copy())
        st.subheader("✅ Output after applying logic")
        st.dataframe(result)