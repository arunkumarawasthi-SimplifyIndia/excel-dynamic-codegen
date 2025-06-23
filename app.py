import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import openpyxl

st.set_page_config(layout="wide")
st.title("Excel to Python Code Generator with Formula Awareness (Base Version)")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xlsm"])
if uploaded_file:
    try:
        # Load workbook using openpyxl for formula access
        in_memory_file = BytesIO(uploaded_file.read())
        wb = openpyxl.load_workbook(in_memory_file, data_only=False)
        sheet_names = wb.sheetnames
        selected_sheet = st.selectbox("Choose a sheet", sheet_names)
        ws = wb[selected_sheet]

        # Display Excel data (values only)
        data_only_wb = openpyxl.load_workbook(BytesIO(uploaded_file.getvalue()), data_only=True)
        df = pd.DataFrame(data_only_wb[selected_sheet].values)

        st.subheader("Preview of Sheet Data")
        st.dataframe(df)

        # Extract formulas and values
        formula_map = []
        for row in ws.iter_rows():
            for cell in row:
                if cell.value is not None and isinstance(cell.value, str) and cell.value.startswith("="):
                    formula_map.append({
                        "cell": cell.coordinate,
                        "formula": cell.value
                    })

        st.subheader("Extracted Formulas")
        if formula_map:
            st.write(formula_map)
        else:
            st.info("No formulas found in this sheet.")

        # Generate placeholder Python code
        def generate_code(sheet_name):
            code = "import pandas as pd\n"
            code += f"df = pd.read_excel('your_file.xlsx', sheet_name='{sheet_name}')\n"
            code += "# Formula logic translation to be inserted here\n"
            code += "print(df.head())\n"
            return code

        final_code = generate_code(selected_sheet)
        st.subheader("Generated Python Code")
        st.code(final_code, language="python")

        # Download button
        b64 = base64.b64encode(final_code.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="generated_code.py">📥 Download Python Code</a>'
        st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to process the Excel file: {e}")
