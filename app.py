import streamlit as st
import pandas as pd
import os
from generated_full_code import calculate_logic

# App title and logos
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col2:
    st.title("Excel to Dynamic Python Code Generator")
with col3:
    st.image("edelweiss_logo.png", width=100)

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xlsm"])
if uploaded_file:
    df_dict = pd.read_excel(uploaded_file, sheet_name=None)
    sheet = st.selectbox("Select Sheet", list(df_dict.keys()))
    if sheet:
        df = df_dict[sheet]
        st.subheader("Excel Preview")
        st.dataframe(df)

        try:
            result = calculate_logic(df.copy())
            st.success("Code executed successfully.")
            st.subheader("Output Data")
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error executing logic: {e}")

    with open("generated_full_code.py", "r") as code_file:
        st.subheader("📜 Generated Python Code")
        st.code(code_file.read(), language="python")