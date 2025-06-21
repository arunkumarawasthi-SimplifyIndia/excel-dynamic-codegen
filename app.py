import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from generate_code import read_excel_and_generate_code
from generated_full_code import generate_full_python_code

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center;'>📘 Excel to Dynamic <span style='color:#ED3B3B'>Python Code</span> Generator</h1>
    """,
    unsafe_allow_html=True,
)

# File upload
uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    st.success("✅ File uploaded and previewed successfully")

    # Save uploaded file temporarily
    temp_path = f"temp_uploaded/{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Show sheet selection
    wb = load_workbook(filename=temp_path, read_only=True)
    sheet_names = wb.sheetnames
    selected_sheet = st.selectbox("Select Sheet", sheet_names)
    wb.close()

    # Preview Excel contents
    df_preview = pd.read_excel(temp_path, sheet_name=selected_sheet)
    st.markdown("### 📊 Excel Preview")
    st.dataframe(df_preview, use_container_width=True)

    # Generate Python logic
    read_excel_and_generate_code(temp_path)

    # Load generated logic
    with open("generated_logic.py", "r") as f:
        logic_code = f.read()

    st.markdown("### 🛠️ Generated Python Code")
    st.code(logic_code, language="python")

    # Run Full Python Code
    st.markdown("### 📦 Full Generated Python Script")
    try:
        result_df = generate_full_python_code(temp_path, selected_sheet)
        full_code = f"""import pandas as pd

data = pd.read_excel("{temp_path}", sheet_name="{selected_sheet}")

{logic_code}

result = calculate(data)
print(result)"""
        st.code(full_code, language="python")
        st.download_button("📥 Download Full Python File", full_code, file_name="generated_full_script.py")

        # Run the logic and show output
        if st.button("▶️ Run Code and Show Output"):
            st.success("✅ Logic executed successfully!")
            st.dataframe(result_df)

    except Exception as e:
        st.error(f"❌ Error executing logic: {e}")
