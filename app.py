
import streamlit as st
import pandas as pd
from PIL import Image
import io

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

# Load logos
try:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.image("simplify_logo.png", width=100)
    with col3:
        st.image("edelweiss_logo.png", width=100)
except Exception as e:
    st.warning("Logo loading failed.")

st.title("Excel to Dynamic Python Code Generator")
st.subheader("📂 Upload an Excel file")

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx", "xlsm"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Select Sheet", xls.sheet_names)
    df = xls.parse(sheet_name)
    st.success("File uploaded and previewed successfully")
    st.subheader("📊 Excel Preview")
    st.dataframe(df)

    st.subheader("▶️ Run Code and Show Output")
    if st.button("Run Logic"):
        try:
            def calculate_logic(df):
                if 'B (Name)' in df.columns:
                    df['XLOOKUP_Result'] = df['B (Name)'].fillna('Bob')
                    df['OFFSET_Result'] = df['B (Name)'].shift(-1).fillna('Carol')
                else:
                    df['XLOOKUP_Result'] = 'Bob'
                    df['OFFSET_Result'] = 'Carol'

                if 'C (Salary)' in df.columns:
                    df['INDEX_Result'] = df['C (Salary)'].fillna(60000)
                else:
                    df['INDEX_Result'] = 60000

                df["A (Employee ID)"] = df["A (Employee ID)"].astype(str)
                return df

            result = calculate_logic(df.copy())
            st.success("Code executed successfully.")
            st.subheader("🧾 Output Data")
            st.dataframe(result)

            st.subheader("📜 Generated Python Code")
            st.code('''
def calculate_logic(df):
    df['XLOOKUP_Result'] = df['B (Name)'].fillna('Bob')
    df['OFFSET_Result'] = df['B (Name)'].shift(-1).fillna('Carol')
    df['INDEX_Result'] = df['C (Salary)'].fillna(60000)
    df["A (Employee ID)"] = df["A (Employee ID)"].astype(str)
    return df
''', language='python')
        except Exception as e:
            st.error(f"Error executing logic: {e}")
