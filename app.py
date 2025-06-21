
import streamlit as st
import pandas as pd
import os
from generated_logic import calculate_logic

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

st.markdown("## 🧠 Excel to Dynamic Python Code Generator")
st.markdown("Upload an Excel file to generate Python logic based on its content.")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    all_sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    sheet_names = list(all_sheets.keys())

    selected_sheet = st.selectbox("Select a worksheet to view and generate logic:", sheet_names)
    df = all_sheets[selected_sheet]
    st.success("File uploaded and previewed successfully")

    st.markdown("### 📊 Excel Preview")
    st.dataframe(df)

    df.to_csv("temp_data.csv", index=False)

    st.markdown("### 🛠️ Generated Python Code")
    st.code("""def calculate_logic(data):
    match_row = data[data['A'] == 102]
    xlookup_result = match_row['B'].values[0] if not match_row.empty else 'Not Found'
    data['XLOOKUP_Result'] = xlookup_result

    offset_result = data.iloc[2, 1]
    data['OFFSET_Result'] = offset_result

    index_result = data['C'].iloc[1]
    data['INDEX_Result'] = index_result

    return data""", language="python")

    st.markdown("### 📦 Full Generated Python Script")
    st.code("""import pandas as pd

data = pd.read_csv('temp_data.csv')

def calculate_logic(data):
    match_row = data[data['A'] == 102]
    xlookup_result = match_row['B'].values[0] if not match_row.empty else 'Not Found'
    data['XLOOKUP_Result'] = xlookup_result

    offset_result = data.iloc[2, 1]
    data['OFFSET_Result'] = offset_result

    index_result = data['C'].iloc[1]
    data['INDEX_Result'] = index_result

    return data

result = calculate_logic(data)
print(result)
""")

    if st.button("▶️ Run Code and Show Output"):
        try:
            result = calculate_logic(df)
            st.success("✅ Code executed successfully!")
            st.dataframe(result)
        except Exception as e:
            st.error(f"❌ Error executing logic: {e}")
