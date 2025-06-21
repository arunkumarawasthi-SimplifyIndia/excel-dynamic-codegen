import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
from generated_full_code import calculate_logic

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

# Logo Display
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col3:
    st.image("edelweiss_logo.png", width=100)

st.markdown("## 🧠 Excel to Dynamic Python Code Generator")
uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    df_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    sheet_names = list(df_sheets.keys())
    selected_sheet = st.selectbox("Select Sheet", sheet_names)

    df = df_sheets[selected_sheet]
    st.success("File uploaded and previewed successfully")
    st.markdown("### 📊 Excel Preview")
    st.dataframe(df)

    if st.button("▶️ Run Code and Show Output"):
        try:
            result = calculate_logic(df.copy())
            st.success("Code executed successfully.")
            st.markdown("### 📋 Output Data")
            st.dataframe(result)
        except Exception as e:
            st.error(f"❌ Error executing logic: {e}")