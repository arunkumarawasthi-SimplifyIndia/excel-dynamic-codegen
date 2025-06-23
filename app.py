import streamlit as st
import pandas as pd
from excel_to_python_dynamic.codegen import generate_code

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

st.title("📊 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("Upload Excel File", type=["xls", "xlsx", "xlsm"])
if uploaded_file:
    sheet_names = pd.ExcelFile(uploaded_file).sheet_names
    selected_sheet = st.selectbox("Select Sheet", sheet_names)

    if selected_sheet:
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet, header=None)
        st.subheader("Raw Preview")
        st.dataframe(df, use_container_width=True)

        try:
            df_cleaned, python_code = generate_code(df)
            st.subheader("✅ Cleaned & Interpreted Data")
            st.dataframe(df_cleaned, use_container_width=True)

            st.subheader("🧠 Auto-Generated Python Logic")
            st.code(python_code, language='python')
        except Exception as e:
            st.error(f"Error executing logic: {e}")
