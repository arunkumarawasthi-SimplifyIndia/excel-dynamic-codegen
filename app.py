import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import io

st.set_page_config(page_title="Step 1: Excel to Python Preview", layout="wide")
st.markdown("<h1 style='text-align: center;'>🧠 Excel to Python Code Generator — Step 1</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Excel Upload and Formula Reader</h4>", unsafe_allow_html=True)

# Optional logo bar
logo_cols = st.columns([1, 6, 1])
with logo_cols[0]:
    try:
        st.image("simplify_logo.png", width=90)
    except:
        st.markdown("🔴")
with logo_cols[2]:
    try:
        st.image("edelweiss_logo.png", width=90)
    except:
        st.markdown("🔵")

uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    st.success("✅ File uploaded successfully")

    uploaded_bytes = uploaded_file.read()
    wb = load_workbook(filename=io.BytesIO(uploaded_bytes), data_only=False, keep_vba=True)
    sheet_names = wb.sheetnames
    st.info(f"📄 Sheets found: {sheet_names}")

    selected_sheet = st.selectbox("📑 Select a worksheet", sheet_names)

    # Load selected sheet as DataFrame
    df = pd.read_excel(io.BytesIO(uploaded_bytes), sheet_name=selected_sheet, dtype=str)
    df.columns = df.columns.astype(str).str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.fillna("", inplace=True)

    st.subheader("📊 Sheet Preview")
    st.dataframe(df, use_container_width=True)

    # Extract formulas
    formulas = {}
    ws = wb[selected_sheet]
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and cell.value.startswith("="):
                formulas[cell.coordinate] = cell.value

    st.subheader("🧮 Extracted Formulas")
    if formulas:
        st.json(formulas)
    else:
        st.info("No formulas found.")

    # Generate placeholder Python code
    python_code = "def calculate(data):\n"
    for col in df.columns:
        python_code += f"    data['{col}_processed'] = data['{col}']  # Placeholder\n"
    python_code += "    return data\n"

    st.subheader("🛠️ Generated Python Code")
    st.code(python_code, language='python')

    # Optional: run code
    if st.button("▶️ Run and Show Output"):
        exec_globals = {}
        exec(python_code, exec_globals)
        result = exec_globals['calculate'](df.copy())
        st.subheader("📤 Output Data")
        st.dataframe(result, use_container_width=True)
