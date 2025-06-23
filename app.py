import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import openpyxl
import re

st.set_page_config(layout="wide")
st.title("Excel to Python Code Generator with Formula Conversion")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xlsm"])
if uploaded_file:
    try:
        # Load workbook using openpyxl for formulas
        in_memory_file = BytesIO(uploaded_file.read())
        wb = openpyxl.load_workbook(in_memory_file, data_only=False)
        sheet_names = wb.sheetnames
        selected_sheet = st.selectbox("Choose a sheet", sheet_names)
        ws = wb[selected_sheet]

        # Show values for preview
        data_only_wb = openpyxl.load_workbook(BytesIO(uploaded_file.getvalue()), data_only=True)
        df = pd.DataFrame(data_only_wb[selected_sheet].values)
        st.subheader("Preview of Sheet Data")
        st.dataframe(df)

        # Extract formulas and convert
        converted_lines = []
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    formula = cell.value
                    coordinate = cell.coordinate

                    # Basic INDEX(A1:A3, 2) conversion
                    index_match = re.match(r"=INDEX\(([^,]+),\s*(\d+)\)", formula)
                    if index_match:
                        cell_range, index = index_match.groups()
                        col_letter = re.findall(r"[A-Z]+", cell_range)[0]
                        row_range = list(map(int, re.findall(r"\d+", cell_range)))
                        row_start = row_range[0] - 1
                        row_end = row_range[-1]
                        col_index = ord(col_letter.upper()) - 65
                        python_expr = f"value_{coordinate} = df.iloc[{row_start}:{row_end}, {col_index}].iloc[{int(index)-1}]"
                        converted_lines.append(python_expr)
                    else:
                        converted_lines.append(f"# Could not parse formula in {coordinate}: {formula}")

        # Combine full code
        final_code = "import pandas as pd\n"
        final_code += f"df = pd.read_excel('your_file.xlsx', sheet_name='{selected_sheet}')\n"
        final_code += "\n".join(converted_lines) + "\n"
        final_code += "print(df.head())\n"

        st.subheader("Generated Python Code")
        st.code(final_code, language="python")

        b64 = base64.b64encode(final_code.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="generated_code.py">📥 Download Python Code</a>'
        st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to process the Excel file: {e}")
