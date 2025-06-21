import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from generate_code import read_excel_and_generate_code
from generated_full_code import generate_full_python_code

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="centered")

col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col2:
    st.title("Excel to Dynamic Python Code Generator")
with col3:
    st.image("edelweiss_logo.png", width=100)

st.markdown("### 🧠 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file is not None:
    file_path = f"temp_uploaded/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    df = pd.read_excel(file_path)
    st.success("✅ File uploaded and previewed successfully")
    st.subheader("📊 Excel Preview")
    st.dataframe(df)

    # Generate code logic
    read_excel_and_generate_code(file_path)

    # Display generated logic
    st.subheader("🛠️ Generated Python Code")
    with open("generated_logic.py", "r") as f:
        st.code(f.read(), language="python")

    # Display full runnable Python code
    st.subheader("📦 Full Generated Python Script")
    full_script = generate_full_python_code(file_path, df.columns[0])  # Use first sheet or update logic as needed
    st.code(full_script, language="python")
    st.download_button("📥 Download Full Python File", full_script, file_name="generated_code.py")

    # Run logic and show output
    st.markdown("### ▶️ Run Code and Show Output")
    try:
        from generated_logic import calculate
        output_df = calculate(df)
        st.dataframe(output_df)
    except Exception as e:
        st.error(f"❌ Error executing logic: {e}")
