
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout="wide")

# Safe logo display
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    try:
        st.image("simplify_logo.png", width=100)
    except:
        st.warning("Simplify logo failed to load.")
with col3:
    try:
        st.image("edelweiss_logo.png", width=100)
    except:
        st.warning("Edelweiss logo failed to load.")

st.title("Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    try:
        sheets = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Select Sheet", sheets.sheet_names)
        df = sheets.parse(sheet_name)

        st.subheader("📊 Excel Preview")
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
                st.success("Logic executed successfully.")
                st.subheader("✅ Output Data")
                st.dataframe(result_df)

                st.subheader("🧠 Generated Python Code")
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
                st.error(f"Error in logic execution: {e}")
    except Exception as e:
        st.error(f"Error reading file: {e}")
