import streamlit as st
import pandas as pd
import importlib.util
import os
import uuid

st.set_page_config(layout="wide")

st.title("Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls", "xlsm"])
if uploaded_file:
    file_id = str(uuid.uuid4())
    saved_path = f"/tmp/{file_id}_{uploaded_file.name}"
    with open(saved_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    xls = pd.ExcelFile(saved_path)
    sheet = st.selectbox("Choose a sheet", xls.sheet_names)
    df = xls.parse(sheet)

    st.subheader("Preview of Data")
    st.dataframe(df)

    # Generate Python code dynamically
    def generate_code(df):
        code = "import pandas as pd\n"
        code += f"df = pd.read_excel('{uploaded_file.name}', sheet_name='{sheet}')\n"
        code += "# Add your logic below\n"
        code += "print(df.head())\n"
        return code

    code = generate_code(df)
    st.subheader("Generated Python Code")
    st.code(code, language="python")

    code_file_path = os.path.join(app_dir, "generated_code.py")
    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    st.download_button("Download Generated Code", code, file_name="generated_code.py")
