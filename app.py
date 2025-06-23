
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import io

st.set_page_config(page_title="Excel → Python Code Generator", layout="wide")
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image("simplify_logo.png", width=100)
with col2:
    st.markdown("<h1 style='text-align: center;'>Excel to Dynamic Python Code Generator</h1>", unsafe_allow_html=True)
with col3:
    st.image("edelweiss_logo.png", width=100)
st.title("🧠 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    st.success("✅ File uploaded successfully")
    st.write("📍 Step 1: File received")

    uploaded_bytes = uploaded_file.read()
    try:
        wb = load_workbook(filename=io.BytesIO(uploaded_bytes), data_only=False, keep_vba=True)
        st.write("📍 Step 2: Workbook loaded")

        sheet_names = wb.sheetnames
        st.write("📍 Step 3: Sheets found →", sheet_names)

        selected_sheet = st.selectbox("📑 Select a worksheet", sheet_names)
        df = pd.read_excel(io.BytesIO(uploaded_bytes), sheet_name=selected_sheet)
        st.write("📍 Step 4: Sheet loaded")

        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.fillna("", inplace=True)

        st.subheader(f"📊 Preview of '{selected_sheet}' Sheet")
        st.dataframe(df)

        sheet = wb[selected_sheet]
        formulas = {}
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                    formulas[cell.coordinate] = cell.value

        st.subheader("🧮 Extracted Formulas")
        if formulas:
            st.json(formulas)
        else:
            st.info("No formulas found.")

        # Generate Python code
        columns = df.columns.tolist()
        python_code = "def calculate(data):\n"
        for col in columns:
            python_code += f"    data['{col}_processed'] = data['{col}']  # Placeholder logic\n"
        python_code += "    return data"

        st.subheader("🛠️ Generated Python Code")
        st.code(python_code, language='python')

        if st.button("▶️ Run Code and Show Output"):
            exec_globals = {}
            exec(python_code, exec_globals)
            processed_df = exec_globals['calculate'](df)
            st.subheader("📤 Processed Output")
            st.dataframe(processed_df)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
