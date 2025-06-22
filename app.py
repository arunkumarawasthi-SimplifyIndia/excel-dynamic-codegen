
import streamlit as st
import pandas as pd
from excel_to_python_dynamic.codegen import generate_code

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

# Load logos
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col3:
    st.image("edelweiss_logo.png", width=100)

st.markdown("## Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Select Sheet", xls.sheet_names)

    if sheet_name:
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        st.success("File uploaded and previewed successfully")
        st.markdown("### 📊 Excel Preview")
        st.dataframe(df)

        if st.button("▶️ Run Code and Show Output"):
            try:
                logic_fn, code = generate_code(df)
                result = logic_fn(df.copy())
                st.success("Code executed successfully.")
                st.markdown("### 📤 Output Data")
                st.dataframe(result)
                st.markdown("### 📜 Generated Python Code")
                st.code(code, language="python")
            except Exception as e:
                st.error(f"Error executing logic: {e}")
