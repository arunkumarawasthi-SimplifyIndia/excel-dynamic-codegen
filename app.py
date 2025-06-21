import streamlit as st
import pandas as pd
import os
from generated_full_code import calculate_logic

st.set_page_config(layout="wide", page_title="Excel to Dynamic Python Code Generator")

# Display title and logos
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col2:
    st.title("Excel to Dynamic Python Code Generator")
with col3:
    st.image("edelweiss_logo.png", width=100)

st.markdown("### 🧠 Excel to Dynamic Python Code Generator")
uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name=None)
    sheet_names = list(df.keys())
    selected_sheet = st.selectbox("Select Sheet", sheet_names)
    data = df[selected_sheet]

    st.success("File uploaded and previewed successfully")
    st.markdown("### 📊 Excel Preview")
    st.dataframe(data)

    if st.button("▶️ Run Code and Show Output"):
        try:
            result = calculate_logic(data.copy())
            st.success("✅ Code executed successfully.")
            st.markdown("### 🧮 Output Data")
            st.dataframe(result)
        except Exception as e:
            st.error(f"❌ Error executing logic: {e}")
else:
    st.info("Please upload an Excel file to proceed.")
