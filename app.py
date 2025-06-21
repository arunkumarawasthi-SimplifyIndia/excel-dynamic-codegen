
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from generated_full_code import calculate_logic

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col3:
    st.image("edelweiss_logo.png", width=100)

st.markdown("## 🧠 Excel to Dynamic Python Code Generator")
uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Select Sheet", xls.sheet_names)
    df = pd.read_excel(xls, sheet_name)
    st.success("File uploaded and previewed successfully")
    st.subheader("📊 Excel Preview")
    st.dataframe(df)

    if st.button("▶️ Run Code and Show Output"):
        try:
            result = calculate_logic(df)
            st.success("Code executed successfully.")
            st.subheader("🧾 Output Data")
            st.dataframe(result)
        except Exception as e:
            st.error(f"❌ Error executing logic: {str(e)}")
