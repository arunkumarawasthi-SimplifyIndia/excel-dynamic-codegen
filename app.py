
import streamlit as st
import pandas as pd
import os
from generated_full_code import calculate_logic

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col2:
    st.markdown("<h1 style='text-align: center;'>Excel to Dynamic Python Code Generator</h1>", unsafe_allow_html=True)
with col3:
    st.image("edelweiss_logo.png", width=100)

st.subheader("🧠 Excel to Dynamic Python Code Generator")
uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    selected_sheet = st.selectbox("Select Sheet", sheet_names)
    df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

    st.success("File uploaded and previewed successfully")
    st.subheader("📊 Excel Preview")
    st.dataframe(df)

    df.to_csv("temp_data.csv", index=False)

    st.subheader("📦 Full Generated Python Script")
    with open("generated_full_code.py", "r") as f:
        st.code(f.read(), language="python")

    if st.button("▶️ Run Code and Show Output"):
        try:
            result = calculate_logic(df)
            st.success("Code executed successfully.")
            st.subheader("🧾 Output Data")
            st.dataframe(result)
        except Exception as e:
            st.error(f"❌ Error executing logic: {e}")
