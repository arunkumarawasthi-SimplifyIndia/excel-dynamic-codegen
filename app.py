import streamlit as st
import pandas as pd
from io import BytesIO
import base64

st.set_page_config(layout="wide")

st.title("Excel to Dynamic Python Code Generator (Stable Version)")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls", "xlsm"])
if uploaded_file:
    try:
        # Read Excel directly from uploaded file in-memory
        xls = pd.ExcelFile(uploaded_file)
        sheet = st.selectbox("Choose a sheet", xls.sheet_names)
        df = xls.parse(sheet)

        st.subheader("Preview of Data")
        st.dataframe(df)

        # Generate dynamic Python code
        def generate_code():
            code = "import pandas as pd\n"
            code += f"df = pd.read_excel('your_file.xlsx', sheet_name='{sheet}')\n"
            code += "# Sample logic\n"
            code += "print(df.head())\n"
            return code

        code_output = generate_code()
        st.subheader("Generated Python Code")
        st.code(code_output, language="python")

        # Download button
        b64 = base64.b64encode(code_output.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="generated_code.py">📥 Download Code File</a>'
        st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to read Excel file: {e}")
