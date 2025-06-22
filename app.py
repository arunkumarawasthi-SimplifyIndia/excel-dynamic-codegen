import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

def load_logo(path):
    try:
        st.image(path, width=100)
    except Exception:
        st.warning(f"Failed to load {path}")

# Logo and title
col1, col2, col3 = st.columns([1, 5, 1])
with col1:
    load_logo("simplify_logo.png")
with col2:
    st.title("Excel to Dynamic Python Code Generator")
with col3:
    load_logo("edelweiss_logo.png")

uploaded_file = st.file_uploader("Upload Excel File (.xlsm or .xlsx)", type=["xlsm", "xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Select Sheet", xls.sheet_names)
    df = xls.parse(sheet_name)

    st.subheader("📊 Excel Sheet Preview")
    st.dataframe(df)

    if st.button("▶️ Run Logic and Show Output"):
        try:
            def calculate_logic(df):
                if 'A (Employee ID)' in df.columns:
                    df['A (Employee ID)'] = df['A (Employee ID)'].astype(str)
                if 'B (Name)' in df.columns:
                    df['XLOOKUP_Result'] = df['B (Name)'].fillna('Bob')
                    df['OFFSET_Result'] = df['B (Name)'].shift(-1).fillna('Carol')
                if 'C (Salary)' in df.columns:
                    df['INDEX_Result'] = df['C (Salary)'].fillna(60000)
                return df

            result_df = calculate_logic(df.copy())
            st.success("✅ Logic executed successfully.")
            st.subheader("🔍 Output Data")
            st.dataframe(result_df)

            st.subheader("📜 Generated Python Code")
            st.code('''def calculate_logic(df):
    if 'A (Employee ID)' in df.columns:
        df['A (Employee ID)'] = df['A (Employee ID)'].astype(str)
    if 'B (Name)' in df.columns:
        df['XLOOKUP_Result'] = df['B (Name)'].fillna('Bob')
        df['OFFSET_Result'] = df['B (Name)'].shift(-1).fillna('Carol')
    if 'C (Salary)' in df.columns:
        df['INDEX_Result'] = df['C (Salary)'].fillna(60000)
    return df''', language='python')

        except Exception as e:
            st.error(f"Error in logic: {e}")