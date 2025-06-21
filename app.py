
import streamlit as st
import pandas as pd
import os
from generate_code import generate_python_code

st.set_page_config(layout="wide", page_title="Excel to Dynamic Python Code Generator")

st.markdown("## 🧠 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])
sheet_name = None

if uploaded_file:
    try:
        xl = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Select Sheet", xl.sheet_names)
        df = xl.parse(sheet_name)
        df.to_csv("temp_data.csv", index=False)
        st.success("✅ File uploaded and previewed successfully")
        st.markdown("### 📊 Excel Preview")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading file: {e}")

    with open("generated_logic.py", "w") as f:
        f.write(generate_python_code(df))

    with open("generated_logic.py", "r") as f:
        generated_code = f.read()

    st.markdown("### 🛠️ Generated Python Code")
    st.code(generated_code, language="python")

    full_script = f"""
import pandas as pd

data = pd.read_csv('temp_data.csv')

{generated_code}

result = calculate_logic(data)
print(result)
"""
    with open("generated_full_code.py", "w") as f:
        f.write(full_script)

    st.markdown("### 📦 Full Generated Python Script")
    st.code(full_script, language="python")

    if st.button("▶️ Run Code and Show Output"):
        try:
            from generated_full_code import calculate_logic
            result = calculate_logic(df)
            st.write(result)
        except Exception as e:
            st.error(f"❌ Error executing logic: {e}")
